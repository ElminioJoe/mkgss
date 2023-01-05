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

class SchoolInfoForm(forms.ModelForm):
    class Meta:
        model = SchoolInfo
        fields = ['name', 'image', 'image_alt_text']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AdministrationForm(SchoolInfoForm):
    class Meta(SchoolInfoForm.Meta):
        model = Administration

class AcademicForm(SchoolInfoForm):
    subject = forms.CharField(max_length=70)

    class Meta(SchoolInfoForm.Meta):
        model = Academic
        fields = SchoolInfoForm.Meta.fields + ['subject']

class AdmissionForm(SchoolInfoForm):
    class Meta(SchoolInfoForm.Meta):
        model = Admission

class CurricularForm(SchoolInfoForm):
    class Meta(SchoolInfoForm.Meta):
        model = Curricular

class SchoolHistoryForm(SchoolInfoForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta(SchoolInfoForm.Meta):
        model = SchoolHistory
        fields = SchoolInfoForm.Meta.fields + ['content']

class SchoolValueForm(SchoolInfoForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta(SchoolInfoForm.Meta):
        model = SchoolValue
        fields = SchoolInfoForm.Meta.fields + ['content']

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

