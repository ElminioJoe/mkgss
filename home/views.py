from django.http import Http404
from django.shortcuts import render
from .models import *

# Create your views here.

def home(request):
    try:
        welcome_post = Post.objects.get(target_page__exact='WC')
        about_post = Post.objects.get(target_page__exact='1C')
        admission_post = Post.objects.get(target_page__exact='2C')
        academics_post = Post.objects.get(target_page__exact='3C')
        staff_post = Post.objects.get(target_page__exact='4C')
        sports_post = Post.objects.get(target_page__exact='5C')
        library_post = Post.objects.get(target_page__exact='6C')
        alumni_post = Post.objects.get(target_page__exact='7C')
        board_m_post = Post.objects.get(target_page__exact='8C')
    except Post.DoesNotExist:
        raise Http404("No Post is Currently available.")

    news = News.objects.all()[:4]

    context = {
        'welcome_post': welcome_post,
        'about_post': about_post,
        'admission_post': admission_post,
        'academics_post': academics_post,
        'staff_post': staff_post,
        'sports_post': sports_post,
        'library_post': library_post,
        'alumni_post': alumni_post,
        'board_m_post': board_m_post,
        'news': news,
    }
    return render(request, 'home/home.html', context)

def gallery(request):
    images = Gallery.objects.all().filter(category__gt=0).order_by('category')

    context = {
        'images': images,
    }
    return render(request, 'home/gallery.html', context)

def about(request):
    departments_posts = Post.objects.all().filter(department_id__gt=0)
    school_info = Post.objects.filter(school_info_id__gt=0)
    about = Post.objects.get(target_page__exact='1C')
    context = {
        'departments_posts': departments_posts,
        'school_info': school_info,
        'about': about,
    }
    return render(request, 'home/about.html', context)

def contact(request):
    return render(request, 'home/contact.html',{})
def messages(request):
    return render(request, 'home/message.html',{})
