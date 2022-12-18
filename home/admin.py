from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from .models import *

# Register your models here.

class SchoolInfoChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = SchoolInfo  # Optional, explicitly set here.


@admin.register(Administration)
class AdministrationoAdmin(SchoolInfoChildAdmin):
    base_model = Administration  # Explicitly set here!
    show_in_index = True  # makes child model admin visible in main admin site


@admin.register(Admission)
class AdmissionAdmin(SchoolInfoChildAdmin):
    base_model = Admission  # Explicitly set here!
    show_in_index = True  # makes child model admin visible in main admin site


@admin.register(Academic)
class AcademicAdmin(SchoolInfoChildAdmin):
    base_model = Academic  # Explicitly set here!
    show_in_index = True  # makes child model admin visible in main admin site


@admin.register(Curricular)
class CurricularAdmin(SchoolInfoChildAdmin):
    base_model = Curricular  # Explicitly set here!
    show_in_index = True  # makes child model admin visible in main admin site


@admin.register(SchoolHistory)
class SchoolHistoryAdmin(SchoolInfoChildAdmin):
    base_model = SchoolHistory  # Explicitly set here!
    show_in_index = True  # makes child model admin visible in main admin site

@admin.register(SchoolValue)
class SchoolValueAdmin(SchoolInfoChildAdmin):
    base_model = SchoolValue  # Explicitly set here!
    show_in_index = True  # makes child model admin visible in main admin site

@admin.register(SchoolInfo)
class SchoolInfoAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = SchoolInfo  # Optional, explicitly set here.
    child_models = (Administration, Admission, Academic, Curricular, SchoolHistory, SchoolValue)


admin.site.register(HomeFeature)
admin.site.register(Publisher)
admin.site.register(Staff)
admin.site.register(Department)
admin.site.register(Message)
# admin.site.register(Academic)
# admin.site.register(Administration)
# admin.site.register(Curricular)
# admin.site.register(Admission)
# admin.site.register(SchoolHistory)
# admin.site.register(SchoolValue)
admin.site.register(Gallery)
admin.site.register(Category)
admin.site.register(News)

