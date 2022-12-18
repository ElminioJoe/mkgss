from django import forms
from django.forms import ModelForm

from .models import *

class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'


class AcademicForm(ModelForm):
    class Meta:
        model = SchoolInfo
        fields = '__all__'
        # exclude = ['slug', 'post_date', 'modification_date']
        widgets = {
            'info': forms.Textarea(attrs={'rows':5,}),
            }
class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = '__all__'


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class GalleryForm(ModelForm):
    class Meta:
        model = Gallery
        fields = '__all__'

