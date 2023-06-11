import re
import bleach
from html.parser import HTMLParser


from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Category

def validate_category(value):
    if Category.objects.filter(name__iexact=value).exists():
        raise ValidationError(_("A category with this name already exists."), code="invalid")
    return value


EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
def validate_email(email):
    # Perform email validation logic, such as using regular expressions
    # Return True if the email is valid, False otherwise
    return bool(EMAIL_PATTERN.match(email))


class SanitizeHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_stack = []
        self.cleaned_data = ""

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.tag_stack = []
        else:
            self.tag_stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "script":
            self.tag_stack = []
        elif self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()

    def handle_data(self, data):
        if not self.tag_stack:
            self.cleaned_data += data

def sanitize_input(data):
    # Remove HTML tags, special characters, and scripts
    parser = SanitizeHTMLParser()
    parser.feed(data)
    cleaned_data = bleach.clean(parser.cleaned_data, strip=True)
    cleaned_data = cleaned_data.strip()
    return cleaned_data