from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Category
from .managers.queries import QueryManager


class StaticViewSitemap(Sitemap):
    priority = 1
    changefreq = "daily"

    def items(self):
        return [
            "home",
            "about",
            "management",
            "gallery",
            "news",
            "job-listing",
            "contact",
        ]

    def location(self, item):
        return reverse(item)


class AboutSiteMap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return [
            "academic",
            "administration",
            "admission",
            "curricular",
            "principles",
            "history",
            "staff",
        ]

    def location(self, item):
        return f"/about/#tab_list-{item}"


class BlogsSiteMap(Sitemap):
    """
    Generate sitemap for the Blogs

    """

    changefreq = "daily"
    priority = 0.5

    def items(self):
        return QueryManager.get_news()

    def lastmod(self, item):
        """
        Return the last modification date for the given object.
        """
        return getattr(item, "last_modified", None)


class JoblistingsSiteMap(Sitemap):
    """
    Generate sitemap for the JobListing

    """

    changefreq = "daily"
    priority = 0.5

    def items(self):
        return QueryManager.get_open_job_listing()

    def lastmod(self, item):
        """
        Return the last modification date for the given object.
        """
        return getattr(item, "date_listed", None)


class GallerySiteMap(Sitemap):
    """
    Generate sitemap for the Gallery

    """

    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def lastmod(self, item):
        """
        Return the last modification date for the given object.
        """
        return getattr(item, "date_modified", None)
