from django.contrib.auth import get_user_model
from django.db import models
from django_resized import ResizedImageField
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from PIL import Image
# Create your models here.

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='MGKSC')[0]
class Publisher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


# class Author(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

class Department(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class SchStatement(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Post(models.Model):
    class TargetLocation(models.TextChoices):
        WELCOME = 'WC', _('Welcome Text Card')
        ABOUT = '1C', _('About Text Card')
        ADMISSION = '2C',_('Admission Text Card')
        ACADEMICS = '3C',_('Academics Text Card')
        STAFF = '4C', _('Staff Text Card')
        SPORTS = '5C', _('Sports Text Card')
        LIBRARY = '6C', _('Library Text Card')
        ALUMNIS = '7C', _('Alumnis Text Card')
        BOARD_MEMBER = '8C', _('Board Members Text Card')
        ANY = 'ANY', _('ANY')

    target_page = models.CharField(max_length=3, choices=TargetLocation.choices, default="ANY")
    post_title = models.CharField(max_length=300, blank=True)
    post = models.TextField()
    post_image = ResizedImageField(size=[1920, 1300], crop=['middle', 'center'], upload_to='posts/', blank=True, default='default value')
    image_alt_text = models.CharField(max_length=50, blank=True, help_text="A short description of what the image contents are.")
    publisher = models.ForeignKey(Publisher, on_delete=models.SET(get_sentinel_user))
    post_date = models.DateTimeField(null=True, blank=True)
    modification_date = models.DateTimeField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    school_info = models.ForeignKey(SchStatement, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    # page = models.ForeignKey('Page', on_delete=models.PROTECT)

    # authors = models.ManyToManyField(Author, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.post_title, self.target_page)

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.post_date is None:
            self.post_date = timezone.localtime(timezone.now())

        self.slug = slugify('{}'.format(self.post_title))
        self.modification_date = timezone.localtime(timezone.now())
        super(Post, self).save(*args, **kwargs)

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


class Gallery(models.Model):
    image_alt_text = models.CharField(max_length=50, blank=True, help_text="A short description of what the image contents are.")
    gallery_image = models.ImageField(upload_to='gallery/', default="default value")
    image_caption = models.TextField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    post_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} - {}'.format(self.category.name, self.image_alt_text)

    def get_absolute_url(self):
        return reverse('gallery-detail')

    def save(self, *args, **kwargs):
        super(Gallery, self).save(*args, **kwargs)


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


