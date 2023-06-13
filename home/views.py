from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, CreateView, UpdateView, DeleteView, FormView, ListView

from .models import *
from .forms import *
from .data import create_school_info_objects, create_home_feature_objects
from .validators import validate_email, sanitize_input
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
            create_home_feature_objects()
            return

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

        context = {
            "images": images,
        }
        return render(request, self.template_name, context)


class AboutView(View):
    template_name = "home/about.html"

    def get(self, request, *args, **kwargs):
        create_school_info_objects()

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
        recommended = News.random_data.all()[:6]

        context = {
            "news": news,
            "recommended": recommended,
        }
        return render(request, self.template_name, context)


class SchoolNewsDetailView(DetailView):
    model = None  # model will be set in the url
    template_name = None  # template name will be set in the url
    context_object_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news"] = News.objects.order_by("-post_date").exclude(id=self.object.id)[:8]
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


class ContactFormView(View):
    template_name = "home/contact.html"
    # success_url = "/contact/"

    def get(self, request):
        form = ContactForm(initial=request.POST)
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            name = sanitize_input(form.cleaned_data.get('name'))
            email = form.cleaned_data.get('email')
            subject = sanitize_input(form.cleaned_data.get('subject'))
            message = sanitize_input(form.cleaned_data.get('message'))

            # Perform additional validation
            if not all([name, email, subject, message]):
                messages.error(request, 'Please fill in all fields.')
            elif not validate_email(email):
                messages.error(request, 'Invalid Email Address.')
            else:
                host_email_address = os.environ.get('EMAIL_HOST_USER')
                send_mail(subject, message, email, [host_email_address])
                messages.info(self.request, 'Your message has been delivered Successfully.')
                # Clear the form values after successful submission
                form = ContactForm()
        else:
            messages.error(request, 'Form submission is invalid.')

        return render(request, self.template_name, {'form': form})

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
