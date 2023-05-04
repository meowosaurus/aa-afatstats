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

from .data import *

def del_corp_models():
    CorporationData.objects.all().delete()

def generate_corps_data(total = True):
    if total is False:
        corps_data = CorporationData.objects.all().order_by('-rel_fats')[:50]
    else:
        corps_data = CorporationData.objects.all().order_by('-fats')[:50]

    return corps_data

def get_corporation_data(ships=""):
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

    return corporation_data

def recalculate_corp_data():
    del_corp_models()

    all_corps = EveCorporationInfo.objects.all()

    for corps in all_corps:
        corp_characters = EveCharacter.objects.filter(corporation_id=corps.corporation_id)

        corp_data = CorporationData()
        corp_data.corporation_name = corps.corporation_name
        corp_data.corporation_id = corps.corporation_id
        corp_data.corporation_ticker = corps.corporation_ticker
        corp_data.member_count = corps.member_count
        corp_data.players = 0
        corp_data.fats = 0
        corp_data.rel_fats = 0

        # Used to get the actual player count, not the member count
        corporation_players = {}

        ships = ""

        if corp_characters.exists():

            for corp_char in corp_characters:
                # Find main and save it in corporation_players
                records = OwnershipRecord.objects.filter(character=corp_char)
                for record in records:
                    if record.user not in corporation_players:
                        corporation_players[record.user] = set()
                        corporation_players[record.user].add(corp_char)
                    else:
                        corporation_players[record.user].add(corp_char)

                # Calculate how many FATs a character has
                all_fats = AFat.objects.filter(character=corp_char)
                for fat in all_fats:
                    corp_data.fats += 1
            
            corp_data.players = len(corporation_players)
            corp_data.rel_fats = corp_data.fats / corp_data.players

        corp_data.save()

    #DataStorage.corporations_total = get_fats()

    ships = {"Burst", "Scalpel", "Scythe", "Scimitar",
             "Navitas", "Thalia", "Exequror", "Oneiros",
             "Bantam", "Kirin", "Osprey", "Basilisk",
             "Inquisitor", "Deacon", "Augoror", "Guardian"}

    #DataStorage.corporations_logi = get_fats(ships)

    ships = {"Bifrost", "Claymore", "Slepnir",
             "Magus", "Astarte", "Eos",
             "Stork", "Nighthawk", "Vulture",
             "Pontifex", "Absolution", "Damnation"}

    #DataStorage.corporations_boosts = get_fats(ships)

    ships = {"Stiletto", "Slasher", "Rifter", "Sabre", "Claw", 
             "Incursus", "Atron", "Ares", "Taranis", "Eris", 
             "Condor", "Merlin", "Crow", "Raptor", "Flycatcher",
             "Punisher", "Executioner", "Malediction", "Crusader", "Heretic"}

    #DataStorage.corporations_tackle = get_fats(ships)

    ships = {"Vigil", "Vigil Fleet Issue", "Hyena", "Huginn", "Rapier", "Panther",
             "Maulus", "Maulus Navy Issue", "Keres", "Arazu", "Lachesis", "Sin",
             "Griffin", "Griffin Navy Issue", "Kitsune", "Rook", "Falcon", "Widow",
             "Crucifier", "Crucifier Navy Issue", "Sentinel", "Curse", "Pilgrim", "Redeemer",
             "Curor", "Ashimmu", "Bhaalgorn", "Daredevil", "Vigilant", "Vindicator", 
             "Garmur", "Orthrus", "Barghest"}

    #DataStorage.corporations_snowflakes = get_fats(ships)

    ships = {"Nidhoggur", "Naglfar", "Naglfar Navy Issue",
             "Thanatos", "Moros", "Moros Navy Issue",
             "Chimera", "Phoenix", "Phoenix Navy Issue",
             "Archon", "Revelation", "Revelation Navy Issue"}

    #DataStorage.corporations_caps = get_fats(ships)

    ships = {"Lif", "Ninazu", "Minokawa", "Apostle", "Loggerhead", "Dagon"}

    #DataStorage.corporations_fax = get_fats(ships)

    ships = {"Hel", "Nyx", "Wyvern", "Aeon", "Vendetta"}

    #DataStorage.corporations_supers = get_fats(ships)

    ships = {"Ragnarok", "Erebus", "Leviathan", "Avatar", "Molok", "Komodo", "Vanquisher"}

    #DataStorage.corporations_titans = get_fats(ships)

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

