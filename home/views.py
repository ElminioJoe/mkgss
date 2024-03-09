import json
import os
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    View,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    ListView,
)
from random import choice

from . import models
from .managers.queries import QueryManager
from .forms import *
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


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        entries = QueryManager.get_all_entries()
        carousel_images = QueryManager.get_carousel_images()
        latest_news_4 = QueryManager.get_news(4)

        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        context["carousel_images"] = carousel_images
        context["entries"] = None
        context["extras"] = entries.filter(entry="EXTRA")
        context["curricular"] = entries.filter(
            parent_entry=None, entry="CURRICULAR"
        ).first()
        context["message"] = entries.filter(parent_entry=None, entry="MESSAGE").first()
        context["school_history"] = entries.filter(
            parent_entry=None, entry="HISTORY"
        ).first()
        context["admin"] = entries.filter(
            parent_entry=None, entry="ADMINISTRATION"
        ).first()
        context["academic"] = entries.filter(
            parent_entry=None, entry="ACADEMIC"
        ).first()
        context["admission"] = entries.filter(
            parent_entry=None, entry="ADMISSION"
        ).first()
        context["school_motto"] = entries.filter(
            parent_entry=None, entry="PRINCIPLES"
        ).first()
        context["news"] = latest_news_4
        return context


class GalleryCategoryListView(ListView):
    model = models.Category
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
    model = models.Category
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


class AboutView(TemplateView):
    template_name = "home/about.html"

    def get_context_data(self, **kwargs):
        entries = QueryManager.get_all_entries()
        list_staff = QueryManager.get_all_teaching_staff()

        context = super().get_context_data(**kwargs)
        entry = self.kwargs.get("entry")
        context["title"] = "About"
        context["entry"] = entry
        context["academics"] = entries.filter(entry="ACADEMIC")
        context["admission"] = entries.filter(entry="ADMISSION")
        context["administration"] = entries.filter(entry="ADMINISTRATION")
        context["curricular"] = entries.filter(entry="CURRICULAR")
        context["principle"] = entries.filter(entry="PRINCIPLES")
        context["school_history"] = entries.filter(entry="HISTORY")
        context["staffs"] = list_staff
        return context


class NewsView(ListView):
    model = models.News
    template_name = "home/news.html"
    context_object_name = "news"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        recommended_news_5 = QueryManager.get_random_news()

        context = super().get_context_data(**kwargs)
        context["title"] = "Blog"
        context["recommended"] = recommended_news_5
        return context


class SchoolNewsDetailView(DetailView):
    model = None  # model will be set in the url
    template_name = None  # template name will be set in the url
    context_object_name = None

    def get_context_data(self, **kwargs):
        latest_news = QueryManager.get_news()

        context = super().get_context_data(**kwargs)
        news_item = context["news_item"]
        context["title"] = "Blog Detail"
        context["subtitle"] = news_item.headline
        context["news"] = latest_news.exclude(id=self.object.id)[:5]
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
        return context


class BaseEntryView(LoginRequiredMixin, SuccessMessageMixin):
    login_url = "/404/page-not-found/"
    redirect_field_name = None
    model = models.Entry
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
            return reverse_lazy("update_entry", args=[entry, self.object.slug])
        else:
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
            entry=self.kwargs.get("entry").capitalize(),
        )


class BaseNewsView(LoginRequiredMixin, SuccessMessageMixin):
    login_url = "/404/page-not-found/"
    redirect_field_name = None
    model = models.News
    form_class = NewsForm
    template_name = "home/forms/news_form.html"
    form_action = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_type = "news"
        context["news"] = news_type
        context["action"] = self.form_action
        context["title"] = f"{self.form_action} {news_type}"
        return context

    def get_success_url(self):
        if self.request.POST.get("add_another"):
            return reverse_lazy( "news_create")
        elif self.request.POST.get("save_continue"):
            return reverse_lazy("news_update", args=[self.object.slug])
        else:
            return reverse_lazy("news")


class CreateNewsView(BaseNewsView, CreateView):
    model = models.News
    template_name = "home/forms/news_form.html"
    success_message = "'%(headline)s' was created successfully"
    form_class = NewsForm
    form_action = "add"

    def form_valid(self, form):
        form.instance.publisher = models.Publisher.objects.get_or_create(
            pk=1, full_name="Admin", email="admin@mkghs.sc"
        )[0]
        return super(CreateNewsView, self).form_valid(form)


class UpdateNewsView(BaseNewsView, UpdateView):
    model = models.News
    success_message = "'%(headline)s' was updated successfully"
    form_class = NewsForm
    template_name = "home/forms/news_form.html"
    form_action = "update"


class DeleteNewsView(BaseNewsView, DeleteView):
    model = models.News
    template_name = "home/forms/confirm_news_delete_form.html"
    success_message = "'%(headline)s' was deleted successfully"
    form_action = "delete"
    form_class = EntryDeleteForm
    success_url = reverse_lazy("news")

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            self.get_object().__dict__,
        )


class SchoolManagementView(TemplateView):
    template_name = "home/management.html"

    def get_context_data(self, **kwargs):
        board_members = QueryManager.get_board_members()
        principals = QueryManager.get_principals().all()

        context = super().get_context_data(**kwargs)
        context["title"] = "Board of Management"
        context["principals"] = principals
        context["board_members"] = board_members

        return context


class BaseStaffView(LoginRequiredMixin, SuccessMessageMixin):
    login_url = "/404/page-not-found/"
    redirect_field_name = None
    model = models.Staff
    form_class = StaffForm
    template_name = "home/forms/staff_form.html"
    form_action = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_role = self.kwargs.get("role")
        context["role"] = staff_role
        context["action"] = self.form_action
        context["title"] = f"{self.form_action} {staff_role}"
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            role=self.kwargs.get("role").capitalize(),
        )

    def get_success_url(self):
        role = self.kwargs.get("role")
        if self.request.POST.get("add_another"):
            return reverse_lazy("create_staff", args=[role])
        elif self.request.POST.get("save_continue"):
            return reverse_lazy("update_staff", args=[role, self.object.slug])
        else:
            return f"/about/#tab_list-staff"


class CreateStaffView(BaseStaffView, CreateView):
    success_message = "%(role)s Details for '%(full_name)s' was created successfully"
    form_action = "add"
    error_message = """
        Action not Allowed!!
        It's not possible to add multiple instances of Principal or Deputy Principal
        """

    def form_valid(self, form):
        role = self.kwargs.get("role").upper()
        if role in ["PRINCIPAL", "DEPUTY"]:
            existing_roles = self.model.objects.filter(role__in=["PRINCIPAL", "DEPUTY"])
            if existing_roles.exists():
                messages.error(self.request, self.error_message)
                return self.form_invalid(form)

        form.instance.role = role
        return super(CreateStaffView, self).form_valid(form)


class UpdateStaffView(BaseStaffView, UpdateView):
    success_message = "Details for %(role)s '%(full_name)s' was updated successfully"
    form_action = "update"


class DeleteStaffView(BaseStaffView, DeleteView):
    template_name = "home/forms/confirm_staff_delete_form.html"
    success_message = "%(role)s '%(full_name)s' was deleted successfully"
    form_action = "delete"
    form_class = EntryDeleteForm
    error_message = """
        Action Not Allowed!!
        It's not possible to delete the Principal or Deputy Principal Objects.
        """

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.role in ["PRINCIPAL", "DEPUTY"]:
            messages.error(request, self.error_message)
            return self.render_to_response(self.get_context_data())
        return super().delete(request, *args, **kwargs)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            self.get_object().__dict__,
            role=self.kwargs.get("role").capitalize(),
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
        category = get_object_or_404(models.Category, id=category_id)

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
            gallery = models.Gallery(category=category, gallery_image=image)
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
        category = get_object_or_404(models.Category, id=self.kwargs.get("category_id"))
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
                gallery = models.Gallery(category=category, gallery_image=image)
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
