from django import forms

from .models import *


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
        fields = "__all__"


class HomeFeatureForm(FormWidgets, forms.ModelForm):
    class Meta:
        model = HomeFeature
        fields = "__all__"


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


class MessageForm(FormWidgets, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ["date_created", "date_modified"]


class GalleryForm(FormWidgets, forms.ModelForm):
    class Meta:
        model = Gallery
        exclude = ["post_date", "thumbnail", "slug"]
