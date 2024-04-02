"""kadzonzo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin-panel/", admin.site.urls),
    path("", include("home.urls")),
    path("authentication/", include("user_auth.urls")),
    path(
        "ckeditor5/", include("django_ckeditor_5.urls"),
        name="ck_editor_5_upload_file"
    ),
]

admin.site.site_header = "Moi Kadzonzo Girls Secondary School "
admin.site.site_title = f"{admin.site.site_header}"
# admin.site.index_title = ""

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
else:
    urlpatterns+= re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
