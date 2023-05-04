"""Admin models"""

# Django
from django.contrib import admin  # noqa: F401
from .models import *

# Register your models here.
admin.site.register(MainCharacters)
admin.site.register(CorporationData)
admin.site.register(CorporationMains)
admin.site.register(CorporationAlts)

admin.site.register(CapsuleersStat)