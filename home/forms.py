from django import forms
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget


from .models import *
from .validators import validate_category


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
    info = forms.CharField(widget=CKEditorWidget())

    class Meta(SchoolInfoForm.Meta):
        model = Administration
        fields = SchoolInfoForm.Meta.fields + ["info"]


class AcademicForm(SchoolInfoForm):
    class Meta(SchoolInfoForm.Meta):
        model = Academic
        fields = SchoolInfoForm.Meta.fields + ["subject", "info"]


class AdmissionForm(SchoolInfoForm):
    info = forms.CharField(widget=CKEditorWidget())
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
    create_category = forms.CharField(max_length=50, required=False, validators=[validate_category])
    description = forms.CharField(max_length=200, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label="Select Category")
    gallery_image = forms.ImageField(
        label=_("Image"),
        widget=MultipleFileInput(attrs={"required": False}),
        required=False,
    )

    class Meta:
        model = Gallery
        fields = [
            "create_category",
            "description",
            "category",
            "gallery_image",
            # "image_alt_text",
        ]
        labels = {
            "gallery_image": _("Image"),
        }
        help_texts = {"gallery_image": _("upload images")}



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