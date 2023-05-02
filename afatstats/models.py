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
        permissions = (("basic_access", "Can access this app"),
                      ("capsuleer_top", "Can access capsuleer top statistics"),
                      ("capsuleer_logi", "Can access capsuleer logi statistics"),
                      ("capsuleer_boosts", "Can access capsuleer boosts statistics"),
                      ("capsuleer_tackle", "Can access capsuleer tackle statistics"),
                      ("capsuleer_snowflakes", "Can access capsuleer snowflakes statistics"),
                      ("capsuleer_caps", "Can access capsuleer caps statistics"),
                      ("capsuleer_fax", "Can access capsuleer fax statistics"),
                      ("capsuleer_supers", "Can access capsuleer supers statistics"),
                      ("capsuleer_titans", "Can access capsuleer titans statistics"),)


class MainCharacters(models.Model):
    main_character = models.CharField(max_length=255)

    alt_character = models.CharField(max_length=255)

    def __str__(self):
        return self.main_character + ": " + self.alt_character





