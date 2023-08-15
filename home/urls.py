from django.urls import path
from .forms import *
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("update_carousel_image/<int:pk>/", views.SchoolInfoUpdateView.as_view(
            model=CarouselImage,
            form_class=CarouselImageForm,
            template_name="home/forms/carousel_image_form.html",
        ),
        name="update_carousel_image"),
    path(
        "features/update/<int:pk>/",
        views.SchoolInfoUpdateView.as_view(
            model=HomeFeature,
            form_class=HomeFeatureForm,
            template_name="home/forms/home_features_form.html",
        ),
        name="home_features_update",
    ),
    path("gallery/", views.GalleryCategoryListView.as_view(), name="gallery"),
    path("gallery/<slug:slug>/", views.GalleryCategoryDetailView.as_view(), name='gallery-detail'),
    path("gallery/create/category/",views.CreateCategoryView.as_view(), name="create_category"),
    path("gallery/add/images/<int:category_id>/",views.AddImageView.as_view(), name="add_images"),
    path("gallery/delete/images/", views.images_delete, {'model': Gallery, 'success_message': 'Selected images have been deleted.'}, name="image_delete"),
    path("gallery/delete/category/", views.images_delete, {'model': Category, 'success_message': 'Selected Categories have been deleted.'}, name="category_delete"),
    path("about/", views.AboutView.as_view(), name="about"),
    path(
        "about/create/administration/",
        views.SchoolInfoCreateView.as_view(
            model=Administration,
            form_class=AdministrationForm,
            template_name="home/forms/administration_form.html",
        ),
        name="administration_create",
    ),
    path(
        "about/update/administration/<int:pk>/",
        views.SchoolInfoUpdateView.as_view(
            model=Administration,
            form_class=AdministrationForm,
            template_name="home/forms/administration_form.html",
        ),
        name="administration_update",
    ),
    path(
        "about/delete/administration/<int:pk>/",
        views.SchoolInfoDeleteView.as_view(
            model=Administration, success_url=reverse_lazy("about")
        ),
        name="administration_delete",
    ),
    path(
        "about/update/admission/<int:pk>/",
        views.SchoolInfoUpdateView.as_view(
            model=Admission,
            form_class=AdmissionForm,
            template_name="home/forms/admission_form.html",
        ),
        name="admission_update",
    ),
    path(
        "about/create/academic/",
        views.SchoolInfoCreateView.as_view(
            model=Academic,
            form_class=AcademicForm,
            template_name="home/forms/academic_form.html",
        ),
        name="academic_create",
    ),
    path(
        "about/update/academic/<int:pk>/",
        views.SchoolInfoUpdateView.as_view(
            model=Academic,
            form_class=AcademicForm,
            template_name="home/forms/academic_form.html",
        ),
        name="academic_update",
    ),
    path(
        "about/delete/academic/<int:pk>/",
        views.SchoolInfoDeleteView.as_view(model=Academic, success_url=reverse_lazy("about")),
        name="academic_delete",
    ),
    path(
        "about/create/curricular/",
        views.SchoolInfoCreateView.as_view(
            model=Curricular,
            form_class=CurricularForm,
            template_name="home/forms/curricular_form.html",
        ),
        name="curricular_create",
    ),
    path(
        "about/update/curricular/<int:pk>/",
        views.SchoolInfoUpdateView.as_view(
            model=Curricular,
            form_class=CurricularForm,
            template_name="home/forms/curricular_form.html",
        ),
        name="curricular_update",
    ),
    path(
        "about/delete/curricular/<int:pk>/",
        views.SchoolInfoDeleteView.as_view(
            model=Curricular, success_url=reverse_lazy("about")
        ),
        name="curricular_delete",
    ),
    path(
        "about/update/school_history/<int:pk>/",
        views.SchoolInfoUpdateView.as_view(
            model=SchoolHistory,
            form_class=SchoolHistoryForm,
            template_name="home/forms/school_history_form.html",
        ),
        name="school_history_update",
    ),
    path(
        "about/update/school_value/<int:pk>/",
        views.SchoolInfoUpdateView.as_view(
            model=SchoolValue,
            form_class=SchoolValueForm,
            template_name="home/forms/school_value_form.html",
        ),
        name="school_value_update",
    ),
    path(
        "about/create/staff/",
        views.SchoolInfoCreateView.as_view(
            model=Staff,
            form_class=StaffForm,
            template_name="home/forms/staff_form.html",
        ),
        name="staff_create",
    ),
    path(
        "about/update/staff/<int:pk>/",
        views.SchoolInfoUpdateView.as_view(
            model=Staff,
            form_class=StaffForm,
            template_name="home/forms/staff_form.html",
        ),
        name="staff_update",
    ),
    path(
        "about/delete/staff/<int:pk>/",
        views.SchoolInfoDeleteView.as_view(model=Staff, success_url=reverse_lazy("about")),
        name="staff_delete",
    ),
    path("news/", views.NewsView.as_view(), name="news"),
    path(
        "news/<slug:slug>/",
        views.SchoolNewsDetailView.as_view(
            model=News,
            template_name="home/news_detail.html",
            context_object_name = "news_item"
        ),
        name="news-detail"),
    path(
        "news/create/article",
        views.SchoolInfoCreateView.as_view(
            model=News,
            form_class=NewsForm,
            template_name="home/forms/news_form.html",
        ),
        name="news_create",
    ),
    path(
        "news/update/article/<int:pk>/",
        views.SchoolInfoUpdateView.as_view(
            model=News,
            form_class=NewsForm,
            template_name="home/forms/news_form.html",
        ),
        name="news_update",
    ),
    path(
        "news/delete/article/<int:pk>/",
        views.SchoolInfoDeleteView.as_view(model=News, success_url=reverse_lazy("news")),
        name="news_delete",
    ),
    path("contact/", views.ContactFormView.as_view(), name="contact"),
]
