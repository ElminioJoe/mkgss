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
        return models.Entry.objects.exclude(is_deleted=True)

    @staticmethod
    def get_carousel_images():
        """
        Fetch all carousel images ordered by date_created.
        """
        return models.CarouselImage.objects.order_by("date_created")

    @staticmethod
    def get_all_teaching_staff():
        """
        Fetch all staff objects.
        """
        return models.Staff.objects.filter(
            Q(role__in=[models.Staff.HEAD_OF_DEPARTMENT])
            | Q(role__in=[models.Staff.TEACHING_STAFF])
        )

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

    @staticmethod
    def get_principals():
        """
        Fetch the Principal and Deputy principal objects
        """
        return models.Staff.objects.filter(
            Q(role__in=[models.Staff.PRINCIPAL])
            | Q(role__in=[models.Staff.DEPUTY])
            | Q(role__in=[models.Staff.ADMINISTRATOR])
        )

    @staticmethod
    def get_board_members():
        """
        Fetch all Board of Management objects.
        """
        return models.Staff.objects.filter(
                role=models.Staff.DIRECTOR
            )
