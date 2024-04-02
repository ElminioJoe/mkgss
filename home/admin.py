from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.CarouselImage)
admin.site.register(models.Publisher)
admin.site.register(models.Staff)
admin.site.register(models.Department)
admin.site.register(models.Gallery)
admin.site.register(models.Category)
admin.site.register(models.News)
admin.site.register(models.JobListing)


class EntryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "entry",
        "parent_entry",
        "is_deleted",
        "date_created",
        "date_modified",
    )
    list_filter = (
        "entry",
        "parent_entry",
        "is_deleted",
        "date_created",
        "date_modified",
    )


admin.site.register(models.Entry, EntryAdmin)
