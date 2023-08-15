from django import forms
from django.utils.translation import gettext_lazy as _

from .models import *


class FormWidgets(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            attrs = {}
            if isinstance(field.widget, forms.Textarea):
                attrs.update({"class": "LargeTextField ckeditor", "rows": "3", "cols": "10"})
            if isinstance(field.widget, forms.TextInput):
                attrs.update({"class": "TextField"})
            if isinstance(field.widget, forms.ClearableFileInput):
                attrs.update({"class": "form-control-file"})
            if isinstance(field.widget, forms.BooleanField):
                attrs.update({"class": "form-check-input"})
            self.fields[name].widget.attrs.update(attrs)


class MultipleFileInput(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs['multiple'] = 'multiple'
        return super().render(name, value, attrs)

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


class CarouselImageForm(FormWidgets, forms.ModelForm):
    class Meta:
        model = CarouselImage
        fields = ["caption", "carousel_image"]


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
        fields = ["name", "cover_image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"disabled": True, "title":"Disabled"})


class AdministrationForm(SchoolInfoForm):
    class Meta(SchoolInfoForm.Meta):
        model = Administration
        fields = SchoolInfoForm.Meta.fields + ["admin_info"]


class AcademicForm(SchoolInfoForm):
    class Meta(SchoolInfoForm.Meta):
        model = Academic
        fields = SchoolInfoForm.Meta.fields + ["academics_info"]


class AdmissionForm(SchoolInfoForm):
    class Meta(SchoolInfoForm.Meta):
        model = Admission
        fields = SchoolInfoForm.Meta.fields + ["admission_info"]


class CurricularForm(SchoolInfoForm):
    class Meta(SchoolInfoForm.Meta):
        model = Curricular
        fields = SchoolInfoForm.Meta.fields + ["curricular_info"]


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


class AddImageForm(FormWidgets, forms.ModelForm):
    gallery_image = forms.ImageField(
        label=_("Images"),
        widget=MultipleFileInput(attrs={"required": True}),
        required=True,
    )

    rename_category = forms.BooleanField(
        label=_("Rename Category"),
        required=False,
        initial=False,
    )
    new_category_name = forms.CharField(
        label=_("Category Name"),
        required=False,
        max_length=50,
    )
    rename_description = forms.BooleanField(
        label=_("Modify Description"),
        required=False,
        initial=False,
    )
    new_description = forms.CharField(
        label=_("Description"),
        required=False,
        max_length=200,
    )

    class Meta:
        model = Gallery
        fields = ['gallery_image']
        help_texts = {"gallery_image": _("upload images")}

    def clean(self):
        cleaned_data = super().clean()
        rename_category = cleaned_data.get('rename_category')
        new_category_name = cleaned_data.get('new_category_name')
        rename_description = cleaned_data.get('rename_description')
        new_description = cleaned_data.get('new_description')

        if (new_category_name or new_description) and not (rename_category or rename_description):
            self.add_error(None, "You must check the appropriate rename fields.")


        return cleaned_data

class CreateGalleryForm(FormWidgets, forms.ModelForm):
    category_image = forms.ImageField(
        label="Category Image",
        widget=MultipleFileInput(attrs={"required": True}),
        required=True)

    class Meta:
        model = Category
        fields = ['name', 'description', 'category_image']
        help_texts = {"category_image": _("upload images")}


class ContactForm(forms.Form):
    name = forms.CharField(max_length=60, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)