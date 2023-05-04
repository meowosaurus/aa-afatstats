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

    try:
        if query:
            results = CorporationAlts.objects.filter(alt_character__icontains=query)

            for result in results:
                character = CorporationMains.objects.filter(character_name=result.main_character)
                if character:
                
                    temp = "0:" + str(result.main_character)
                    statistic = CapsuleersStat.objects.filter(stat=temp)

                    search_results[character] = set()
                    search_results[character] = (result.alt_character, 
                                             result.alt_id,
                                             character[0].character_name,
                                             character[0].character_id,
                                             character[0].corporation_name,
                                             character[0].corporation_id,
                                             statistic[0].fats)

                    print(character[0].fats)

            context.update({'search_results': search_results}) 
    except (NameError, AttributeError, ValueError, IndexError, TypeError) as e:
        context.update({'error_code': '#1000'})
        context.update({'error_msg': 'Blub'})
        return render(request, 'afatstats/error.html', context)

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
    
    try:
        all_fats = CapsuleersStat.objects.filter(identifier=0).order_by('-fats')
    except (NameError, AttributeError, ValueError) as e:
        context.update({'error_code': '#1000'})
        context.update({'error_msg': 'Blub'})
        return render(request, 'afatstats/error.html', context)

    print(all_fats)

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_logi")
def capsuleers_logi(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Logistics")

    try:
        all_fats = CapsuleersStat.objects.filter(identifier=1).order_by('-fats')
    except (NameError, AttributeError, ValueError) as e:
        context.update({'error_code': '#1000'})
        context.update({'error_msg': 'Blub'})
        return render(request, 'afatstats/error.html', context)


    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_boosts")
def capsuleers_boosts(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Boosts")

    try:
        all_fats = CapsuleersStat.objects.filter(identifier=2).order_by('-fats')
    except (NameError, AttributeError, ValueError) as e:
        context.update({'error_code': '#1000'})
        context.update({'error_msg': 'Blub'})
        return render(request, 'afatstats/error.html', context)


    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_tackle")
def capsuleers_tackle(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Tackle")

    try:
        all_fats = CapsuleersStat.objects.filter(identifier=3).order_by('-fats')
    except (NameError, AttributeError, ValueError) as e:
        context.update({'error_code': '#1000'})
        context.update({'error_msg': 'Blub'})
        return render(request, 'afatstats/error.html', context)

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_snowflakes")
def capsuleers_snowflakes(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Snowflakes")

    try:
        all_fats = CapsuleersStat.objects.filter(identifier=4).order_by('-fats')
    except (NameError, AttributeError, ValueError) as e:
        context.update({'error_code': '#1000'})
        context.update({'error_msg': 'Blub'})
        return render(request, 'afatstats/error.html', context)

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_caps")
def capsuleers_caps(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Caps")

    try:
        all_fats = CapsuleersStat.objects.filter(identifier=5).order_by('-fats')
    except (NameError, AttributeError, ValueError) as e:
        context.update({'error_code': '#1000'})
        context.update({'error_msg': 'Blub'})
        return render(request, 'afatstats/error.html', context)

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_fax")
def capsuleers_fax(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top FAX")

    try:
        all_fats = CapsuleersStat.objects.filter(identifier=6).order_by('-fats')
    except (NameError, AttributeError, ValueError) as e:
        context.update({'error_code': '#1000'})
        context.update({'error_msg': 'Blub'})
        return render(request, 'afatstats/error.html', context)

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_supers")
def capsuleers_supers(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Supers")

    try:
        all_fats = CapsuleersStat.objects.filter(identifier=7).order_by('-fats')
    except (NameError, AttributeError, ValueError) as e:
        context.update({'error_code': '#1000'})
        context.update({'error_msg': 'Blub'})
        return render(request, 'afatstats/error.html', context)

    context.update({'all_fats': all_fats})

    return render(request, "afatstats/capsuleers.html", context)

@login_required
@permission_required("afatstats.capsuleer_titans")
def capsuleers_titans(request: WSGIRequest) -> HttpResponse:
    context = generate_context(request, "Top Titans")

    try:
        all_fats = CapsuleersStat.objects.filter(identifier=8).order_by('-fats')
    except (NameError, AttributeError, ValueError) as e:
        context.update({'error_code': '#1000'})
        context.update({'error_msg': 'Blub'})
        return render(request, 'afatstats/error.html', context)

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
