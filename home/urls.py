from django.urls import include, path, re_path, reverse_lazy
from django.views.generic import RedirectView

from .forms import *
from . import views, models

urlpatterns = [
    # ----------- Entry Urls -----------
    # path("entry/")
    path(
        "entry/",
        include(
            [
                path(
                    "add/<str:entry>/",
                    views.CreateEntryView.as_view(),
                    name="create_entry",
                ),
                path(
                    "update/<str:entry>/<slug:slug>/",
                    views.UpdateEntryView.as_view(),
                    name="update_entry",
                ),
                path(
                    "delete/<str:entry>/<slug:slug>/",
                    views.DeleteEntryView.as_view(),
                    name="delete_entry",
                ),
            ]
        ),
    ),
    # ----------- ---------- -----------
    path("", views.HomeView.as_view(), name="home"),
    path(
        "update_carousel_image/<int:pk>/",
        views.SchoolInfoUpdateView.as_view(
            model=models.CarouselImage,
            form_class=CarouselImageForm,
            template_name="home/forms/carousel_image_form.html",
            success_message="Carousel Image Updated!",
        ),
        name="update_carousel_image",
    ),
    # ----------- Gallery Urls -----------
    path("gallery/", views.GalleryCategoryListView.as_view(), name="gallery"),
    path(
        "gallery/<slug:slug>/",
        views.GalleryCategoryDetailView.as_view(),
        name="gallery-detail",
    ),
    path(
        "gallery/create/category/",
        views.CreateCategoryView.as_view(),
        name="create_category",
    ),
    path(
        "gallery/add/images/<int:category_id>/",
        views.AddImageView.as_view(),
        name="add_images",
    ),
    path(
        "gallery/delete/images/",
        views.images_delete,
        {
            "model": models.Gallery,
            "success_message": "Selected images have been deleted.",
        },
        name="image_delete",
    ),
    path(
        "gallery/delete/category/",
        views.images_delete,
        {
            "model": models.Category,
            "success_message": "Selected Categories have been deleted.",
        },
        name="category_delete",
    ),
    # ----------- ---------- -----------
    # ----------- About Urls -----------
    path(
        "about/<str:entry>/",
        RedirectView.as_view(pattern_name="about"),
        name="about_redirect",
    ),
    re_path(
        r"^about/(?:#tab_list-(?P<entry>)/)?$", views.AboutView.as_view(), name="about"
    ),
    path(
        "about/delete/curricular/<int:pk>/",
        views.SchoolInfoDeleteView.as_view(
            # model=models.Curricular,
            # success_url=reverse_lazy("about"),
            success_message="Curricular Details Deleted",
        ),
        name="curricular_delete",
    ),
    path(
        "about/create/staff/",
        views.SchoolInfoCreateView.as_view(
            model=models.Staff,
            form_class=StaffForm,
            template_name="home/forms/staff_form.html",
            success_message="Staff Details Added",
        ),
        name="staff_create",
    ),
    path(
        "about/update/staff/<int:pk>/",
        views.SchoolInfoUpdateView.as_view(
            model=models.Staff,
            form_class=StaffForm,
            template_name="home/forms/staff_form.html",
            success_message="Staff Details Updated",
        ),
        name="staff_update",
    ),
    path(
        "about/delete/staff/<int:pk>/",
        views.SchoolInfoDeleteView.as_view(
            model=models.Staff,
            # success_url=reverse_lazy("about"),
            success_message="Staff Details Deleted",
        ),
        name="staff_delete",
    ),
    path(
        "news/",
        include(
            [
                path("", views.NewsView.as_view(), name="news"),
                path(
                    "<slug:slug>/",
                    views.SchoolNewsDetailView.as_view(
                        model=models.News,
                        template_name="home/news_detail.html",
                        context_object_name="news_item",
                    ),
                    name="news-detail",
                ),
                path(
                    "create/article",
                    views.CreateNewsView.as_view(),
                    name="news_create",
                ),
                path(
                    "update/article/<slug:slug>/",
                    views.UpdateNewsView.as_view(),
                    name="news_update",
                ),
                path(
                    "delete/article/<slug:slug>/",
                    views.DeleteNewsView.as_view(),
                    name="news_delete",
                ),
            ]
        )
    ),
    path("contact/", views.ContactFormView.as_view(), name="contact"),
    # ----------- ---------- -----------
    # ----- Staff & Management Urls ------
    path(
        "management/",
        include(
            [
                path("", views.SchoolManagementView.as_view(), name="management"),
                path(
                    "add/<str:role>/",
                    views.CreateStaffView.as_view(),
                    name="create_staff",
                ),
                path(
                    "update/<str:role>/<slug:slug>/",
                    views.UpdateStaffView.as_view(),
                    name="update_staff",
                ),
                path(
                    "delete/<str:role>/<slug:slug>/",
                    views.DeleteStaffView.as_view(),
                    name="delete_staff",
                ),
            ]
        ),
    ),
]
