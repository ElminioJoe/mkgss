from django.db.models import Q

from .. import models


class QueryManager:
    """
    A class to manage commonly used queries.
    """

    @staticmethod
    def get_all_entries():
        """
        Fetch all non-deleted entries.
        """
        return models.Entry.objects.filter(
            Q(entry__in=["ACADEMIC", "ADMISSION", "ADMINISTRATION", "CURRICULAR"])
            | Q(entry__in=["PRINCIPLES", "HISTORY", "MESSAGE", "EXTRA"])
        ).exclude(is_deleted=True)

    @staticmethod
    def get_carousel_images():
        """
        Fetch all carousel images ordered by date_created.
        """
        return models.CarouselImage.objects.order_by("date_created")

    @staticmethod
    def get_all_staff():
        """
        Fetch all staff objects.
        """
        return models.Staff.objects.all()

    @staticmethod
    def get_news(count=None):
        """
        Fetch news objects with a specified count or all news objects if count is None.
        """
        if count is None:
            return models.News.objects.all()
        else:
            return models.News.objects.all()[:count]

    @staticmethod
    def get_random_news(count=5):
        """
        Fetch random news objects with a specified count.
        """
        return models.News.random_data.all()[:count]
