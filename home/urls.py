from django.urls import include, path, re_path, reverse_lazy
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
                    "update/<str:entry>/<int:pk>/",
                    views.UpdateEntryView.as_view(),
                    name="update_entry",
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
    path(
        "features/update/<int:pk>/",
        views.SchoolInfoUpdateView.as_view(
            model=models.HomeFeature,
            form_class=HomeFeatureForm,
            template_name="home/forms/home_features_form.html",
            success_message="Homepage Hero Details Updated",
        ),
        name="home_features_update",
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
    re_path(
        "about/(?:#tab_list-(?P<entry>)/)?$", views.AboutView.as_view(), name="about"
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
    path("news/", views.NewsView.as_view(), name="news"),
    path(
        "news/<slug:slug>/",
        views.SchoolNewsDetailView.as_view(
            model=models.News,
            template_name="home/news_detail.html",
            context_object_name="news_item",
        ),
        name="news-detail",
    ),
    path(
        "news/create/article",
        views.SchoolInfoCreateView.as_view(
            model=models.News,
            form_class=NewsForm,
            template_name="home/forms/news_form.html",
            success_message="Blog Post Added",
        ),
        name="news_create",
    ),
    path(
        "news/update/article/<int:pk>/",
        views.SchoolInfoUpdateView.as_view(
            model=models.News,
            form_class=NewsForm,
            template_name="home/forms/news_form.html",
            success_message="Blog Post Updated",
        ),
        name="news_update",
    ),
    path(
        "news/delete/article/<int:pk>/",
        views.SchoolInfoDeleteView.as_view(
            model=models.News,
            success_url=reverse_lazy("news"),
            success_message="Blog Post Deleted",
        ),
        name="news_delete",
    ),
    path("contact/", views.ContactFormView.as_view(), name="contact"),
    # ----------- ---------- -----------
]
