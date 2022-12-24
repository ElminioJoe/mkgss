import os
from django.contrib.auth import get_user_model
from django.core.files import File
from django.db import models
from io import BytesIO
from django_resized import ResizedImageField
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from PIL import Image
from polymorphic.models import PolymorphicModel

# Create your models here.
class ImageAltTextField(models.CharField):
    def __init__(self, *args, **kwargs):
        self.image_field_name = kwargs.pop('image_field_name', None)
        kwargs['max_length'] = kwargs.get('max_length', 255)
        kwargs['blank'] = True
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
    return get_user_model().objects.get_or_create(username='MGKSC')[0]


class HomeFeature(models.Model):

    welcome_info = models.TextField(max_length=300)

    staff_info = models.TextField(max_length=300)
    staff_image =  ResizedImageField(size=[1920, 1300], crop=['middle', 'center'],upload_to='homeFeatures/', default='default value')
    staff_image_alt_text = ImageAltTextField(image_field_name='staff_image')

    academics_info = models.TextField(max_length=300)
    academics_image =  ResizedImageField(size=[1920, 1300], crop=['middle', 'center'],upload_to='homeFeatures/', default='default value')
    academics_image_alt_text = ImageAltTextField(image_field_name='academics_image')

    curricular_info = models.TextField(max_length=300)
    curricular_image =  ResizedImageField(size=[1920, 1300], crop=['middle', 'center'],upload_to='homeFeatures/', default='default value')
    curricular_image_alt_text = ImageAltTextField(image_field_name='curricular_image')

    library_info = models.TextField(max_length=300)
    library_image =  ResizedImageField(size=[1920, 1300], crop=['middle', 'center'],upload_to='homeFeatures/', default='default value')
    library_image_alt_text = ImageAltTextField(image_field_name='library_image')

    alumni_info = models.TextField(max_length=300)
    alumni_image =  ResizedImageField(size=[1920, 1300], crop=['middle', 'center'],upload_to='homeFeatures/', default='default value')
    alumni_image_alt_text = ImageAltTextField(image_field_name='alumni_image')

    administration_info = models.TextField(max_length=300)
    administration_image =  ResizedImageField(size=[1920, 1300], crop=['middle', 'center'],upload_to='homeFeatures/', default='default value')
    administration_image_alt_text = ImageAltTextField(image_field_name='administration_image')

    def __str__(self):
        return 'Home Features'


class Publisher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f'(self.first_name, self.last_name)'

class Staff(models.Model):
    title = models.CharField(max_length=5)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    picture = ResizedImageField(size=[600, 600], upload_to='staff/', blank=True, default='default value')
    phone_number = models.CharField(max_length=10, blank=True)
    about = models.TextField(max_length=1000, blank=True)
    role = models.CharField(max_length=30, blank=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'(self.first_name, self.last_name, self.role)'


class Department(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class SchoolInfo(PolymorphicModel):
    name = models.CharField(max_length=100)
    image =  ResizedImageField(size=[1920, 1300], crop=['middle', 'center'],upload_to='about/', default='default value', blank=True)
    image_alt_text = ImageAltTextField(image_field_name='image')

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

class Administration(SchoolInfo):
    info = models.TextField(max_length=5000)


class Academic(SchoolInfo):
    subject = models.CharField(max_length=70)
    info = models.TextField(max_length=5000)


    def __str__(self):
        return f'(self.name, self.subject)'


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
    news_image = models.ImageField(upload_to='news/', default='default value')
    image_alt_text = ImageAltTextField(image_field_name='news_image')
    post_date = models.DateTimeField(null=True, blank=True)
    modification_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    # authors = models.ManyToManyField(Author)

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return f'(self.headline, self.publisher.first_name)'

    def get_absolute_url(self):
        return reverse('news-detail', args=[str(self.id)])

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



class Message(models.Model):
    message_title = models.CharField(max_length=70)
    message = models.TextField()
    author = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date_created = models.DateTimeField(blank=True, null=True)
    date_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return f'(self.author, self.message_title)'

    def get_absolute_url(self):
        return reverse('message-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())

        self.date_modified = timezone.localtime(timezone.now())
        super(Message, self).save(*args, **kwargs)


class Gallery(models.Model):
    gallery_image = models.ImageField(upload_to='gallery/', default="default value")
    image_alt_text = ImageAltTextField(image_field_name='gallery_image')
    thumbnail = ResizedImageField(crop=['middle', 'center'], upload_to="gallery/thumbnails/", blank=True, null=True, editable=False)
    image_caption = models.TextField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    post_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'(self.category.name, self.image_alt_text)'

    def get_absolute_url(self):
        return reverse('gallery-detail')

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
        self.thumbnail.save(f"{self.gallery_image.name}_thumbnail.{image.format.lower()}",
            File(temp_handle), save=False)


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
    name = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    date_modified = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())

        self.slug = slugify(self.name)
        self.date_modified = timezone.localtime(timezone.now())
        super(Category, self).save(*args, **kwargs)


    @classmethod
    def update_category(cls,id,name):
        cls.objects.filter(id=id).update(name=name)


