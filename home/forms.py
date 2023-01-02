from django import forms

from .models import *

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'


class HomeFeatureForm(forms.ModelForm):
    class Meta:
        model = HomeFeature
        fields = '__all__'
        widgets = {
           'welcome_info': forms.Textarea(attrs={'rows': 3}),
           'staff_info': forms.Textarea(attrs={'rows': 3}),
           'academics_info': forms.Textarea(attrs={'rows': 3}),
           'curricular_info': forms.Textarea(attrs={'rows': 3}),
           'library_info': forms.Textarea(attrs={'rows': 3}),
           'alumni_info': forms.Textarea(attrs={'rows': 3}),
           'administration_info': forms.Textarea(attrs={'rows': 3}),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = '__all__'

