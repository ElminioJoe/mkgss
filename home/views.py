from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import View

from .models import *
from .forms import *

# Create your views here.

def update_form_fields(form, model):
    # checks and updates changed form fields
    update_fields = {}
    for field in form.changed_data:
        if form.cleaned_data[field]: # only add non-blank fields to the update_fields dictionary
            update_fields[field] = form.cleaned_data[field]
    model.objects.filter(pk=form.instance.pk).update(**update_fields)

class HomeView(View):
    form_class = HomeFeatureForm
    template_name = 'home/home.html'

    def get(self, request, *args, **kwargs):
        home_features = get_object_or_404(HomeFeature)
        school_history = get_object_or_404(SchoolHistory.objects.only('content'))
        admission = get_object_or_404(Admission.objects.only('info'))
        school_values = get_object_or_404(SchoolValue.objects.only('motto'))
        news = News.objects.order_by('-post_date')[:4]

        form = self.form_class(request.POST, instance=home_features)

        context = {
            'home_features': home_features,
            'school_history': school_history,
            'admission': admission,
            'school_values': school_values,
            'news': news,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        home_features = get_object_or_404(HomeFeature)
        form = self.form_class(request.POST, request.FILES, instance=home_features)
        if form.is_valid():
            update_form_fields(form, HomeFeature)
            messages.success(request, 'Update Successful!!')
        return HttpResponseRedirect(reverse_lazy('home'))


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

    form_name = request.GET.get('form_name') # Get the name of the form
    if form_name == 'administrationForm':
        form_class = AdministrationForm
    elif form_name == 'academicForm':
        form_class = AcademicForm
    elif form_name == 'admissionForm':
        form_class = AdmissionForm
    elif form_name == 'curricularForm':
        form_class = CurricularForm
    elif form_name == 'schoolHistoryForm':
        form_class = SchoolHistoryForm
    elif form_name == 'schoolValueForm':
        form_class = SchoolValueForm
    else:
        form_class = SchoolInfoForm

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success!!')
        return HttpResponseRedirect('about')

    else:
        form = form_class(request.POST)

    context = {
        # 'academics': academics,
        # 'administration': administration,
        # 'admission': admission,
        # 'curriculars': curriculars,
        # 'school_virtues': school_virtues,
        # 'school_history': school_history,
        'staffs': staffs,
        'form': form,
    }
    return render(request, 'home/about.html', context)

def contact(request):
    return render(request, 'home/contact.html',{})
def message(request):
    principal = Message.objects.filter(author__role='Principal').get()
    deputy = Message.objects.filter(author__role='Deputy Principal').get()

    context={
        'principal': principal,
        'deputy': deputy
    }
    return render(request, 'home/message.html', context)
