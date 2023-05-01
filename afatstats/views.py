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

def generate_context(request, title):
    context = {"title": title,
               "permissions": request.user.get_all_permissions()}

    print(request.user.get_all_permissions())

    return context

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
    account_fat_counts = dict()

    all_fat_links = AFatLink.objects.all()
    all_fats = AFat.objects.all()

    for fat in all_fats:
        char = MainCharacters.objects.get(alt_character=fat.character)
        if char:
            if char.main_character not in account_fat_counts:
                account_fat_counts[char.main_character] = 1
            else:
                account_fat_counts[char.main_character] += 1

    return account_fat_counts

def get_fats_count_type(ships):
    account_fat_counts = dict()

    all_fat_links = AFatLink.objects.all()
    all_fats = AFat.objects.all()

    for fat in all_fats:
        if not fat.shiptype in ships:
            continue

        char = MainCharacters.objects.get(alt_character=fat.character)
        if char:
            if char.main_character not in account_fat_counts:
                account_fat_counts[char.main_character] = 1
            else:
                account_fat_counts[char.main_character] += 1

    return account_fat_counts

def ships_view(context, ships):
    # Find all main characters and their alt characters
    find_main_characters()
    # Count all fats
    counts = get_fats_count_type(ships)

    # Sort array from big to small (FAT based)
    account_fat_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    context.update({'account_fat_counts': account_fat_counts})

    return context

@login_required
@permission_required("afatstats.basic_access")
def index(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """

    context = generate_context(request, "Top Players")

    # Find all main characters and their alt characters
    find_main_characters()
    # Count all fats
    counts = get_fats_count()

    # Sort array from big to small (FAT based)
    account_fat_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    context.update({'account_fat_counts': account_fat_counts})

    

    return render(request, "afatstats/index.html", context)

### Players

@login_required
@permission_required("afatstats.capsuleer_top")
def capsuleers_top(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """

    context = generate_context(request, "Top Players")

    # Find all main characters and their alt characters
    find_main_characters()
    # Count all fats
    counts = get_fats_count()

    # Sort array from big to small (FAT based)
    account_fat_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    context.update({'account_fat_counts': account_fat_counts})

    return render(request, "afatstats/index.html", context)

@login_required
@permission_required("afatstats.capsuleer_logi")
def capsuleers_logi(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Logis")

    ships = {"Burst", "Scalpel", "Scythe", "Scimitar"}

    context = ships_view(context, ships)

    return render(request, "afatstats/index.html", context)

@login_required
@permission_required("afatstats.capsuleer_boosts")
def capsuleers_boosts(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Boosts")

    ships = {"Bifrost", "Claymore"}

    context = ships_view(context, ships)

    return render(request, "afatstats/index.html", context)

@login_required
@permission_required("afatstats.capsuleer_tackle")
def capsuleers_tackle(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Tackle")

    ships = {"Stiletto", "Slasher", "Rifter", "Sabre"}

    context = ships_view(context, ships)

    return render(request, "afatstats/index.html", context)

@login_required
@permission_required("afatstats.capsuleer_snowflakes")
def capsuleers_snowflakes(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Snowflakes")

    ships = {"Huginn", "Rapier"}

    context = ships_view(context, ships)

    return render(request, "afatstats/index.html", context)

@login_required
@permission_required("afatstats.capsuleer_caps")
def capsuleers_caps(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Caps")

    ships = {"Naglfar", "Nidhoggur"}

    context = ships_view(context, ships)

    return render(request, "afatstats/index.html", context)

@login_required
@permission_required("afatstats.capsuleer_fax")
def capsuleers_fax(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top FAX")

    ships = {"Lif"}

    context = ships_view(context, ships)

    return render(request, "afatstats/index.html", context)

@login_required
@permission_required("afatstats.capsuleer_supers")
def capsuleers_supers(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Supers")

    ships = {"Hel"}

    context = ships_view(context, ships)

    return render(request, "afatstats/index.html", context)

@login_required
@permission_required("afatstats.capsuleer_titans")
def capsuleers_titans(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Titans")

    ships = {"Ragnarok"}

    context = ships_view(context, ships)

    return render(request, "afatstats/index.html", context)

