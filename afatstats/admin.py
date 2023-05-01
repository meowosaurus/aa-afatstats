"""Admin models"""

# Django
from django.contrib import admin  # noqa: F401
from .models import MainCharacters

# Register your models here.
admin.site.register(MainCharacters)