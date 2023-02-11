import os
from django.contrib.auth import get_user_model
from django.core.files import File
from django.db import models
from io import BytesIO
from django_resized import ResizedImageField
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from PIL import Image
from model_utils.managers import InheritanceManager

from .managers import RandomManager

# Create your models here.
class ImageAltTextField(models.CharField):
    def __init__(self, *args, **kwargs):
        self.image_field_name = kwargs.pop("image_field_name", None)
        kwargs["max_length"] = kwargs.get("max_length", 255)
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if not getattr(model_instance, self.attname):
            # Generate image alt text using the image filename
            image_field = [
                f
                for f in model_instance._meta.fields
                if isinstance(f, models.ImageField) and f.name == self.image_field_name
            ][0]
            filename = os.path.basename(getattr(model_instance, image_field.name).name)
            setattr(model_instance, self.attname, os.path.splitext(filename)[0])
        return getattr(model_instance, self.attname)


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="MGKSC")[0]


class HomeFeature(models.Model):
    welcome_info = models.TextField(max_length=300, blank=True)

    administration_info = models.TextField(max_length=300, blank=True)
    administration_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="homeFeatures/",
        blank=True,
        default="default value",
    )
    administration_image_alt_text = ImageAltTextField(
        image_field_name="administration_image",
        help_text="Optional: Short description of what the image entails.",
    )

    academics_info = models.TextField(max_length=300, blank=True)
    academics_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="homeFeatures/",
        blank=True,
        default="default value",
    )
    academics_image_alt_text = ImageAltTextField(image_field_name="academics_image")

    staff_info = models.TextField(max_length=300, blank=True)
    staff_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="homeFeatures/",
        blank=True,
        default="default value",
    )
    staff_image_alt_text = ImageAltTextField(
        image_field_name="staff_image",
        help_text="Optional: Short description of what the image entails.",
    )

    curricular_info = models.TextField(max_length=300, blank=True)
    curricular_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="homeFeatures/",
        blank=True,
        default="default value",
    )
    curricular_image_alt_text = ImageAltTextField(
        image_field_name="curricular_image,",
        help_text="Optional: Short description of what the image entails.",
    )

    library_info = models.TextField(max_length=300, blank=True)
    library_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="homeFeatures/",
        blank=True,
        default="default value",
    )
    library_image_alt_text = ImageAltTextField(
        image_field_name="library_image",
        help_text="Optional: Short description of what the image entails.",
    )

    alumni_info = models.TextField(max_length=300, blank=True)
    alumni_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="homeFeatures/",
        blank=True,
        default="default value",
    )
    alumni_image_alt_text = ImageAltTextField(
        image_field_name="alumni_image",
        help_text="Optional: Short description of what the image entails.",
    )

    def __str__(self):
        return "Home Features"

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
    title = models.CharField(max_length=5, help_text="Titles and other words associated with a person's name. Example: 'Mr', 'Mrs', 'Miss'")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    picture = ResizedImageField(
        size=[600, 600], upload_to="staff/", blank=True, default="default value"
    )
    phone_number = models.CharField(max_length=10, blank=True)
    message = models.TextField(max_length=1000, blank=True, help_text="")
    role = models.CharField(max_length=30, blank=True, help_text="Optional. The role of the staff member. Example: 'Principal', 'Deputy Principal', 'HOD'")
    department = models.CharField(max_length=100 ,blank=True, null=True, help_text="Optional. The department the staff member belongs to."
    )

    # department = models.ForeignKey(
    #     "Department", on_delete=models.CASCADE, blank=True, null=True, help_text="Optional. The department the staff member belongs to."
    # )

    def staff_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.staff_full_name()} - {self.role}"

    def get_absolute_url(self):
        return reverse_lazy("about")


class Department(models.Model):
    name = models.CharField(max_length=30, help_text="The name of the department. Example: 'Mathematics', 'Humanities'  ")

    def __str__(self):
        return self.name


class SchoolInfo(models.Model):
    name = models.CharField(max_length=100)
    image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="about/",
        default="default value",
        blank=True,
    )
    image_alt_text = ImageAltTextField(
        image_field_name="image",
        help_text="Optional: short description of what the image entails.",
    )
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    date_modified = models.DateTimeField(blank=True, null=True, auto_now=True)

    objects = InheritanceManager()

    def __str__(self):
        return self.name

    def update_image(self, new_image):
        self.image = new_image
        self.save()

    def delete(self, *args, **kwargs):
        # Delete the image files from the file system
        self.image.delete()

        # Call the parent delete method to delete the object from the database
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("about")


class Administration(SchoolInfo):
    info = models.TextField(max_length=5000)


class Academic(SchoolInfo):
    subject = models.CharField(max_length=70)
    info = models.TextField(max_length=5000)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Admission(SchoolInfo):
    info = models.TextField(max_length=5000)


class Curricular(SchoolInfo):
    info = models.TextField(max_length=5000)


class SchoolHistory(SchoolInfo):
    content = models.TextField(max_length=5000)


class SchoolValue(SchoolInfo):
    motto = models.TextField(max_length=500)
    mission = models.TextField(max_length=500)
    vision = models.TextField(max_length=500)


class News(models.Model):
    headline = models.CharField(max_length=250)
    news = models.TextField()
    publisher = models.ForeignKey(Publisher, on_delete=models.SET(get_sentinel_user))
    news_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="news/",
        default="default value"
    )
    image_alt_text = ImageAltTextField(
        image_field_name="news_image",
        help_text="Optional: short description of what the image entails.",
    )
    post_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    modification_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    # authors = models.ManyToManyField(Author)

    objects = models.Manager()
    random_data = RandomManager()

    class Meta:
        ordering = ["-post_date"]

    def __str__(self):
        return f"{self.headline} - {self.publisher.full_name()}"

    def get_absolute_url(self):
        # return reverse("news-detail", args=[str(self.id)])
        return reverse_lazy("news")

    def save(self, *args, **kwargs):
        if self.post_date is None:
            self.post_date = timezone.localtime(timezone.now())

        self.slug = slugify(self.headline)
        self.modification_date = timezone.localtime(timezone.now())
        super(News, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the image files from the file system
        self.news_image.delete()

        # Call the parent delete method to delete the object from the database
        super().delete(*args, **kwargs)



class Gallery(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, related_name="image_category")
    gallery_image = models.ImageField(upload_to="gallery/", blank=False, default="default value")
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
    # image_caption = models.TextField(null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - {self.image_alt_text}"

    def get_absolute_url(self):
        return reverse("gallery-detail")

    def create_thumbnail(self):
        # If there is no image associated with this object, return
        if not self.gallery_image:
            return

        # Set our max thumbnail size
        THUMBNAIL_SIZE = (200, 150)

        # Open original image and create thumbnail
        image = Image.open(self.gallery_image.file)
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        # Save thumbnail to a BytesIO object
        temp_handle = BytesIO()
        image.save(temp_handle, image.format)
        temp_handle.seek(0)

        # Save the thumbnail to the thumbnail field
        self.thumbnail.save(
            f"{self.gallery_image.name}_thumbnail.{image.format.lower()}",
            File(temp_handle),
            save=False,
        )

    def save(self, *args, **kwargs):
        self.create_thumbnail()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the image files from the file system
        self.gallery_image.delete()
        self.thumbnail.delete()

        # Call the parent delete method to delete the object from the database
        super().delete(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=True, verbose_name="Category")
    description = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    date_modified = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category-detail", args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())

        self.slug = slugify(self.name)
        self.date_modified = timezone.localtime(timezone.now())
        super(Category, self).save(*args, **kwargs)

    @classmethod
    def update_category(cls, id, name):
        cls.objects.filter(id=id).update(name=name)
