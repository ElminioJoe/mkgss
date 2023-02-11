from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, CreateView, UpdateView, DeleteView, FormView

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
        home_features = get_object_or_404(HomeFeature)
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


def gallery(request):
    # image_categories = Category.objects.all()
    images = Gallery.objects.all()

    context = {
        # 'image_categories': image_categories,
        "images": images,
    }
    return render(request, "home/gallery.html", context)


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


class SchoolInfoDetailView(DetailView):
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
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        context["template_name"] = self.template_name
        return context


class SchoolInfoUpdateView(UpdateView):
    model = None  # model will be set in the url
    form_class = None  # form class will be set in the url
    template_name = None  # template name will be set in the url
    # success_url = reverse_lazy('about')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST or None, instance=self.object)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def form_valid(self, form):
        update_form_fields(form, self.model)
        messages.success(self.request, "Success! Details Updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] = self.form_class
        context["template_name"] = self.template_name
        return context


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

    def get(self, request, *args, **kwargs):
        image_formset = self.form_class()
        # category_form = CategoryForm()

        context = {
            "image_formset": image_formset,
            # "category_form": category_form
        }
        return render(request, self.template_name, context )

    def post(self, request, *args, **kwargs):
        image_formset = self.form_class(request.POST, request.FILES)
        images = request.FILES.getlist('gallery_image')

        if image_formset.is_valid():
            category = image_formset.cleaned_data.get("category")

            if isinstance(category, Category):
                for image in images:
                    gallery = Gallery(category=category, gallery_image=image)
                    gallery.save()
            else:
                created_category = image_formset.cleaned_data.get('create_category')
                description = image_formset.cleaned_data.get('description')
                category = Category.objects.create(name=created_category, description=description)
                for image in images:
                    gallery = Gallery(category=category, gallery_image=image)
                    gallery.save()
            messages.success(request, "Images uploaded successfully!")
            return super().form_valid(image_formset)

        else:
            return self.form_invalid(image_formset)


    # def post(self, request, *args, **kwargs):
    #     image_formset = self.form_class(request.POST, request.FILES)
    #     category_form = CategoryForm(request.POST)
    #     images = request.FILES.getlist('gallery_image')
    #     if image_formset.is_valid() and category_form.is_valid():
    #         category_name = request.POST.get("category")
    #         if not image_formset.data["category"] and not category_form.data["name"]:
    #             image_formset.add_error("category", "Please select or create a category")
    #         # Check if the user selected an existing category or created a new one
    #         elif category_name:
    #             category, created = Category.objects.get_or_create(name=category_name)
    #         else:
    #             category = category_form.save()

    #         for image in images:
    #             gallery = Gallery(category=category, gallery_image=image)
    #             gallery.save()
    #         messages.success(request, "Images uploaded successfully!")
    #         return HttpResponseRedirect(self.success_url)

    #     else:

    #         self.form_invalid(image_formset)
