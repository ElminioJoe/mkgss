from django import forms
from django.utils.translation import gettext_lazy as _

from .models import *
from .validators import validate_category


class FormWidgets(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            attrs = {}
            if isinstance(field.widget, forms.Textarea):
                attrs.update({"class": "LargeTextField", "rows": "3", "cols": "10"})
            if isinstance(field.widget, forms.TextInput):
                attrs.update({"class": "TextField"})
            if isinstance(field.widget, forms.ClearableFileInput):
                attrs.update({"class": "form-control-file"})
            self.fields[name].widget.attrs.update(attrs)


class StaffForm(FormWidgets, forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            "title",
            "first_name",
            "last_name",
            "role",
            "department",
            "email",
            "picture",
            "phone_number",
            "message",
        ]


class HomeFeatureForm(FormWidgets, forms.ModelForm):
    class Meta:
        model = HomeFeature
        fields = [
            "welcome_info",
            "administration_info",
            "administration_image",
            "academics_info",
            "academics_image",
            "staff_info",
            "staff_image",
            "curricular_info",
            "curricular_image",
            "library_info",
            "library_image",
            "alumni_info",
            "alumni_image",
        ]


class SchoolInfoForm(FormWidgets, forms.ModelForm):
    class Meta:
        model = SchoolInfo
        fields = ["name", "image", "image_alt_text"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AdministrationForm(SchoolInfoForm):
    class Meta(SchoolInfoForm.Meta):
        model = Administration
        fields = SchoolInfoForm.Meta.fields + ["info"]


class AcademicForm(SchoolInfoForm):
    class Meta(SchoolInfoForm.Meta):
        model = Academic
        fields = SchoolInfoForm.Meta.fields + ["subject", "info"]


class AdmissionForm(SchoolInfoForm):
    class Meta(SchoolInfoForm.Meta):
        model = Admission
        fields = SchoolInfoForm.Meta.fields + ["info"]


class CurricularForm(SchoolInfoForm):
    class Meta(SchoolInfoForm.Meta):
        model = Curricular
        fields = SchoolInfoForm.Meta.fields + ["info"]


class SchoolHistoryForm(SchoolInfoForm):
    class Meta(SchoolInfoForm.Meta):
        model = SchoolHistory
        fields = SchoolInfoForm.Meta.fields + ["content"]


class SchoolValueForm(SchoolInfoForm):
    class Meta(SchoolInfoForm.Meta):
        model = SchoolValue
        fields = SchoolInfoForm.Meta.fields + ["motto", "mission", "vision"]


class NewsForm(FormWidgets, forms.ModelForm):
    class Meta:
        model = News
        exclude = ["post_date", "modification_date", "slug"]


class GalleryForm(FormWidgets, forms.ModelForm):
    # create_category = forms.CharField(max_length=50, required=False)
    # category = forms.ChoiceField(
    #     choices=[("", "")], required=False, label="Select Category"
    # )
    # description = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Gallery
        fields = [
            "category",
            "gallery_image",
            # "image_alt_text",
        ]
        labels = {
            "gallery_image": _("Image"),
        }
        help_texts = {"gallery_image": _("upload images")}
        widgets = {
            "gallery_image": forms.ClearableFileInput(
                attrs={"multiple": True, "required": False}
            )
        }

    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.fields["category"].choices += [
            (cat.id, cat.name) for cat in Category.objects.all()
        ]

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        created_category = cleaned_data.get("create_category")
        description = cleaned_data.get("description")

        if not category and not created_category:
            raise forms.ValidationError(
                "Please choose an existing category or create a new one."
            )

        if created_category:
            category = Category.objects.create(
                name=created_category, description=description
            )
            cleaned_data["category"] = category

        return cleaned_data


# GalleryFormSet = forms.formset_factory(GalleryForm, extra =1)


class CategoryForm(FormWidgets, forms.ModelForm):
    # name = forms.CharField(validators=[validate_category])
    class Meta:
        model = Category
        fields = ("name", "description")
        labels = {
            "name": _("Create Category"),
        }
        # help_texts = {
        #     'name': _('Category name.'),
        # }

class GalleryFormSet(FormWidgets, forms.Form):
    name = forms.CharField(label=_("Create Category"), validators=[validate_category])
    description = forms.CharField(widget=forms.Textarea, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                       label=_("Select Category"), required=False)
    gallery_image = forms.ImageField(widget=forms.ClearableFileInput(
                attrs={"multiple": True, "required": False}), label=_("Image"),
                                           required=False)

    def clean_category(self):
        name = self.cleaned_data.get('name')
        category = self.cleaned_data.get('category')

        if not name and not category:
            raise forms.ValidationError(_("Please create a new category or select an existing one"))

        return category

    def save(self, commit=True):
        name = self.cleaned_data.get('name')
        description = self.cleaned_data.get('description')
        category = self.cleaned_data.get('category')
        images = self.cleaned_data.get('gallery_image')

        if name:
            category = Category.objects.create(name=name, description=description)
        else:
            category = Category.objects.get(id=category.id)

        if images:
            for image in images:
                Gallery.objects.create(category=category, gallery_image=image)