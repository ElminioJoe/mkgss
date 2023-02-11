from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Category

def validate_category(value):
    if Category.objects.filter(name__iexact=value).exists():
        raise ValidationError(_("A category with this name already exists."))
    return value
