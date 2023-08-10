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
from ckeditor.fields import RichTextField

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
                f for f in model_instance._meta.fields
                if isinstance(f, models.ImageField) and f.name == self.image_field_name
            ][0]
            filename = os.path.basename(getattr(model_instance, image_field.name).name)
            setattr(model_instance, self.attname, os.path.splitext(filename)[0])
        return getattr(model_instance, self.attname)


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="MGKSC")[0]


class HomeFeature(models.Model):
    welcome_info = models.TextField(
        max_length=300,
        blank=True,
        default="Welcome to Moi Kadzonzo Girls High School website. It is designed for parents, students, Alumni, staff, sponsors, friends of the school and prospective parents who may know little about us.",
    )

    administration_info = models.TextField(
        max_length=300,
        blank=True,
        default="Meet our team of experienced professionals who manage and lead our organization. Our administration is dedicated to providing the best possible service to our clients and stakeholders."
    )
    administration_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="homeFeatures/",
        blank=True,
        default="default-image.jpg",
    )
    administration_image_alt_text = ImageAltTextField(
        image_field_name="administration_image",
        help_text="Optional: Short description of what the image entails.",
    )

    academics_info = models.TextField(
        max_length=300,
        blank=True,
        default="Our educational programs are designed to prepare students for success in their chosen careers. We offer a wide range of courses and programs, from technical training to liberal arts and sciences.",
    )
    academics_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="homeFeatures/",
        blank=True,
        default="default-image.jpg",
    )
    academics_image_alt_text = ImageAltTextField(
        image_field_name="academics_image", default=""
    )

    staff_info = models.TextField(
        max_length=300,
        blank=True,
        default="Our staff is made up of dedicated and talented individuals who are committed to providing excellent service to our clients and customers. They bring a wealth of experience and expertise to their roles, ensuring that we deliver the highest quality work.",
    )
    staff_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="homeFeatures/",
        blank=True,
        default="default-image.jpg",
    )
    staff_image_alt_text = ImageAltTextField(
        image_field_name="staff_image",
        help_text="Optional: Short description of what the image entails.",
    )

    curricular_info = models.TextField(
        max_length=300,
        blank=True,
        default="Our curricular activities are designed to provide students with opportunities to explore their interests, develop new skills, and build relationships with peers. We offer a wide range of activities, from sports teams and clubs to music and theater programs.",
    )
    curricular_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="homeFeatures/",
        blank=True,
        default="default-image.jpg",
    )
    curricular_image_alt_text = ImageAltTextField(
        image_field_name="curricular_image",
        help_text="Optional: Short description of what the image entails.",
    )

    library_info = models.TextField(
        max_length=300,
        blank=True,
        default="Our library is a vital resource for students and researchers, providing access to a wide range of books, journals, and digital resources. Our knowledgeable staff is available to assist with research and information inquiries.",
    )
    library_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="homeFeatures/",
        blank=True,
        default="default-image.jpg",
    )
    library_image_alt_text = ImageAltTextField(
        image_field_name="library_image",
        help_text="Optional: Short description of what the image entails.",
    )

    alumni_info = models.TextField(
        max_length=300,
        blank=True,
        default="Our alumni are an important part of our community, and we are proud of their accomplishments and contributions. We maintain strong relationships with our alumni, providing opportunities for networking, professional development, and social events.",
    )
    alumni_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="homeFeatures/",
        blank=True,
        default="default-image.jpg",
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
    title = models.CharField(
        max_length=5,
        help_text="Titles and other words associated with a person's name. Example: 'Mr', 'Mrs', 'Miss'",
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    picture = ResizedImageField(
        size=[600, 600], upload_to="staff/", blank=True, default="default value"
    )
    phone_number = models.CharField(max_length=10, blank=True)
    message = models.TextField(max_length=1000, blank=True, help_text="")
    role = models.CharField(
        max_length=30,
        blank=True,
        help_text="Optional. The role of the staff member. Example: 'Principal', 'Deputy Principal', 'HOD'",
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Optional. The department the staff member belongs to.",
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
    name = models.CharField(
        max_length=30,
        help_text="The name of the department. Example: 'Mathematics', 'Humanities'  ",
    )

    def __str__(self):
        return self.name


class SchoolInfo(models.Model):
    name = models.CharField(max_length=100, default='')
    cover_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="about/",
        default="default-image.jpg",
        blank=True,
    )
    image_alt_text = ImageAltTextField(
        image_field_name="cover_image",
        help_text="Optional: short description of what the image entails.",
    )
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    date_modified = models.DateTimeField(blank=True, null=True, auto_now=True)

    objects = InheritanceManager()

    def __str__(self):
        return self.name

    def update_image(self, new_image):
        self.cover_image = new_image
        self.save()

    def delete(self, *args, **kwargs):
        # Delete the image files from the file system
        self.image.delete()

        # Call the parent delete method to delete the object from the database
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("about")


class Administration(SchoolInfo):
    admin_info = RichTextField()


class Academic(SchoolInfo):
    # subject = models.CharField(max_length=70)
    academics_info = RichTextField()


class Admission(SchoolInfo):
    admission_info = RichTextField()


class Curricular(SchoolInfo):
    curricular_info = RichTextField()


class SchoolHistory(SchoolInfo):
    content = RichTextField()


class SchoolValue(SchoolInfo):
    motto = models.TextField(
        max_length=500,
        default="Bright Shining Star of Academic Excellence in the Nation.",
    )
    mission = models.TextField(
        max_length=500,
        default="Instilling Self-Esteem And Empowering The Girl Child For The Competitive Market In Life.",
    )
    vision = models.TextField(
        max_length=500,
        default="To Be A Bright Shining Star of Academic Excellence In The Nation.",
    )


class News(models.Model):
    headline = models.CharField(max_length=250)
    news = RichTextField()
    publisher = models.ForeignKey(Publisher, on_delete=models.SET(get_sentinel_user))
    news_image = ResizedImageField(
        size=[1920, 1300],
        crop=["middle", "center"],
        upload_to="news/",
        default="default-image.jpg",
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
        if not self.id:
            self.create_thumbnail()
        super(Gallery, self).save(*args, **kwargs)


    def create_thumbnail(self):
        # If there is no image associated with this object, return
        if not self.gallery_image:
            return

        # Open original image
        image = Image.open(self.gallery_image.file)

        # Calculate thumbnail size based on the original image size
        original_size = image.size
        max_thumbnail_size = (200, 200)
        thumbnail_size = calculate_thumbnail_size(original_size, max_thumbnail_size)

        # Create thumbnail
        image.thumbnail(thumbnail_size, Image.ANTIALIAS)

        # Save thumbnail to a BytesIO object
        temp_handle = BytesIO()
        image.save(temp_handle, "PNG")
        temp_handle.seek(0)

        # Save the thumbnail to the thumbnail field
        self.thumbnail.save(
            f"{self.gallery_image.name}_thumbnail.png",
            File(temp_handle),
            save=False,
        )

    def delete(self, *args, **kwargs):
        # Delete the image files from the file system
        self.gallery_image.delete()
        self.thumbnail.delete()

        # Call the parent delete method to delete the object from the database
        super().delete(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(
        max_length=50, unique=True, blank=True, verbose_name="Category"
    )
    description = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    date_modified = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category-detail", args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = timezone.localtime(timezone.now())

        self.slug = slugify(self.name)
        self.date_modified = timezone.localtime(timezone.now())
        super(Category, self).save(*args, **kwargs)

    @classmethod
    def update_category(cls, id, name):
        cls.objects.filter(id=id).update(name=name)


def calculate_thumbnail_size(original_size, max_thumbnail_size):
    # Calculate the thumbnail size while preserving the aspect ratio
    width, height = original_size
    max_width, max_height = max_thumbnail_size

    if width <= max_width and height <= max_height:
        # No need to resize, return the original size
        return original_size

    # Calculate the aspect ratio
    aspect_ratio = width / height

    if aspect_ratio > max_width / max_height:
        # Image is wider, limit by width
        thumbnail_width = max_width
        thumbnail_height = int(thumbnail_width / aspect_ratio)
    else:
        # Image is taller or square, limit by height
        thumbnail_height = max_height
        thumbnail_width = int(thumbnail_height * aspect_ratio)

    return thumbnail_width, thumbnail_height