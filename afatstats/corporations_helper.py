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
    try:
        CorporationData.objects.all().delete()
    except OperationalError as e:
        print("#1019 -> Unable to delete CorporationData model in del_corp_models -> corporations_helper.py")

def load_corps_data(total = True):
    if total is False:
        try:
            corps_data = CorporationData.objects.all().order_by('-rel_fats')[:50]
        except (NameError, AttributeError, ValueError) as e:
            context.update({'error_code': '#1011'})
            context.update({'error_msg': 'Unable to load CorporationData model for column "-rel_fats" in load_corps_data -> corporations_helper.py'})
            return render(request, 'afatstats/error.html', context)
    else:
        try:
            corps_data = CorporationData.objects.all().order_by('-fats')[:50]
        except (NameError, AttributeError, ValueError) as e:
            context.update({'error_code': '#1012'})
            context.update({'error_msg': 'Unable to load CorporationData model for column "-fats" in load_corps_data -> corporations_helper.py'})
            return render(request, 'afatstats/error.html', context)

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

    try:
        all_corps = EveCorporationInfo.objects.all()
    except (NameError, AttributeError, OperationalError) as e:
        print("#1013 -> Unable to load EveCorporationInfo model in recalculate_corp_data -> corporations_helper.py")

    for corps in all_corps:
        try:
            corp_characters = EveCharacter.objects.filter(corporation_id=corps.corporation_id)
        except (NameError, AttributeError, OperationalError) as e:
            print("#1014 -> Unable to load EveCharacter model with corporation_id = corps.corporation_id in recalculate_corp_data -> corporations_helper.py")

        try:
            corp_data = CorporationData()
            corp_data.corporation_name = corps.corporation_name
            corp_data.corporation_id = corps.corporation_id
            corp_data.corporation_ticker = corps.corporation_ticker
            corp_data.member_count = corps.member_count
            corp_data.players = 0
            corp_data.fats = 0
            corp_data.rel_fats = 0
            corp_data.shit_metric = 0
        except TypeError as e:
            print("#1015 -> Unable to create new CorporationData object in recalculate_corp_data -> corporations_helper.py")

        try:
            # Used to get the actual player count, not the member count
            corporation_players = {}

            ships = ""

            if corp_characters.exists():

                for corp_char in corp_characters:
                    # Find main and save it in corporation_players
                    try:
                        records = OwnershipRecord.objects.filter(character=corp_char)
                        for record in records:
                            if record.user not in corporation_players:
                                corporation_players[record.user] = set()
                                corporation_players[record.user].add(corp_char)
                            else:
                                corporation_players[record.user].add(corp_char)
                    except (NameError, AttributeError, OperationalError) as e:
                        print("#1017 -> Unable to load existing OwnershipRecord object for character = corp_char in recalculate_corp_data -> corporations_helper.py")

                    # Calculate how many FATs a character has
                    try:
                        all_fats = AFat.objects.filter(character=corp_char)
                        for fat in all_fats:
                            corp_data.fats += 1
                    except (NameError, AttributeError, OperationalError) as e:
                        print("#1018 -> Unable to load existing AFat object for character = corp_char in recalculate_corp_data -> corporations_helper.py")
            
                corp_data.players = len(corporation_players)
                corp_data.rel_fats = corp_data.fats / corp_data.players
                corp_data.shit_metric = corp_data.fats / (corp_data.players * 6)

            corp_data.save()
        except (NameError, AttributeError, OperationalError) as e:
            print("#1016 -> Unable to fill new CorporationData object with data in recalculate_corp_data -> corporations_helper.py")

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

