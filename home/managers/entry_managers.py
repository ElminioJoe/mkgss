from django.db import models
from django.db.models.query import QuerySet


class AdministrationEntryManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(entry="ADMINISTRATION")


class AdmissionEntryManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(entry="ADMISSIONS")


class AcademicEntryManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(entry="ACADEMIC")


class CurricularEntryManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(entry="CURRICULAR")


class HistoryEntryManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(entry="HISTORY")


class PrinciplesEntryManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(entry="PRINCIPLES")