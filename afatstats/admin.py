"""Admin models"""

# Django
from django.contrib import admin  # noqa: F401
from .models import *

admin.site.register(CorporationData)
admin.site.register(CorporationMains)
admin.site.register(CorporationAlts)

admin.site.register(CapsuleersStat)