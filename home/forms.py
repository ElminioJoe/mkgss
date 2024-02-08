from django import forms
from django.utils.translation import gettext_lazy as _

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
            self.fields[name].widget.attrs.update(attrs)


class MultipleFileInput(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs["multiple"] = "multiple"
        return super().render(name, value, attrs)


class StaffForm(FormWidgets, forms.ModelForm):
    class Meta:
        model = models.Staff
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
        model = models.CarouselImage
        fields = ["caption", "carousel_image"]


class HomeFeatureForm(FormWidgets, forms.ModelForm):
    class Meta:
        model = models.HomeFeature
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


class EntryForm(FormWidgets, forms.ModelForm):
    class Meta:
        model = models.Entry
        fields = [
            "title",
            "cover_image",
            "content",
        ]


class BaseEntryFormSet(forms.BaseModelFormSet):
    def __init__(self, entry_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry_type = entry_type
        if entry_type:
            entry_manager = get_entry_object_manager(entry_type)
            if hasattr(entry_manager, "get_queryset"):
                self.queryset = entry_manager.get_queryset().all()
            else:
                raise TypeError(f"{entry_manager} does not provide a valid queryset.")

EntryFormSet = forms.modelformset_factory(
    models.Entry,
    form=EntryForm,
    formset=BaseEntryFormSet,
    extra=2,
    max_num=15,
    fields=[
        "title",
        "cover_image",
        "content",
    ],
)


class NewsForm(FormWidgets, forms.ModelForm):
    class Meta:
        model = models.News
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


def get_entry_object_manager(entry: str):
    if entry:
        entry = entry.lower()
    print(entry)
    manager_name = f"{entry}_entries"
    return getattr(models.Entry, manager_name, None)
