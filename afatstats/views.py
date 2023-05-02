"""App Views"""

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

def generate_context(request, title):
    context = {"title": title,
               "permissions": request.user.get_all_permissions()}

    return context

@login_required
@permission_required("afatstats.basic_access")
def index(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """

    context = generate_context(request, "Top Total")

    context = index_view(context)

    return render(request, "afatstats/capsuleers.html", context)

### Players

@login_required
@permission_required("afatstats.capsuleer_top")
def capsuleers_top(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """

    context = generate_context(request, "Top Total")

    context = index_view(context)

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_logi")
def capsuleers_logi(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Logis")

    ships = {"Burst", "Scalpel", "Scythe", "Scimitar",
             "Navitas", "Thalia", "Exequror", "Oneiros",
             "Bantam", "Kirin", "Osprey", "Basilisk",
             "Inquisitor", "Deacon", "Augoror", "Guardian"}

    context = ships_view(context, ships)

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_boosts")
def capsuleers_boosts(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Boosts")

    ships = {"Bifrost", "Claymore", "Slepnir",
             "Magus", "Astarte", "Eos",
             "Stork", "Nighthawk", "Vulture",
             "Pontifex", "Absolution", "Damnation"}

    context = ships_view(context, ships)

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_tackle")
def capsuleers_tackle(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Tackle")

    ships = {"Stiletto", "Slasher", "Rifter", "Sabre", "Claw", 
             "Incursus", "Atron", "Ares", "Taranis", "Eris", 
             "Condor", "Merlin", "Crow", "Raptor", "Flycatcher",
             "Punisher", "Executioner", "Malediction", "Crusader", "Heretic"}

    context = ships_view(context, ships)

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_snowflakes")
def capsuleers_snowflakes(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Snowflakes")

    ships = {"Vigil", "Vigil Fleet Issue", "Hyena", "Huginn", "Rapier", "Panther",
             "Maulus", "Maulus Navy Issue", "Keres", "Arazu", "Lachesis", "Sin",
             "Griffin", "Griffin Navy Issue", "Kitsune", "Rook", "Falcon", "Widow",
             "Crucifier", "Crucifier Navy Issue", "Sentinel", "Curse", "Pilgrim", "Redeemer",
             "Curor", "Ashimmu", "Bhaalgorn", "Daredevil", "Vigilant", "Vindicator", 
             "Garmur", "Orthrus", "Barghest"}

    context = ships_view(context, ships)

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_caps")
def capsuleers_caps(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Caps")

    ships = {"Nidhoggur", "Naglfar", "Naglfar Navy Issue",
             "Thanatos", "Moros", "Moros Navy Issue",
             "Chimera", "Phoenix", "Phoenix Navy Issue",
             "Archon", "Revelation", "Revelation Navy Issue"}

    context = ships_view(context, ships)

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_fax")
def capsuleers_fax(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top FAX")

    ships = {"Lif", "Ninazu", "Minokawa", "Apostle", "Loggerhead", "Dagon", ""}

    context = ships_view(context, ships)

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_supers")
def capsuleers_supers(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Supers")

    ships = {"Hel", "Nyx", "Wyvern", "Aeon", "Vendetta", ""}

    context = ships_view(context, ships)

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_titans")
def capsuleers_titans(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Titans")

    ships = {"Ragnarok", "Erebus", "Leviathan", "Avatar", "Molok", "Komodo", "Vanquisher"}

    context = ships_view(context, ships)

    return render(request, "afatstats/capsuleers.html", context)

### Corporations

def corporations_total(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Total Corp Participation")
    
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
                    corp_temp_data[5] += 1

            # Get the amount of actual players
            corp_temp_data[4] = len(corporation_players)

            corporation_data[corps.corporation_name] = tuple(corp_temp_data)

    corp_fat_counts = dict(sorted(corporation_data.items(), key=lambda item: item[1][4], reverse=True))

    context.update({'corp_fat_counts': corp_fat_counts})
            
    return render(request, "afatstats/corporations.html", context)

def corporations_relative(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Relative Corp Participation")
    
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
                                                    0, # Player count
                                                    0) # FAT count



        if corp_characters.exists():
            corp_temp_data = list(corporation_data[corps.corporation_name])

            for corp_char in corp_characters:
                # Find main
                records = OwnershipRecord.objects.filter(character=corp_char)
                print(records)

                # Calculate how many FATs a character has
                all_fats = AFat.objects.filter(character=corp_char)
                for fat in all_fats:
                    
                    corp_temp_data[5] += 1

            corporation_data[corps.corporation_name] = tuple(corp_temp_data)

    corp_fat_counts = dict(sorted(corporation_data.items(), key=lambda item: item[1][4], reverse=True))

    context.update({'corp_fat_counts': corp_fat_counts})
            
    return render(request, "afatstats/corporations.html", context)

