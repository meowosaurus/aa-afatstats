"""Admin models"""

# Django
from django.contrib import admin  # noqa: F401
from .models import *

# Register your models here.
admin.site.register(MainCharacters)
admin.site.register(CorporationData)
admin.site.register(CorporationMains)
admin.site.register(CorporationAlts)

admin.site.register(CapsuleersTotal)
admin.site.register(CapsuleersLogi)
admin.site.register(CapsuleersBoosts)
admin.site.register(CapsuleersTackle)
admin.site.register(CapsuleersSnowflakes)
admin.site.register(CapsuleersCaps)
admin.site.register(CapsuleersFAX)
admin.site.register(CapsuleersSupers)
admin.site.register(CapsuleersTitans)

admin.site.register(CapsuleersStat)