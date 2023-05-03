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

def del_player_models():
    CorporationMains.objects.all().delete()
    CorporationAlts.objects.all().delete()

def get_fats(ships = ""):
    account_data = dict()

    all_fats = AFat.objects.all()

    for fat in all_fats:
        if len(ships) > 0:
            if not fat.shiptype in ships:
                continue

        alt_char = CorporationAlts.objects.get(alt_character=fat.character)
        if alt_char:
            alt_data = EveCharacter.objects.get(character_name=alt_char.alt_character)
            if alt_char.main_character not in account_data:
                account_data[alt_char.main_character] = (alt_data.character_id,
                                                         alt_data.corporation_id,
                                                         alt_data.corporation_name, 
                                                         1)
            else:
                temp = list(account_data[alt_char.main_character])
                temp[3] += 1
                account_data[alt_char.main_character] = tuple(temp)

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
                        main_char.corporation_name = main[0].character_name
                        main_char.corporation_id = main[0].corporation_id
                        main_char.fats = 0
                        main_char.save()

                    alt_char = CorporationAlts()
                    alt_char.main_character = record.user
                    alt_char.alt_character = character.character_name
                    alt_char.save()

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
