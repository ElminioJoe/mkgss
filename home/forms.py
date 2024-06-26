from django import forms
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from django_ckeditor_5.widgets import CKEditor5Widget
from . import models


class FormWidgets(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            attrs = {}
            if isinstance(field.widget, forms.Textarea):
                attrs.update(
                    {"class": "LargeTextField ckeditor", "rows": "3", "cols": "10"}
                )
            if isinstance(field.widget, forms.TextInput):
                attrs.update({"class": "TextField"})
            if isinstance(field.widget, forms.ClearableFileInput):
                attrs.update({"class": "form-control-file"})
            if isinstance(field.widget, forms.BooleanField):
                attrs.update({"class": "form-check-input"})
            if isinstance(field.widget, forms.DateInput):
                attrs.update({"class": "DateField"})
            self.fields[name].widget.attrs.update(attrs)


class MultipleFileInput(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs["multiple"] = "multiple"
        return super().render(name, value, attrs)


class StaffForm(FormWidgets, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        model = models.Staff
        fields = [
            "title",
            "full_name",
            "department",
            "picture",
            "content",
        ]


class CarouselImageForm(FormWidgets, forms.ModelForm):
    class Meta:
        model = models.CarouselImage
        fields = ["caption", "carousel_image"]


class EntryForm(FormWidgets, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        model = models.Entry
        fields = [
            "title",
            "cover_image",
            "content",
        ]

    def clean_content(self):
        data = self.cleaned_data["content"]
        if not data:
            raise forms.ValidationError("This field is required.")
        return data


class EntryDeleteForm(forms.Form):
    pass

class NewsForm(FormWidgets, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        model = models.News
        fields = [
            "headline", "news_image", "content"
        ]

    def clean_content(self):
        data = self.cleaned_data["content"]
        if not data:
            raise forms.ValidationError("This field is required.")
        return data


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
        model = models.Gallery
        fields = ["gallery_image"]
        help_texts = {"gallery_image": _("upload images")}

    def clean(self):
        cleaned_data = super().clean()
        rename_category = cleaned_data.get("rename_category")
        new_category_name = cleaned_data.get("new_category_name")
        rename_description = cleaned_data.get("rename_description")
        new_description = cleaned_data.get("new_description")

        if (new_category_name or new_description) and not (
            rename_category or rename_description
        ):
            self.add_error(None, "You must check the appropriate rename fields.")

        return cleaned_data


class CreateGalleryForm(FormWidgets, forms.ModelForm):
    category_image = forms.ImageField(
        label="Category Image",
        widget=MultipleFileInput(attrs={"required": True}),
        required=True,
    )

    class Meta:
        model = models.Category
        fields = ["name", "description", "category_image"]
        help_texts = {"category_image": _("upload images")}


class ContactForm(forms.Form):
    name = forms.CharField(max_length=60, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class JobListingForm(FormWidgets, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].required = False

    class Meta:
        model = models.JobListing
        fields = [
            "title", "experience", "type", "description", "application_deadline",
        ]
        widgets = {
            "application_deadline": forms.DateInput(attrs={"type": "date"}),  # Use HTML5 date input
        }
        help_texts = {
            "description": "Information partaining the job listed. i.e. Job Description, Job Requirements, e.t.c",
            "status": 'Set status to "Open" to list the job on the page. Status "Closed" won\'t be listed.',
            "experience": "Experience of the candidate. i.e. 3 Years, Entry level, e.t.c.",
            "type": "e.g. Fulltime, Parttime, Internship, e.t.c",
        }

    def clean_content(self):
        data = self.cleaned_data["description"]
        if not data:
            raise forms.ValidationError("This field is required.")
        return data
