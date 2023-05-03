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
                      ### Capsuleer Permissions
                      ("capsuleer_top", "Can access capsuleer top statistics"),
                      ("capsuleer_logi", "Can access capsuleer logi statistics"),
                      ("capsuleer_boosts", "Can access capsuleer boosts statistics"),
                      ("capsuleer_tackle", "Can access capsuleer tackle statistics"),
                      ("capsuleer_snowflakes", "Can access capsuleer snowflakes statistics"),
                      ### Capsuleer Caps Permissions
                      ("capsuleer_caps", "Can access capsuleer caps statistics"),
                      ("capsuleer_fax", "Can access capsuleer fax statistics"),
                      ("capsuleer_supers", "Can access capsuleer supers statistics"),
                      ("capsuleer_titans", "Can access capsuleer titans statistics"),
                      ### Corporations Permissions
                      ("corporations_total", "Can access corporations total statistics"),
                      ("corporations_relative", "Can access corporations relative statistics"),
                      ("corporations_logi", "Can access corporations logi statistics"),
                      ("corporations_boosts", "Can access corporations boosts statistics"),
                      ("corporations_tackle", "Can access corporations tackle statistics"),
                      ("corporations_snowflakes", "Can access corporations snowflakes statistics"),
                      ### Corporations Caps Permissions
                      ("corporations_caps", "Can access corporations caps statistics"),
                      ("corporations_fax", "Can access corporations fax statistics"),
                      ("corporations_supers", "Can access corporations supers statistics"),
                      ("corporations_titans", "Can access corporations titans statistics"),)


class MainCharacters(models.Model):
    main_character = models.CharField(max_length=255)

    alt_character = models.CharField(max_length=255)

    def __str__(self):
        return self.main_character + ": " + self.alt_character





