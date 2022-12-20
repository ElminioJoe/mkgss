import os
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
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

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='MGKSC')[0]


class HomeFeature(models.Model):

    welcome_info = models.TextField(max_length=300)

    staff_info = models.TextField(max_length=300)
    staff_image =  ResizedImageField(size=[1920, 1300], crop=['middle', 'center'],upload_to='homeFeatures/', default='default value')

    # admission_info = models.TextField(max_length=300)
    # admission_image =  ResizedImageField(size=[1920, 1300], crop=['middle', 'center'],upload_to='homeFeatures/', default='default value')

    academics_info = models.TextField(max_length=300)
    academics_image =  ResizedImageField(size=[1920, 1300], crop=['middle', 'center'],upload_to='homeFeatures/', default='default value')

    curricular_info = models.TextField(max_length=300)
    curricular_image =  ResizedImageField(size=[1920, 1300], crop=['middle', 'center'],upload_to='homeFeatures/', default='default value')

    library_info = models.TextField(max_length=300)
    library_image =  ResizedImageField(size=[1920, 1300], crop=['middle', 'center'],upload_to='homeFeatures/', default='default value')

    alumni_info = models.TextField(max_length=300)
    alumni_image =  ResizedImageField(size=[1920, 1300], crop=['middle', 'center'],upload_to='homeFeatures/', default='default value')

    administration_info = models.TextField(max_length=300)
    administration_image =  ResizedImageField(size=[1920, 1300], crop=['middle', 'center'],upload_to='homeFeatures/', default='default value')


    def __str__(self):
        return 'Home Features'


class Publisher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

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
        return '{} - {}'.format(self.first_name, self.role)


class Department(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class SchoolInfo(PolymorphicModel):
    name = models.CharField(max_length=100)
    image =  ResizedImageField(size=[1920, 1300], crop=['middle', 'center'],upload_to='about/', default='default value', blank=True)
    image_alt_text = models.CharField(max_length=50, blank=True, help_text="A short description of what the image contents are.")


    def __str__(self):
        return '{} -'.format(self.name )


class Administration(SchoolInfo):
    info = models.TextField(max_length=5000)

    def __str__(self):
        return self.name


class Academic(SchoolInfo):
    subject = models.CharField(max_length=70)
    info = models.TextField(max_length=5000)


    def __str__(self):
        return '{} - {}'.format(self.name, self.subject)


class Admission(SchoolInfo):
    info = models.TextField(max_length=5000)

    def __str__(self):
        return self.name


class Curricular(SchoolInfo):
    info = models.TextField(max_length=5000)

    def __str__(self):
        return self.name


class SchoolHistory(SchoolInfo):
    content = models.TextField(max_length=5000)

    def __str__(self):
        return self.name

class SchoolValue(SchoolInfo):
    content = models.TextField(max_length=500)

    def __str__(self):
        return self.name

# class Post(models.Model):
#     post_title = models.CharField(max_length=300, blank=True)
#     post = models.TextField()
#     post_image = ResizedImageField(size=[1920, 1300], crop=['middle', 'center'], upload_to='posts/', blank=True, default='default value')
#     image_alt_text = models.CharField(max_length=50, blank=True, help_text="A short description of what the image contents are.")
#     post_date = models.DateTimeField(null=True, blank=True)
#     modification_date = models.DateTimeField(blank=True, null=True)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
#     slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)

#     def __str__(self):
#         return '{} - {}'.format(self.post_title, self.about or self.department)

#     def get_absolute_url(self):
#         return reverse('post-detail', args=[str(self.id)])

#     def save(self, *args, **kwargs):
#         if self.post_date is None:
#             self.post_date = timezone.localtime(timezone.now())

#         self.slug = slugify('{}'.format(self.post_title))
#         self.modification_date = timezone.localtime(timezone.now())
#         super(Post, self).save(*args, **kwargs)

class News(models.Model):
    headline = models.CharField(max_length=250)
    news = models.TextField()
    publisher = models.ForeignKey(Publisher, on_delete=models.SET(get_sentinel_user))
    news_image = models.ImageField(upload_to='news/', default='default value')
    image_alt_text = models.CharField(max_length=50, blank=True, help_text="A short description of what the image contents are.")
    post_date = models.DateTimeField(null=True, blank=True)
    modification_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    # authors = models.ManyToManyField(Author)

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return '{} - {}'.format(self.headline, self.publisher.first_name)

    def get_absolute_url(self):
        return reverse('news-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.post_date is None:
            self.post_date = timezone.localtime(timezone.now())

        self.slug = slugify(self.headline)
        self.modification_date = timezone.localtime(timezone.now())
        super(News, self).save(*args, **kwargs)

class Message(models.Model):
    message_title = models.CharField(max_length=70)
    message = models.TextField()
    author = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date_created = models.DateTimeField(blank=True, null=True)
    date_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return '{} - {}'.format(self.author, self.message_title)

    def get_absolute_url(self):
        return reverse('message-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())

        self.date_modified = timezone.localtime(timezone.now())
        super(Message, self).save(*args, **kwargs)


class Gallery(models.Model):
    image_alt_text = models.CharField(max_length=50, blank=True, help_text="A short description of what the image contents are.")
    gallery_image = models.ImageField(upload_to='gallery/', default="default value")
    thumbnail = ResizedImageField(crop=['middle', 'center'], upload_to="gallery/thumbnails/", blank=True, null=True, editable=False)
    image_caption = models.TextField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    post_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} - {}'.format(self.category.name, self.image_alt_text)

    def get_absolute_url(self):
        return reverse('gallery-detail')

    def create_thumbnail(self):
        # If there is no image associated with this.
        # do not create thumbnail
        if not self.gallery_image:
            return

        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (200, 150)

        DJANGO_TYPE = self.gallery_image.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'JPG'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'PNG'

        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(BytesIO(self.gallery_image.read()))

        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        # Save the thumbnail
        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.gallery_image.name)[-1],
                temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        self.thumbnail.save(
            '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf,
            save=False
        )

    def save(self, *args, **kwargs):

        self.create_thumbnail()

        force_update = False

        # If the instance already has been saved, it has an id and we set
        # force_update to True
        if self.id:
            force_update = True

        # Force an UPDATE SQL query if we're editing the image to avoid integrity exception
        super(Gallery, self).save(force_update=force_update)


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


