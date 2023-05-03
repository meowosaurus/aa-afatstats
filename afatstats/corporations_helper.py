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

from .capsuleer_helper import *

def get_corp_main_char(corp_char, corporation_players):
    records = OwnershipRecord.objects.filter(character=corp_char)
    for record in records:
        if record.user not in corporation_players:
            corporation_players[record.user] = set()
            corporation_players[record.user].add(corp_char)
        else:
            corporation_players[record.user].add(corp_char)

    return corporation_players

def get_corp_char_fats(corp_char, corp_temp_data, ships):
    all_fats = AFat.objects.filter(character=corp_char)
    for fat in all_fats:
        # Check if the used ship was requested
        if len(ships) > 0:
            if not fat.shiptype in ships:
                continue

        corp_temp_data += 1

    return corp_temp_data

def get_corporation_data(context, total, ships=""):
    all_corps = EveCorporationInfo.objects.all()
    all_fat_links = AFatLink.objects.all()
    
    corporation_data = dict()
    account_data = dict()

    count = 0

    for corps in all_corps:
        corp_characters = EveCharacter.objects.filter(corporation_id=corps.corporation_id)

        corporation_data[corps.corporation_name] = (corps.corporation_id,
                                                    corps.corporation_name,
                                                    corps.corporation_ticker,
                                                    corps.member_count, 
                                                    0, # Players
                                                    0) # FATs

        # Used to get the actual player count, not the member count
        corporation_players = {}

        if corp_characters.exists():
            corp_temp_data = list(corporation_data[corps.corporation_name])

            for corp_char in corp_characters:
                # Find main and save it in corporation_players
                corporation_players = get_corp_main_char(corp_char, corporation_players)

                # Calculate how many FATs a character has
                corp_temp_data[5] = get_corp_char_fats(corp_char, corp_temp_data[5], ships)

            # Get the amount of actual players
            corp_temp_data[4] = len(corporation_players)

            corporation_data[corps.corporation_name] = tuple(corp_temp_data)

    # If FATs have to be relative to their corp size (actual players)
    if total is False:
        for key, corp_data in corporation_data.items():
            corp_temp_data = list(corp_data)
            if corp_temp_data[4] != 0 or corp_temp_data[5] != 0:
                corp_temp_data[5] = corp_temp_data[5] / corp_temp_data[4]
                corporation_data[key] = tuple(corp_temp_data)

    return corporation_data

