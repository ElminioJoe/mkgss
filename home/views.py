from django.http import Http404
from django.shortcuts import redirect, render
from .models import *
from .forms import *

# Create your views here.

def home(request):
    home_features = HomeFeature.objects.all().get()
    # school_history = SchoolHistory.objects.all()[:1]
    # admission = Admission.objects.all()[:1]
    # try:
    #     school_values = SchoolValue.objects.get(name__icontains='motto')
    # except SchoolValue.DoesNotExist:
    #     raise Http404("School Motto not added.")

    news = News.objects.all()[:4]

    # if request.method == 'POST':
    #     post_form = PostForm(request.POST, request.FILES)
    #     if post_form.is_valid():
    #         post_form.save()
    #     return redirect('home')
    # else:
    #     post_form = PostForm()

    context = {
        'home_features': home_features,
        # 'school_history': school_history,
        # 'admission': admission,
        # 'school_values': school_values,
        'news': news,
        # 'post_form': post_form,
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
    # academics = Academic.objects.all()
    # admission = Admission.objects.all()
    # administration = Administration.objects.all()
    # curriculars = Curricular.objects.all()
    # school_virtues = SchoolValue.objects.filter(about__name__contains='School Virtues').all()
    # school_history = SchoolHistory.objects.all()
    staffs = Staff.objects.all()

    # if request.method == 'POST':
    #     # publisher = Publisher.objects.get(pk=1)
    #     post_form = AcademicForm(request.POST, request.FILES)
    #     if post_form.is_valid():
    #         post_form.save()
    #     return redirect('about')
    # else:
    #     post_form = AcademicForm()

    context = {
        # 'academics': academics,
        # 'administration': administration,
        # 'admission': admission,
        # 'curriculars': curriculars,
        # 'school_virtues': school_virtues,
        # 'school_history': school_history,
        'staffs': staffs,
        # 'post_form': post_form,
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
