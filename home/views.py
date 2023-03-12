from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, CreateView, UpdateView, DeleteView, FormView, ListView

from .models import *
from .forms import *

# Create your views here.


def update_form_fields(form, model):
    "Check and update changed form fields"
    update_fields = {}
    for field in form.changed_data:
        "only add non-blank fields to the update_fields dictionary"
        if form.cleaned_data[field]:
            update_fields[field] = form.cleaned_data[field]
    model.objects.filter(pk=form.instance.pk).update(**update_fields)


class HomeView(View):
    template_name = "home/home.html"

    def get(self, request, *args, **kwargs):
        try:
            home_features = HomeFeature.objects.get()
        except HomeFeature.DoesNotExist:
            home_features = HomeFeature.objects.create(
                welcome_info="Welcome to Moi Kadzonzo Girls High School website. It is designed for parents, students, Alumni, staff, sponsors, friends of the school and prospective parents who may know little about us.",
                administration_info="Meet our team of experienced professionals who manage and lead our organization. Our administration is dedicated to providing the best possible service to our clients and stakeholders.",
                academics_info="Our educational programs are designed to prepare students for success in their chosen careers. We offer a wide range of courses and programs, from technical training to liberal arts and sciences.",
                staff_info="Our staff is made up of dedicated and talented individuals who are committed to providing excellent service to our clients and customers. They bring a wealth of experience and expertise to their roles, ensuring that we deliver the highest quality work.",
                curricular_info="Our curricular activities are designed to provide students with opportunities to explore their interests, develop new skills, and build relationships with peers. We offer a wide range of activities, from sports teams and clubs to music and theater programs.",
                library_info="Our library is a vital resource for students and researchers, providing access to a wide range of books, journals, and digital resources. Our knowledgeable staff is available to assist with research and information inquiries.",
                alumni_info="Our alumni are an important part of our community, and we are proud of their accomplishments and contributions. We maintain strong relationships with our alumni, providing opportunities for networking, professional development, and social events."
        )
            
        schl_info = SchoolInfo.objects.select_subclasses(
            Admission, SchoolValue, SchoolHistory
        )
        school_history = [info for info in schl_info if isinstance(info, SchoolHistory)]
        admission = [info for info in schl_info if isinstance(info, Admission)]
        school_values = [info for info in schl_info if isinstance(info, SchoolValue)]
        news = News.objects.order_by("-post_date")[:4]

        context = {
            "home_features": home_features,
            "schl_info": schl_info,
            "school_history": school_history,
            "admission": admission,
            "school_values": school_values,
            "news": news,
        }
        return render(request, self.template_name, context)


class GalleryView(View):
    template_name = "home/gallery.html"

    def get(self, request, *args, **kwargs):
        images = Gallery.objects.all().order_by("category")
        image = images.first()

        context = {
            # "categories": categories,
            "images": images,
            "image": image,
        }
        return render(request, self.template_name, context)


class AboutView(View):
    template_name = "home/about.html"

    def get(self, request, *args, **kwargs):
        school_info = SchoolInfo.objects.select_subclasses()
        academics = [info for info in school_info if isinstance(info, Academic)]
        admission = [info for info in school_info if isinstance(info, Admission)]
        administration = [
            info for info in school_info if isinstance(info, Administration)
        ]
        curriculars = [info for info in school_info if isinstance(info, Curricular)]
        school_values = [info for info in school_info if isinstance(info, SchoolValue)]
        school_history = [
            info for info in school_info if isinstance(info, SchoolHistory)
        ]
        staffs = Staff.objects.all()

        context = {
            "academics": academics,
            "administration": administration,
            "admission": admission,
            "curriculars": curriculars,
            "school_values": school_values,
            "school_history": school_history,
            "staffs": staffs,
        }
        return render(request, self.template_name, context)


class NewsView(View):
    template_name = "home/news.html"

    def get(self, request):
        news = News.objects.order_by("-post_date")[:4]

        context = {
            "news": news,
        }
        return render(request, self.template_name, context)


class SchoolNewsDetailView(DetailView):
    model = None  # model will be set in the url
    template_name = None  # template name will be set in the url
    context_object_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news"] = News.random_data.exclude(id=self.object.id)[:8]
        context["template_name"] = self.template_name
        return context


class SchoolInfoCreateView(CreateView):
    model = None  # model will be set in the url
    form_class = None  # form class will be set in the url
    template_name = None  # template name will be set in the url
    # success_url = reverse_lazy('about')

    def form_valid(self, form):
        messages.success(self.request, "Success! The form has been submitted.")
        return super(SchoolInfoCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(SchoolInfoCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        # context["template_name"] = self.template_name
        return context


class SchoolInfoUpdateView(UpdateView):
    model = None  # model will be set in the url
    form_class = None  # form class will be set in the url
    template_name = None  # template name will be set in the url
    # success_url = reverse_lazy('about')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        form = self.form_class(self.request.POST or None, instance=self.object)
        context['form'] = form
        # context["template_name"] = self.template_name
        return context

    def form_valid(self, form):
        update_form_fields(form, self.model)
        messages.success(self.request, "Success! Details Updated.")
        return super(SchoolInfoUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(SchoolInfoUpdateView, self).form_invalid(form)


class SchoolInfoDeleteView(DeleteView):
    model = None  # model will be set in the url
    template_name = "home/forms/confirm_delete_form.html"
    success_url = None

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Deleted!!.")
        return super().delete(request, *args, **kwargs)


def contact(request):
    return render(request, "home/contact.html", {})


class GalleryUploadView(FormView):
    template_name = 'home/forms/gallery_upload_form.html'
    form_class = GalleryForm
    success_url = '/gallery/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image_formset"] = self.form_class
        context["errors"] = self.form_class.non_field_errors
        return context

    def form_valid(self, form):
        # Create category object if user entered a new category name
        category_name = form.cleaned_data["create_category"]
        description = form.cleaned_data["description"]

        if category_name:
            category = Category.objects.create(name=category_name, description=description)
        else:
            category = form.cleaned_data['category']

        # Create image objects for each uploaded images
        images = self.request.FILES.getlist('gallery_image')
        for image in images:
            gallery = Gallery(category=category, gallery_image=image)
            gallery.save()
        messages.success(self.request, "Images uploaded successfully!")
        return super(GalleryUploadView, self).form_valid(form)

    def form_invalid(self, form):
        return super(GalleryUploadView, self).form_invalid(form)

