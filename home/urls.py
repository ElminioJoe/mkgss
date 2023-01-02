from django.urls import path
from home.views import HomeView
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('messages/', views.message, name='message'),
]
