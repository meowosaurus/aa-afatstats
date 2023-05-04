import datetime

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count, Q

from afat.models import *

from django.contrib.auth.models import User
from allianceauth.eveonline.models import *
from allianceauth.authentication.models import *

from .models import *
from .data import *

def del_player_models():
    try:
        CorporationMains.objects.all().delete()
        CorporationAlts.objects.all().delete()

        CapsuleersStat.objects.all().delete()
    except OperationalError as e:
        print("#1020 -> Unable to delete CorporationMains, CorporationAlts and CapsuleersStat models in del_player_models -> capsuleer_helper.py")


def get_fats(ships = "", queue_type = 0):
    try:
        all_fats = AFat.objects.all()
    except (NameError, AttributeError, OperationalError) as e:
        print("#1025 -> Unable to load AFat model in get_fats -> capsuleer_helper.py")

    try:
        for fat in all_fats:
            if len(ships) > 0:
                if not fat.shiptype in ships:
                    continue

            try:
                alt_char = CorporationAlts.objects.get(alt_character=fat.character)
                if alt_char:
                    alt_data = EveCharacter.objects.get(character_name=alt_char.alt_character)

                    temp = str(queue_type) + ":" + str(alt_char.main_character)
                    if CapsuleersStat.objects.filter(stat=temp):
                        sql_queue = CapsuleersStat.objects.filter(stat=temp)[0]

                        sql_queue.fats += 1

                        sql_queue.save()
                    else:
                        sql_queue = CapsuleersStat()

                        sql_queue.stat = str(queue_type) + ":" + str(alt_char.main_character)
                        sql_queue.identifier = queue_type
                        sql_queue.character_name = alt_char.main_character
                        sql_queue.character_id = alt_data.character_id
                        sql_queue.corporation_name = alt_data.corporation_name
                        sql_queue.corporation_id = alt_data.corporation_id
                        sql_queue.fats = 1

                        sql_queue.save()
            except (NameError, AttributeError, DoesNotExist, OperationalError) as e:
                print("#1022 -> Unable to overwrite CapsuleersStat model in get_fats -> capsuleer_helper.py")
    except (NameError, AttributeError, OperationalError) as e:
        print("#1021 -> Unable get interate through AFat model in get_fats -> capsuleer_helper.py")

def recalculate_player_data():
    del_player_models()

    try:
        characters = EveCharacter.objects.all()
    except (NameError, AttributeError, OperationalError) as e:
        print("#1023 -> Unable get load EveCharacter model in recalculate_player_data -> capsuleer_helper.py")

    try:
        for character in characters:
            records = OwnershipRecord.objects.filter(character=character)
            for record in records:
            
                if not CorporationAlts.objects.filter(alt_character=character.character_name):

                    main = EveCharacter.objects.filter(character_name=record.user)
                    if main:
                    
                        if not CorporationMains.objects.filter(character_name=main[0].character_name):
                            main_char = CorporationMains()
                            main_char.character_name = main[0].character_name
                            main_char.character_id = main[0].character_id
                            main_char.corporation_name = main[0].corporation_name
                            main_char.corporation_id = main[0].corporation_id
                            main_char.fats = 0
                            main_char.save()

                        alt_char = CorporationAlts()
                        alt_char.main_character = record.user
                        alt_char.alt_character = character.character_name
                        alt_char.alt_id = character.character_id
                        alt_char.save()
    except (NameError, AttributeError, OperationalError) as e:
        print("#1024 -> Unable to overwrite CorporationMains model in recalculate_player_data -> capsuleer_helper.py")

    get_fats("", 0)

    ships = {"Burst", "Scalpel", "Scythe", "Scimitar",
             "Navitas", "Thalia", "Exequror", "Oneiros",
             "Bantam", "Kirin", "Osprey", "Basilisk",
             "Inquisitor", "Deacon", "Augoror", "Guardian"}

    get_fats(ships, 1)

    ships = {"Bifrost", "Claymore", "Slepnir",
             "Magus", "Astarte", "Eos",
             "Stork", "Nighthawk", "Vulture",
             "Pontifex", "Absolution", "Damnation"}

    get_fats(ships, 2)

    ships = {"Stiletto", "Slasher", "Rifter", "Sabre", "Claw", 
             "Incursus", "Atron", "Ares", "Taranis", "Eris", 
             "Condor", "Merlin", "Crow", "Raptor", "Flycatcher",
             "Punisher", "Executioner", "Malediction", "Crusader", "Heretic"}

    get_fats(ships, 3)

    ships = {"Vigil", "Vigil Fleet Issue", "Hyena", "Huginn", "Rapier", "Panther",
             "Maulus", "Maulus Navy Issue", "Keres", "Arazu", "Lachesis", "Sin",
             "Griffin", "Griffin Navy Issue", "Kitsune", "Rook", "Falcon", "Widow",
             "Crucifier", "Crucifier Navy Issue", "Sentinel", "Curse", "Pilgrim", "Redeemer",
             "Curor", "Ashimmu", "Bhaalgorn", "Daredevil", "Vigilant", "Vindicator", 
             "Garmur", "Orthrus", "Barghest"}

    get_fats(ships, 4)

    ships = {"Nidhoggur", "Naglfar", "Naglfar Navy Issue",
             "Thanatos", "Moros", "Moros Navy Issue",
             "Chimera", "Phoenix", "Phoenix Navy Issue",
             "Archon", "Revelation", "Revelation Navy Issue"}

    get_fats(ships, 5)

    ships = {"Lif", "Ninazu", "Minokawa", "Apostle", "Loggerhead", "Dagon"}

    get_fats(ships, 6)

    ships = {"Hel", "Nyx", "Wyvern", "Aeon", "Vendetta"}

    get_fats(ships, 7)

    ships = {"Ragnarok", "Erebus", "Leviathan", "Avatar", "Molok", "Komodo", "Vanquisher"}

    get_fats(ships, 8)
