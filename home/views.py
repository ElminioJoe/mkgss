from django.http import Http404
from django.shortcuts import render
from .models import *

# Create your views here.

def home(request):
    try:
        welcome_post = Post.objects.filter(about__name__contains='Welcome Text').get()
        about_post = Post.objects.filter(about__name__contains='School History').get()
        admission_post = Post.objects.filter(about__name__contains='Admission').get()
        academics_post = Post.objects.filter(about__name__contains='Academics')[0:1].get()
        staff_post = Post.objects.filter(about__name__contains='Staff').get()
        sports_post = Post.objects.filter(about__name__contains='Co-Curricular')[0:1].get()
        library_post = Post.objects.filter(about__name__contains='Library').get()
        alumni_post = Post.objects.filter(about__name__contains='Alumni').get()
        board_m_post = Post.objects.filter(about__name__contains='Administration').get()
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
    # image_categories = Category.objects.all()
    images = Gallery.objects.all()

    context = {
        # 'image_categories': image_categories,
        'images': images,
    }
    return render(request, 'home/gallery.html', context)

def about(request):
    admission = Post.objects.filter(about__name__contains='Admission').get()
    administration = Post.objects.filter(about__name__contains='Administration').all()
    curriculars = Post.objects.filter(about__name__contains='Co-Curricular').all()
    academics = Post.objects.all().filter(department_id__gt=0)
    school_virtues = Post.objects.filter(about__name__contains='School Virtues').all()
    school_history = Post.objects.filter(about__name__contains='School History').get()
    staffs = Staff.objects.all()

    context = {
        'academics': academics,
        'administration': administration,
        'admission': admission,
        'curriculars': curriculars,
        'school_virtues': school_virtues,
        'school_history': school_history,
        'staffs': staffs,
    }
    return render(request, 'home/about.html', context)

def contact(request):
    return render(request, 'home/contact.html',{})
def messages(request):
    principal = Message.objects.filter(author__role='Principal').get()
    deputy = Message.objects.filter(author__role='Deputy Principal').get()

    context={
        'principal': principal,
        'deputy': deputy
    }
    return render(request, 'home/message.html', context)
