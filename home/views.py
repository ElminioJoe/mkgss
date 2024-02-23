import json
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    View,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    ListView,
)
from random import choice

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
            # create_home_feature_objects()
            return

        carousel_images = CarouselImage.objects.order_by("date_created")

        news = News.objects.order_by("-post_date")[:4]

        context = {
            "title": "Home",
            "carousel_images": carousel_images,
            "home_features": home_features,
            "schl_info": None,
            "school_history": None,
            "admission": None,
            "school_values": None,
            "news": news,
        }
        return render(request, self.template_name, context)


class GalleryCategoryListView(ListView):
    model = Category
    template_name = "home/gallery.html"
    context_object_name = "category_list"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Gallery"
        for category in context["category_list"]:
            images = category.images.all()
            if images.exists():
                category.random_image = choice(images)
        return context


class GalleryCategoryDetailView(DetailView):
    model = Category
    template_name = "home/gallery_detail.html"
    context_object_name = "category"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context["category"]
        context["title"] = "Gallery Detail"
        context["subtitle"] = category.name
        context["images"] = category.images.all()

        return context


class AboutView(View):
    template_name = "home/about.html"

    def get(self, request, *args, **kwargs):
        # create_school_info_objects()

        academics = Entry.academic_entries.all().exclude(is_deleted=True)
        admission = Entry.admission_entries.all().exclude(is_deleted=True)
        administration = Entry.administration_entries.all().exclude(is_deleted=True)
        curriculars = Entry.curricular_entries.all().exclude(is_deleted=True)
        school_values = Entry.principles_entries.all()
        school_history = Entry.history_entries.all()
        staffs = Staff.objects.all()

        context = {
            "title": "About",
            "academics": academics,
            "administration": administration,
            "admission": admission,
            "curriculars": curriculars,
            "school_values": school_values,
            "school_history": school_history,
            "staffs": staffs,
        }
        return render(request, self.template_name, context)


class NewsView(ListView):
    model = News
    template_name = "home/news.html"
    context_object_name = "news"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Blog"
        context["recommended"] = News.random_data.all()[:5]

        return context


class SchoolNewsDetailView(DetailView):
    model = None  # model will be set in the url
    template_name = None  # template name will be set in the url
    context_object_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_item = context["news_item"]
        context["title"] = "Blog Detail"
        context["subtitle"] = news_item.headline
        context["news"] = News.objects.order_by("-post_date").exclude(
            id=self.object.id
        )[:5]
        context["template_name"] = self.template_name
        return context


class SchoolInfoCreateView(CreateView):
    model = None  # model will be set in the url
    form_class = None  # form class will be set in the url
    template_name = None  # template name will be set in the url
    # success_url = reverse_lazy('about')
    success_message = None

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(SchoolInfoCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(SchoolInfoCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        # context["template_name"] = self.template_name
        return context


class BaseEntryView(LoginRequiredMixin, SuccessMessageMixin):
    login_url = "/404/not-found/"
    redirect_field_name = None
    model = Entry
    form_class = EntryForm
    template_name = "home/forms/entry_form.html"
    form_action = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry_type = self.kwargs.get("entry")
        context["entry"] = entry_type
        context["action"] = self.form_action
        context["title"] = f"{self.form_action} {entry_type} entries"
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            entry=self.kwargs.get("entry").capitalize(),
        )

    def get_success_url(self):
        entry = self.kwargs.get("entry")
        if self.request.POST.get("add_another"):
            return reverse_lazy("create_entry", args=[entry])
        elif self.request.POST.get("save_continue"):
            return reverse_lazy("update_entry", args=[entry, self.object.id])
        else:
            # return reverse_lazy("about", kwargs={"entry": entry})
            return f"/about/#tab_list-{entry}"


class CreateEntryView(BaseEntryView, CreateView):
    success_message = "%(entry)s Entry '%(title)s' was created successfully"
    form_action = "add"

    def form_valid(self, form):
        form.instance.entry = self.kwargs.get("entry").upper()
        return super(CreateEntryView, self).form_valid(form)


class UpdateEntryView(BaseEntryView, UpdateView):
    success_message = "%(entry)s Entry '%(title)s' was updated successfully"
    form_action = "update"


class DeleteEntryView(BaseEntryView, DeleteView):
    template_name = "home/forms/confirm_entry_delete_form.html"
    success_message = "%(entry)s Entry '%(title)s' was deleted successfully"
    form_action = "delete"
    form_class = EntryDeleteForm
    # context_object_name = "entry"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            self.get_object().__dict__,
            entry = self.kwargs.get("entry").capitalize(),
        )


class SchoolInfoUpdateView(UpdateView):
    model = None  # model will be set in the url
    form_class = None  # form class will be set in the url
    template_name = None  # template name will be set in the url
    # success_url = reverse_lazy('about')
    success_message = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        form = self.form_class(self.request.POST or None, instance=self.object)
        context["form"] = form
        # context["template_name"] = self.template_name
        return context

    def form_valid(self, form):
        update_form_fields(form, self.model)
        messages.success(self.request, self.success_message)
        return super(SchoolInfoUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(SchoolInfoUpdateView, self).form_invalid(form)


class SchoolInfoDeleteView(DeleteView):
    model = None  # model will be set in the url
    template_name = "home/forms/confirm_delete_form.html"
    success_url = None
    success_message = None

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ContactFormView(View):
    template_name = "home/contact.html"
    # success_url = "/contact/"

    def get(self, request):
        form = ContactForm(initial=request.POST)
        return render(
            request, self.template_name, {"form": form, "title": "Contact Us"}
        )

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            name = sanitize_input(form.cleaned_data.get("name"))
            email = form.cleaned_data.get("email")
            subject = sanitize_input(form.cleaned_data.get("subject"))
            message = sanitize_input(form.cleaned_data.get("message"))

            # Perform additional validation
            if not all([name, email, subject, message]):
                messages.error(request, "Please fill in all fields.")
            elif not validate_email(email):
                messages.error(request, "Invalid Email Address.")
            else:
                host_email_address = os.environ.get("EMAIL_HOST_USER")
                send_mail(subject, message, email, [host_email_address])
                messages.info(
                    self.request, "Your message has been delivered Successfully."
                )
                # Clear the form values after successful submission
                form = ContactForm()
        else:
            messages.error(request, "Form submission is invalid.")

        return render(
            request, self.template_name, {"form": form, "title": "Contact Us"}
        )


class AddImageView(FormView):
    template_name = "home/forms/gallery_upload_form.html"
    form_class = AddImageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image_formset"] = self.form_class
        context["errors"] = self.form_class.non_field_errors
        return context

    def form_valid(self, form):
        category_id = self.kwargs.get("category_id")
        category = get_object_or_404(Category, id=category_id)

        # Handle renaming category and description
        rename_category = form.cleaned_data.get("rename_category")
        new_category_name = form.cleaned_data.get("new_category_name")
        rename_description = form.cleaned_data.get("rename_description")
        new_description = form.cleaned_data.get("new_description")

        if rename_category and new_category_name:
            category.name = new_category_name
            category.save()

        if rename_description and new_description:
            category.description = new_description
            category.save()

        # Create image objects for each uploaded images
        images = self.request.FILES.getlist("gallery_image")
        for image in images:
            gallery = Gallery(category=category, gallery_image=image)
            gallery.save()
        messages.success(self.request, "Images Added successfully!")
        return super(AddImageView, self).form_valid(form)

    def form_invalid(self, form):
        # Add form errors to messages framework
        errors = form.non_field_errors()
        for error in errors:
            messages.error(self.request, error)

        return super().form_invalid(form)

    def get_success_url(self):
        category = get_object_or_404(Category, id=self.kwargs.get("category_id"))
        return reverse_lazy("gallery-detail", kwargs={"slug": category.slug})


class CreateCategoryView(FormView):
    template_name = "home/forms/gallery_upload_form.html"
    form_class = CreateGalleryForm
    success_url = "/gallery/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image_formset"] = self.form_class
        context["errors"] = self.form_class.non_field_errors
        return context

    def form_valid(self, form):
        category = form.save(commit=False)
        category_image = self.request.FILES.getlist("category_image")

        # Associate the uploaded image with the category
        if category_image:
            category.save()  # Save the category first to generate the ID

            # Create image objects for each uploaded image
            for image in category_image:
                gallery = Gallery(category=category, gallery_image=image)
                gallery.save()

        messages.success(self.request, "Gallery Added successfully!")
        self.request.session["new_category_id"] = category.id
        return super(CreateCategoryView, self).form_valid(form)


def images_delete(request, model, success_message):
    if request.method == "POST":
        action = request.POST.get("action")
        selected_image_ids = request.POST.get("selected_images", [])
        category_slug = request.POST.get("category_slug")

        if action == "delete_selected_images":
            selected_image_ids = json.loads(selected_image_ids)
            images = model.objects.filter(id__in=selected_image_ids)
            if images:
                # category_id = images.first().category.id
                images.delete()
                messages.success(request, success_message)

                if category_slug:
                    return redirect("gallery-detail", slug=category_slug)
                else:
                    return redirect("gallery")
            else:
                messages.error(request, "Please select at least one image to delete.")

    if category_slug:
        return redirect("gallery-detail", slug=category_slug)
    else:
        return redirect("gallery")
