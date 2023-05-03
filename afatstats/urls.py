"""App URLs"""

# Django
from django.urls import path

# AA afatstats App
from afatstats import views

app_name: str = "afatstats"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    
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
]
