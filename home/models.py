import os
from django.contrib.auth import get_user_model
from django.db import models
from django_resized import ResizedImageField
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from .managers.news_managers import RandomNewsManager
from .utils import create_thumbnail, generate_unique_slug, set_parent_entry


# Create your models here.
class ImageAltTextField(models.CharField):
    def __init__(self, *args, **kwargs):
        self.image_field_name = kwargs.pop("image_field_name", None)
        kwargs["max_length"] = kwargs.get("max_length", 255)
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        image_field_value = getattr(model_instance, self.image_field_name)

        if image_field_value:
            filename = os.path.basename(image_field_value.name)
            alt_text = os.path.splitext(filename)[0]
            setattr(model_instance, self.attname, alt_text)
        return getattr(model_instance, self.attname)


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="MGKSC")[0]


class CarouselImage(models.Model):
    carousel_image = models.ImageField(upload_to="carousel_images/", blank=False)
    image_alt_text = ImageAltTextField(
        image_field_name="carousel_image",
        help_text="Optional: short description of what the image entails.",
    )
    caption = models.CharField(max_length=200, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image_alt_text} - {self.caption}"

    def get_absolute_url(self):
        return reverse_lazy("home")


class Publisher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, blank=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


class Staff(models.Model):
    class StaffRole(models.TextChoices):
        NONE = "", _("---------")
        PRINCIPAL = "PRINCIPAL", _("Principal")
        DEPUTY = "DEPUTY", _("Deputy Principal")
        ADMINISTRATOR = "ADMINISTRATOR", _("Administrator")
        DIRECTOR = "DIRECTOR", _("Board Director")
        TEACHING_STAFF = "TEACHER", _("Teacher")
        NONE_TEACHING_STAFF = "NTS", _("None Teaching Staff")

    title = models.CharField(
        max_length=5, blank=True, default="",
        help_text="Optional: i.e 'Mr', 'Mrs', 'Miss'",
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=10, blank=True)

    content = CKEditor5Field(config_name="minimal")
    role = models.CharField(
        max_length=15, choices=StaffRole, default=StaffRole.NONE, blank=True
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Optional. The department the staff member belongs to.",
    )
    picture = ResizedImageField(
        size=[600, 600], upload_to="staff/", blank=True, default=""
    )
    slug = models.SlugField(max_length=500, unique=True, blank=True, editable=False)

    # department = models.ForeignKey(
    #     "Department", on_delete=models.CASCADE, blank=True, null=True, help_text="Optional. The department the staff member belongs to."
    # )

    def __str__(self):
        return f"{self.full_name} - {self.role}"

    def get_absolute_url(self):
        return reverse_lazy("about")

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(self.__class__.objects, self.full_name)
        super(Staff, self).save(*args, **kwargs)



class Department(models.Model):
    name = models.CharField(
        max_length=30,
        help_text="The name of the department. Example: 'Mathematics', 'Humanities'  ",
    )

    def __str__(self):
        return self.name


class News(models.Model):
    headline = models.CharField(max_length=250)
    content = CKEditor5Field(config_name="minimal")
    publisher = models.ForeignKey(Publisher, on_delete=models.SET(get_sentinel_user))
    news_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="news/",
        default="",
    )
    image_alt_text = ImageAltTextField(
        image_field_name="news_image",
        help_text="Optional: short description of what the image entails.",
    )
    post_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    modification_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    slug = models.SlugField(max_length=500, unique=True, blank=True, editable=False)
    # authors = models.ManyToManyField(Author)

    objects = models.Manager()
    random_data = RandomNewsManager()

    class Meta:
        ordering = ["-post_date"]

    def __str__(self):
        return f"{self.headline} - {self.publisher.full_name()}"

    def get_absolute_url(self):
        # return reverse("news-detail", args=[str(self.id)])
        return reverse_lazy("news")

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(self.__class__.objects, self.headline)
        super(News, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the image files from the file system
        self.news_image.delete()

        # Call the parent delete method to delete the object from the database
        super().delete(*args, **kwargs)


class Gallery(models.Model):
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, blank=True, related_name="images"
    )
    gallery_image = models.ImageField(upload_to="gallery/", blank=False)
    image_alt_text = ImageAltTextField(
        image_field_name="gallery_image",
        help_text="Optional: short description of what the image entails.",
    )
    thumbnail = ResizedImageField(
        crop=["middle", "center"],
        upload_to="gallery/thumbnails/",
        blank=True,
        null=True,
        editable=False,
    )
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - {self.image_alt_text}"

    def save(self, *args, **kwargs):
        create_thumbnail(self, self.gallery_image, self.thumbnail)
        super(Gallery, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the image files from the file system
        self.gallery_image.delete()
        self.thumbnail.delete()

        super().delete(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(
        max_length=50, unique=True, blank=True, verbose_name="Category"
    )
    description = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True, editable=False)
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    date_modified = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category-detail", args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(self.__class__.objects, self.name)
        super(Category, self).save(*args, **kwargs)

    @classmethod
    def update_category(cls, id, name):
        cls.objects.filter(id=id).update(name=name)


class BaseModel(models.Model):
    date_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    date_modified = models.DateTimeField(verbose_name="Date Modified", auto_now=True)
    is_deleted = models.BooleanField(verbose_name="Deleted", default=False)
    date_deleted = models.DateTimeField(
        verbose_name="Date Deleted", null=True, blank=True, editable=False
    )
    slug = models.SlugField(max_length=500, unique=True, blank=True, editable=False)

    class Meta:
        abstract = True

    def delete(self):
        self.is_deleted = True
        self.date_deleted = timezone.now()
        self.save()

    def permanent_delete(self):
        """Permanently delete the object if it's been deleted for more than 30 days."""
        if self.is_deleted and self.date_deleted is not None:
            days_difference = (timezone.now() - self.date_deleted).days
            if days_difference > 30:
                super().delete()


class Entry(BaseModel):
    class Meta:
        verbose_name = "School Info Entry"
        verbose_name_plural = "School Info Entries"

    ENTRY_CHOICES = [
        (None, "---------"),
        ("ADMINISTRATION", "Administration"),
        ("ADMISSION", "Admissions"),
        ("ACADEMIC", "Academic"),
        ("CURRICULAR", "Co-Curricular"),
        ("HISTORY", "School History"),
        ("PRINCIPLES", "Principles"),
        ("MESSAGE", "Principals Message"),
        ("EXTRA", "Extra"),
    ]

    parent_entry = models.ForeignKey(
        "self",
        verbose_name="Parent Entry",
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
        related_name="children",
    )
    entry = models.CharField(
        max_length=15, choices=ENTRY_CHOICES, default=ENTRY_CHOICES[0], blank=True
    )
    title = models.CharField(max_length=150, blank=True, default="")
    content = CKEditor5Field(config_name="minimal")
    cover_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="entries/",
        default="",
        blank=True,
    )
    image_alt_text = ImageAltTextField(
        image_field_name="cover_image",
        help_text="Optional: short description of what the image entails.",
    )

    def __str__(self):
        return f"{self.entry} - {self.title}".upper()

    def get_absolute_url(self):
        return reverse("entry-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self.__class__.objects, self.entry)
        set_parent_entry(self)
        super().save(*args, **kwargs)

    def update_image(self, new_image):
        self.cover_image = new_image
        self.save()

    def has_children(self):
        return Entry.objects.filter(extra_entry=self).exists()
