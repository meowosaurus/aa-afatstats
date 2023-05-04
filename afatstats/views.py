"""App Views"""

import datetime

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count, Q
from django.conf import settings

from afat.models import *

from django.contrib.auth.models import User
from allianceauth.eveonline.models import *
from allianceauth.authentication.models import *

from .models import *

from .capsuleer_helper import *
from .corporations_helper import *
from .tasks import *
from .data import *

def generate_context(request, title):
    context = {"title": title,
               "permissions": request.user.get_all_permissions()}

    return context

#########################################################################

@login_required
@permission_required("afatstats.basic_access")
def index(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """
    context = generate_context(request, "Top Total")

    # Recalculating data in debug mode, because celery doesn't work without a redis server
    if settings.DEBUG:
        recalculate_player_data()
        recalculate_corp_data()

    all_fats = CapsuleersStat.objects.filter(identifier=0).order_by('-fats')

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

def search(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Search for Players or Corporations")

    query = request.GET.get('query')

    search_results = dict()

    if query:
        results = CorporationAlts.objects.filter(alt_character=query)

        for result in results:
            character = CorporationMains.objects.filter(character_name=result.main_character)
            if character:
                search_results[character] = set()
                search_results[character] = (result.alt_character, 
                                             character[0].character_name,
                                             character[0].character_id,
                                             character[0].corporation_name,
                                             character[0].corporation_id,
                                             character[0].fats)

                print(character[0].fats)

        context.update({'search_results': search_results})    

    return render(request, "afatstats/search.html", context)

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

    all_fats = CapsuleersStat.objects.filter(identifier=0).order_by('-fats')

    print(all_fats)

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_logi")
def capsuleers_logi(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Logistics")

    all_fats = CapsuleersStat.objects.filter(identifier=1).order_by('-fats')

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_boosts")
def capsuleers_boosts(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Boosts")

    all_fats = CapsuleersStat.objects.filter(identifier=2).order_by('-fats')

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_tackle")
def capsuleers_tackle(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Tackle")

    all_fats = CapsuleersStat.objects.filter(identifier=3).order_by('-fats')

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_snowflakes")
def capsuleers_snowflakes(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Snowflakes")

    all_fats = CapsuleersStat.objects.filter(identifier=4).order_by('-fats')

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_caps")
def capsuleers_caps(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Caps")

    all_fats = CapsuleersStat.objects.filter(identifier=5).order_by('-fats')

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_fax")
def capsuleers_fax(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top FAX")

    all_fats = CapsuleersStat.objects.filter(identifier=6).order_by('-fats')

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_supers")
def capsuleers_supers(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Supers")

    all_fats = CapsuleersStat.objects.filter(identifier=7).order_by('-fats')

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_titans")
def capsuleers_titans(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Titans")

    all_fats = CapsuleersStat.objects.filter(identifier=8).order_by('-fats')

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

### Corporations

@login_required
@permission_required("afatstats.corporations_total")
def corporations_total(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Total Corp Participation Top 50")

    corporation_data = generate_corps_data(True)

    context.update({'corp_data': corporation_data})
    context.update({'total_fats': True})
            
    return render(request, "afatstats/corporations.html", context)

@login_required
@permission_required("afatstats.corporations_relative")
def corporations_relative(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Relative Corp Participation Top 50")

    corporation_data = generate_corps_data(False)
    
    context.update({'corp_data': corporation_data})
    context.update({'total_fats': False})
            
    return render(request, "afatstats/corporations.html", context)

@login_required
@permission_required("afatstats.corporations_logi")
def corporations_logi(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Relative Corp Participation")

    ships = {"Burst", "Scalpel", "Scythe", "Scimitar",
             "Navitas", "Thalia", "Exequror", "Oneiros",
             "Bantam", "Kirin", "Osprey", "Basilisk",
             "Inquisitor", "Deacon", "Augoror", "Guardian"}

    corporation_data = get_corporation_data(context, True, ships)

    corp_fat_counts = dict(sorted(corporation_data.items(), key=lambda item: item[1][5], reverse=True))

    context.update({'corp_fat_counts': corp_fat_counts})
            
    return render(request, "afatstats/corporations.html", context)

@login_required
@permission_required("afatstats.corporations_boosts")
def corporations_boosts(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Relative Corp Participation")

    ships = {"Bifrost", "Claymore", "Slepnir",
             "Magus", "Astarte", "Eos",
             "Stork", "Nighthawk", "Vulture",
             "Pontifex", "Absolution", "Damnation"}

    corporation_data = get_corporation_data(context, True, ships)

    corp_fat_counts = dict(sorted(corporation_data.items(), key=lambda item: item[1][5], reverse=True))

    context.update({'corp_fat_counts': corp_fat_counts})
            
    return render(request, "afatstats/corporations.html", context)

@login_required
@permission_required("afatstats.corporations_tackle")
def corporations_tackle(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Relative Corp Participation")

    ships = {"Stiletto", "Slasher", "Rifter", "Sabre", "Claw", 
             "Incursus", "Atron", "Ares", "Taranis", "Eris", 
             "Condor", "Merlin", "Crow", "Raptor", "Flycatcher",
             "Punisher", "Executioner", "Malediction", "Crusader", "Heretic"}

    corporation_data = get_corporation_data(context, True, ships)

    corp_fat_counts = dict(sorted(corporation_data.items(), key=lambda item: item[1][5], reverse=True))

    context.update({'corp_fat_counts': corp_fat_counts})
            
    return render(request, "afatstats/corporations.html", context)

@login_required
@permission_required("afatstats.corporations_snowflakes")
def corporations_snowflakes(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Relative Corp Participation")

    ships = {"Vigil", "Vigil Fleet Issue", "Hyena", "Huginn", "Rapier", "Panther",
             "Maulus", "Maulus Navy Issue", "Keres", "Arazu", "Lachesis", "Sin",
             "Griffin", "Griffin Navy Issue", "Kitsune", "Rook", "Falcon", "Widow",
             "Crucifier", "Crucifier Navy Issue", "Sentinel", "Curse", "Pilgrim", "Redeemer",
             "Curor", "Ashimmu", "Bhaalgorn", "Daredevil", "Vigilant", "Vindicator", 
             "Garmur", "Orthrus", "Barghest"}

    corporation_data = get_corporation_data(context, True, ships)

    corp_fat_counts = dict(sorted(corporation_data.items(), key=lambda item: item[1][5], reverse=True))

    context.update({'corp_fat_counts': corp_fat_counts})
            
    return render(request, "afatstats/corporations.html", context)

@login_required
@permission_required("afatstats.corporations_caps")
def corporations_caps(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Relative Corp Participation")

    ships = {"Nidhoggur", "Naglfar", "Naglfar Navy Issue",
             "Thanatos", "Moros", "Moros Navy Issue",
             "Chimera", "Phoenix", "Phoenix Navy Issue",
             "Archon", "Revelation", "Revelation Navy Issue"}

    corporation_data = get_corporation_data(context, True, ships)

    corp_fat_counts = dict(sorted(corporation_data.items(), key=lambda item: item[1][5], reverse=True))

    context.update({'corp_fat_counts': corp_fat_counts})
            
    return render(request, "afatstats/corporations.html", context)

@login_required
@permission_required("afatstats.corporations_fax")
def corporations_fax(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Relative Corp Participation")

    ships = {"Lif", "Ninazu", "Minokawa", "Apostle", "Loggerhead", "Dagon"}

    corporation_data = get_corporation_data(context, True, ships)

    corp_fat_counts = dict(sorted(corporation_data.items(), key=lambda item: item[1][5], reverse=True))

    context.update({'corp_fat_counts': corp_fat_counts})
            
    return render(request, "afatstats/corporations.html", context)

@login_required
@permission_required("afatstats.corporations_supers")
def corporations_supers(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Relative Corp Participation")

    ships = {"Hel", "Nyx", "Wyvern", "Aeon", "Vendetta"}

    corporation_data = get_corporation_data(context, True, ships)

    corp_fat_counts = dict(sorted(corporation_data.items(), key=lambda item: item[1][5], reverse=True))

    context.update({'corp_fat_counts': corp_fat_counts})
            
    return render(request, "afatstats/corporations.html", context)

@login_required
@permission_required("afatstats.corporations_titans")
def corporations_titans(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Relative Corp Participation")

    ships = {"Ragnarok", "Erebus", "Leviathan", "Avatar", "Molok", "Komodo", "Vanquisher"}

    corporation_data = get_corporation_data(context, True, ships)

    corp_fat_counts = dict(sorted(corporation_data.items(), key=lambda item: item[1][5], reverse=True))

    context.update({'corp_fat_counts': corp_fat_counts})
            
    return render(request, "afatstats/corporations.html", context)
