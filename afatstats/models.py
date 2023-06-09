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

class CorporationData(models.Model):
    corporation_name = models.CharField(max_length=255,
                                        unique=True,
                                        help_text="Corporation's name: A string")

    corporation_id = models.IntegerField(default=0,
                                         help_text="Corporation's ID: An integer")

    corporation_ticker = models.CharField(max_length=255,
                                          unique=True,
                                          help_text="Corporation's ticker: A String")

    member_count = models.IntegerField(default=0,
                                       help_text="Corporation's member count: An integer")

    players = models.IntegerField(default=0,
                                  help_text="Corporation's player count: An integer")

    fats = models.IntegerField(default=0,
                               help_text="Corporation's fats: An integer")

    rel_fats = models.FloatField(default=0,
                                 help_text="Corporation's relative fats: A float")

    shit_metric = models.FloatField(default=0,
                                    help_text="Corporation's shit metric: A float")

    def __str__(self):
        return "[" + self.corporation_ticker + "] " + self.corporation_name

class CorporationMains(models.Model):
    character_name = models.CharField(max_length=255,
                                      unique=True)

    character_id = models.IntegerField(default=0)

    corporation_name = models.CharField(max_length=255)

    corporation_id = models.IntegerField(default=0)

    fats = models.IntegerField(default=0)

    def __str__(self):
        return self.character_name

class CorporationAlts(models.Model):
    alt_character = models.CharField(max_length=255,
                                      unique=True)

    alt_id = models.IntegerField(default=0)

    main_character = models.CharField(max_length=255)

    def __str__(self):
        return self.alt_character + " -> " + self.main_character

##########################################################

class CapsuleersStat(models.Model):
    stat = models.CharField(max_length=255, unique=True, default="",
                            help_text="The main identifier to make one row truely unique. Format: (identifier):(character_name) : A String")

    identifier = models.IntegerField(default=0,
                                     help_text="The main identifier, used for sorting only: 0 = total, 1 = logi, 2 = boosts, etc: An integer")

    character_name = models.CharField(max_length=255)

    character_id = models.IntegerField(default=0)

    corporation_name = models.CharField(max_length=255)

    corporation_id = models.IntegerField(default=0)

    fats = models.IntegerField(default=0)

    def __str__(self):
        return "(" + str(self.identifier) + ") " + self.character_name + ": " + str(self.fats)

