"""
App Models
Create your models in here
"""

# Django
from django.db import models


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        """Meta definitions"""

        managed = False
        default_permissions = ()
        permissions = (("basic_access", "Can access this app"),)


class MainCharacters(models.Model):
    main_character = models.CharField(max_length=255)

    alt_character = models.CharField(max_length=255)

    def __str__(self):
        return self.main_character + ": " + self.alt_character






