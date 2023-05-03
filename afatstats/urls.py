"""App URLs"""

# Django
from django.urls import path

# AA afatstats App
from afatstats import views

app_name: str = "afatstats"

urlpatterns = [
    path("", views.index, name="index"),
    
    ### Capsuleers
    path("capsuleers/", views.capsuleers_top, name="capsuleers_top"),
    path("capsuleers/logi/", views.capsuleers_logi, name="capsuleers_logi"),
    path("capsuleers/boosts/", views.capsuleers_boosts, name="capsuleers_boosts"),
    path("capsuleers/tackle/", views.capsuleers_tackle, name="capsuleers_tackle"),
    path("capsuleers/snowflakes/", views.capsuleers_snowflakes, name="capsuleers_snowflakes"),
    ### Capsuleers Caps
    path("capsuleers/caps/", views.capsuleers_caps, name="capsuleers_caps"),
    path("capsuleers/fax/", views.capsuleers_fax, name="capsuleers_fax"),
    path("capsuleers/supers/", views.capsuleers_supers, name="capsuleers_supers"),
    path("capsuleers/titans/", views.capsuleers_titans, name="capsuleers_titans"),

    ### Corporations
    path("corporations/", views.corporations_total, name="corporations_total"),
    path("corporations/relative/", views.corporations_relative, name="corporations_relative"),
    ### Corporations Sub-Caps
    path("corporations/logi/", views.corporations_logi, name="corporations_logi"),
    path("corporations/boosts/", views.corporations_boosts, name="corporations_boosts"),
    path("corporations/tackle/", views.corporations_tackle, name="corporations_tackle"),
    path("corporations/snowflakes/", views.corporations_snowflakes, name="corporations_snowflakes"),
    ### Corporations Caps
    path("corporations/caps/", views.corporations_caps, name="corporations_caps"),
    path("corporations/fax/", views.corporations_fax, name="corporations_fax"),
    path("corporations/supers/", views.corporations_supers, name="corporations_supers"),
    path("corporations/titans/", views.corporations_titans, name="corporations_titans"),
]
