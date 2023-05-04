import datetime

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count

from afat.models import *

from django.contrib.auth.models import User
from allianceauth.eveonline.models import *
from allianceauth.authentication.models import *

from .models import *
from .data import *

def del_player_models():
    CorporationMains.objects.all().delete()
    CorporationAlts.objects.all().delete()

    CapsuleersTotal.objects.all().delete()
    CapsuleersLogi.objects.all().delete()
    CapsuleersBoosts.objects.all().delete()
    CapsuleersTackle.objects.all().delete()
    CapsuleersSnowflakes.objects.all().delete()


def get_fats(ships = "", queue_type = 0):
    account_data = dict()

    all_fats = AFat.objects.all()

    for fat in all_fats:
        if len(ships) > 0:
            if not fat.shiptype in ships:
                continue

        alt_char = CorporationAlts.objects.get(alt_character=fat.character)
        if alt_char:
            alt_data = EveCharacter.objects.get(character_name=alt_char.alt_character)
            if queue_type == 0: # total
                if(len(CapsuleersTotal.objects.filter(character_name=alt_char.main_character))):
                    sql_queue = CapsuleersTotal.objects.filter(character_name=alt_char.main_character)[0]
                else:
                    sql_queue = CapsuleersTotal()
            elif queue_type == 1: # logi
                if(len(CapsuleersLogi.objects.filter(character_name=alt_char.main_character))):
                    sql_queue = CapsuleersLogi.objects.filter(character_name=alt_char.main_character)[0]
                else:
                    sql_queue = CapsuleersLogi()
            elif queue_type == 2: # boosts
                if(len(CapsuleersBoosts.objects.filter(character_name=alt_char.main_character))):
                    sql_queue = CapsuleersBoosts.objects.filter(character_name=alt_char.main_character)[0]
                else:
                    sql_queue = CapsuleersBoosts()
            elif queue_type == 3: # tackle
                if(len(CapsuleersTackle.objects.filter(character_name=alt_char.main_character))):
                    sql_queue = CapsuleersTackle.objects.filter(character_name=alt_char.main_character)[0]
                else:
                    sql_queue = CapsuleersTackle()
            elif queue_type == 4: # snowflakes
                if(len(CapsuleersSnowflakes.objects.filter(character_name=alt_char.main_character))):
                    sql_queue = CapsuleersSnowflakes.objects.filter(character_name=alt_char.main_character)[0]
                else:
                    sql_queue = CapsuleersSnowflakes()
            elif queue_type == 5: # caps
                if(len(CapsuleersCaps.objects.filter(character_name=alt_char.main_character))):
                    sql_queue = CapsuleersCaps.objects.filter(character_name=alt_char.main_character)[0]
                else:
                    sql_queue = CapsuleersCaps()
            elif queue_type == 6: # fax
                if(len(CapsuleersFAX.objects.filter(character_name=alt_char.main_character))):
                    sql_queue = CapsuleersFAX.objects.filter(character_name=alt_char.main_character)[0]
                else:
                    sql_queue = CapsuleersFAX()
            elif queue_type == 7: # supers
                if(len(CapsuleersSupers.objects.filter(character_name=alt_char.main_character))):
                    sql_queue = CapsuleersSupers.objects.filter(character_name=alt_char.main_character)[0]
                else:
                    sql_queue = CapsuleersSupers()
            elif queue_type == 8: # titans
                if(len(CapsuleersTitans.objects.filter(character_name=alt_char.main_character))):
                    sql_queue = CapsuleersTitans.objects.filter(character_name=alt_char.main_character)[0]
                else:
                    sql_queue = CapsuleersTitans()

            if alt_char.main_character not in account_data:
                account_data[alt_char.main_character] = (alt_data.character_id,
                                                         alt_data.corporation_id,
                                                         alt_data.corporation_name, 
                                                         1)

                sql_queue.character_name = alt_char.main_character
                sql_queue.character_id = alt_data.character_id
                sql_queue.corporation_name = alt_data.corporation_name
                sql_queue.corporation_id = alt_data.corporation_id
                sql_queue.fats = 1

                sql_queue.save()
            else:
                temp = list(account_data[alt_char.main_character])
                temp[3] += 1
                account_data[alt_char.main_character] = tuple(temp)

                sql_queue.fats += 1
                sql_queue.save()

    return account_data

def recalculate_player_data():
    del_player_models()

    characters = EveCharacter.objects.all()

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
                    alt_char.save()

    DataStorage.capsuleers_total = get_fats()

    ships = {"Burst", "Scalpel", "Scythe", "Scimitar",
             "Navitas", "Thalia", "Exequror", "Oneiros",
             "Bantam", "Kirin", "Osprey", "Basilisk",
             "Inquisitor", "Deacon", "Augoror", "Guardian"}

    DataStorage.capsuleers_logi = get_fats(ships, 1)

    ships = {"Bifrost", "Claymore", "Slepnir",
             "Magus", "Astarte", "Eos",
             "Stork", "Nighthawk", "Vulture",
             "Pontifex", "Absolution", "Damnation"}

    DataStorage.capsuleers_boosts = get_fats(ships, 2)

    ships = {"Stiletto", "Slasher", "Rifter", "Sabre", "Claw", 
             "Incursus", "Atron", "Ares", "Taranis", "Eris", 
             "Condor", "Merlin", "Crow", "Raptor", "Flycatcher",
             "Punisher", "Executioner", "Malediction", "Crusader", "Heretic"}

    DataStorage.capsuleers_tackle = get_fats(ships, 3)

    ships = {"Vigil", "Vigil Fleet Issue", "Hyena", "Huginn", "Rapier", "Panther",
             "Maulus", "Maulus Navy Issue", "Keres", "Arazu", "Lachesis", "Sin",
             "Griffin", "Griffin Navy Issue", "Kitsune", "Rook", "Falcon", "Widow",
             "Crucifier", "Crucifier Navy Issue", "Sentinel", "Curse", "Pilgrim", "Redeemer",
             "Curor", "Ashimmu", "Bhaalgorn", "Daredevil", "Vigilant", "Vindicator", 
             "Garmur", "Orthrus", "Barghest"}

    DataStorage.capsuleers_snowflakes = get_fats(ships, 4)

    ships = {"Nidhoggur", "Naglfar", "Naglfar Navy Issue",
             "Thanatos", "Moros", "Moros Navy Issue",
             "Chimera", "Phoenix", "Phoenix Navy Issue",
             "Archon", "Revelation", "Revelation Navy Issue"}

    DataStorage.capsuleers_caps = get_fats(ships, 5)

    ships = {"Lif", "Ninazu", "Minokawa", "Apostle", "Loggerhead", "Dagon"}

    DataStorage.capsuleers_fax = get_fats(ships, 6)

    ships = {"Hel", "Nyx", "Wyvern", "Aeon", "Vendetta"}

    DataStorage.capsuleers_supers = get_fats(ships, 7)

    ships = {"Ragnarok", "Erebus", "Leviathan", "Avatar", "Molok", "Komodo", "Vanquisher"}

    DataStorage.capsuleers_titans = get_fats(ships, 8)

def get_main_characters_array():
    characters = EveCharacter.objects.all()

    users = {}
    for character in characters:
        records = OwnershipRecord.objects.filter(character=character)
        for record in records:
            if record.user not in users:
                users[record.user] = set()
                # main character needs to be first
                users[record.user].add(character)
            else:
                users[record.user].add(character)

    return users

def find_main_characters():
    characters = EveCharacter.objects.all()

    for character in characters:
        records = OwnershipRecord.objects.filter(character=character)
        for record in records:
            # Create new row if it doesn't exist yet
            if not MainCharacters.objects.filter(alt_character=character.character_name):
                char = MainCharacters()
                char.main_character = record.user
                char.alt_character = character.character_name
                char.save()

def get_fats_count():
    account_data = dict()

    all_fat_links = AFatLink.objects.all()
    all_fats = AFat.objects.all()

    for fat in all_fats:
        mainChar = MainCharacters.objects.get(alt_character=fat.character)
        if mainChar:
            mainData = EveCharacter.objects.get(character_name=fat.character)
            if mainChar.main_character not in account_data:
                account_data[mainChar.main_character] = (mainData.character_id, 
                                                         mainData.corporation_id, 
                                                         mainData.corporation_name, 
                                                         1)
            else:
                temp = list(account_data[mainChar.main_character])
                temp[3] += 1
                account_data[mainChar.main_character] = tuple(temp)

    return account_data

def get_fats_count_type(ships):
    account_data = dict()

    all_fat_links = AFatLink.objects.all()
    all_fats = AFat.objects.all()

    for fat in all_fats:
        if not fat.shiptype in ships:
            continue

        mainChar = MainCharacters.objects.get(alt_character=fat.character)
        if mainChar:
            mainData = EveCharacter.objects.get(character_name=fat.character)
            if mainChar.main_character not in account_data:
                account_data[mainChar.main_character] = (mainData.character_id, 
                                                         mainData.corporation_id, 
                                                         mainData.corporation_name, 
                                                         1)
            else:
                temp = list(account_data[mainChar.main_character])
                temp[3] += 1
                account_data[mainChar.main_character] = tuple(temp)

    return account_data

def index_view(context):
    # Find all main characters and their alt characters
    find_main_characters()
    # Count all fats
    counts = get_fats_count()

    # Sort array from big to small (FAT based)
    account_fat_counts = dict(sorted(counts.items(), key=lambda item: item[1][3], reverse=True))

    context.update({'account_fat_counts': account_fat_counts})

    return context

def ships_view(context, ships):
    # Find all main characters and their alt characters
    find_main_characters()
    # Count all fats
    counts = get_fats_count_type(ships)

    # Sort array from big to small (FAT based)
    account_fat_counts = dict(sorted(counts.items(), key=lambda item: item[1][3], reverse=True))

    context.update({'account_fat_counts': account_fat_counts})

    return context
