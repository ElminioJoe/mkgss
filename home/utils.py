import random
import re
import string
from django.core.files import File
from django.utils.text import slugify
from io import BytesIO
from PIL import Image


def generate_random_string(length=5, chunk_size=6):
    """Generate a random string of lowercase letters and digits separated by hyphen."""
    chars = string.ascii_lowercase + string.digits
    random_string = "".join(random.choice(chars) for _ in range(length))
    return "-".join(
        random_string[i : i + chunk_size]
        for i in range(0, len(random_string), chunk_size)
    )


def generate_unique_slug(queryset, str=None):
    """
    Generate a unique slug based on the str provided,
    generates a random string if None is provided.
    """
    if not str:
        str = generate_random_string(18)

    base_slug = slugify(str).lower()
    random_chars = generate_random_string(12)
    slug = f"{base_slug}-{random_chars}"

    while queryset.filter(slug=slug).exists():
        random_chars = generate_random_string()
        slug = f"{base_slug}-{random_chars}"
    return slug


def set_parent_entry(instance):
    """Set the parent entry if it's being created."""
    if not instance.pk:
        existing_entries = instance.__class__.objects.filter(entry=instance.entry)
        if existing_entries.exists():
            instance.parent_entry = existing_entries.first()


def create_thumbnail(instance, image_field_name, thumbnail_field_name):
    """Create and save a thumbnail for the specified image field."""
    image_field = image_field_name
    thumbnail_field = thumbnail_field_name

    # If there is no image associated with this object, return
    if not image_field:
        return

    # Open original image
    image = Image.open(image_field)

    # Calculate thumbnail size based on the original image size
    original_size = image.size
    max_thumbnail_size = (200, 200)
    thumbnail_size = calculate_thumbnail_size(original_size, max_thumbnail_size)

    # Create thumbnail
    image.thumbnail(thumbnail_size, Image.LANCZOS)

    # Save thumbnail to a BytesIO object
    temp_handle = BytesIO()
    image.save(temp_handle, "JPEG")
    temp_handle.seek(0)

    # Save the thumbnail to the thumbnail field
    thumbnail_field.save(
        f"{image_field.name}_thumbnail.jpeg",
        File(temp_handle),
        save=False,
    )


def calculate_thumbnail_size(original_size, max_thumbnail_size):
    """Calculate the thumbnail size while preserving the aspect ratio."""
    width, height = original_size
    max_width, max_height = max_thumbnail_size

    if width <= max_width and height <= max_height:
        # No need to resize, return the original size
        return original_size

    # Calculate the aspect ratio
    aspect_ratio = width / height

    if aspect_ratio > max_width / max_height:
        # Image is wider, limit by width
        thumbnail_width = max_width
        thumbnail_height = int(thumbnail_width / aspect_ratio)
    else:
        # Image is taller or square, limit by height
        thumbnail_height = max_height
        thumbnail_width = int(thumbnail_height * aspect_ratio)

    return thumbnail_width, thumbnail_height
