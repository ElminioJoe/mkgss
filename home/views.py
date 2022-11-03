from django.shortcuts import render
from .models import *

# Create your views here.

def home(request):
    welcome_post = Post.objects.get(target_page__exact='WC')
    about_post = Post.objects.get(target_page__exact='1C')
    admission_post = Post.objects.get(target_page__exact='2C')
    academics_post = Post.objects.get(target_page__exact='3C')
    staff_post = Post.objects.get(target_page__exact='4C')
    sports_post = Post.objects.get(target_page__exact='5C')
    library_post = Post.objects.get(target_page__exact='6C')
    alumni_post = Post.objects.get(target_page__exact='7C')
    board_m_post = Post.objects.get(target_page__exact='8C')

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
    return render(request, 'home/gallery.html',{})

def about(request):
    return render(request, 'home/about.html',{})

def contact(request):
    return render(request, 'home/contact.html',{})
def messages(request):
    return render(request, 'home/message.html',{})
