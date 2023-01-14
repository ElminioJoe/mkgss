from django.urls import path
from home.views import HomeView, AboutView ,SchoolInfoCreateView, SchoolInfoUpdateView, SchoolInfoDeleteView
from . forms import *
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('features/update/<int:pk>/',  SchoolInfoUpdateView.as_view(model=HomeFeature, form_class=HomeFeatureForm, template_name='home/forms/home_features_form.html'), name='home_features_update'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', AboutView.as_view(), name='about'),
    path('about/create/administration/', SchoolInfoCreateView.as_view(model=Administration, form_class=AdministrationForm, template_name='home/forms/administration_form.html'), name='administration_create'),
    path('about/update/administration/<int:pk>/', SchoolInfoUpdateView.as_view(model=Administration, form_class=AdministrationForm, template_name='home/forms/administration_form.html'), name='administration_update'),
    path('about/delete/administration/<int:pk>/', SchoolInfoDeleteView.as_view(model=Administration), name='administration_delete'),
    path('about/update/admission/<int:pk>/', SchoolInfoUpdateView.as_view(model=Admission, form_class=AdmissionForm, template_name='home/forms/admission_form.html'), name='admission_update'),
    path('about/create/academic/', SchoolInfoCreateView.as_view(model=Academic, form_class=AcademicForm, template_name='home/forms/academic_form.html'), name='academic_create'),
    path('about/update/academic/<int:pk>/', SchoolInfoUpdateView.as_view(model=Academic, form_class=AcademicForm, template_name='home/forms/academic_form.html'), name='academic_update'),
    path('about/delete/academic/<int:pk>/', SchoolInfoDeleteView.as_view(model=Academic), name='academic_delete'),
    path('about/create/curricular/', SchoolInfoCreateView.as_view(model=Curricular, form_class=CurricularForm, template_name='home/forms/curricular_form.html'), name='curricular_create'),
    path('about/update/curricular/<int:pk>/', SchoolInfoUpdateView.as_view(model=Curricular, form_class=CurricularForm, template_name='home/forms/curricular_form.html'), name='curricular_update'),
    path('about/delete/curricular/<int:pk>/', SchoolInfoDeleteView.as_view(model=Curricular), name='curricular_delete'),
    path('about/update/school_history/<int:pk>/', SchoolInfoUpdateView.as_view(model=SchoolHistory, form_class=SchoolHistoryForm, template_name='home/forms/school_history_form.html'), name='school_history_update'),
    path('about/update/school_value/<int:pk>/', SchoolInfoUpdateView.as_view(model=SchoolValue, form_class=SchoolValueForm, template_name='home/forms/school_value_form.html'), name='school_value_update'),
    path('about/create/staff/', SchoolInfoCreateView.as_view(model=Staff, form_class=StaffForm, template_name='home/forms/staff_form.html'), name='staff_create'),
    path('about/update/staff/<int:pk>/', SchoolInfoUpdateView.as_view(model=Staff, form_class=StaffForm, template_name='home/forms/staff_form.html'), name='staff_update'),
    path('about/delete/staff/<int:pk>/', SchoolInfoDeleteView.as_view(model=Staff), name='staff_delete'),

    path('contact/', views.contact, name='contact'),
    path('messages/', views.message, name='message'),
]
