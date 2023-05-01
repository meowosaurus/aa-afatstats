"""App URLs"""

# Django
from django.urls import path

# AA afatstats App
from afatstats import views

app_name: str = "afatstats"

urlpatterns = [
    path("", views.index, name="index"),
    
    ### Capsuleers
    path("capsuleers/", views.capsuleers_index, name="capsuleers_index"),
    path("capsuleers/logi/", views.capsuleers_logi, name="capsuleers_logi"),
    path("capsuleers/boosts/", views.capsuleers_boosts, name="capsuleers_boosts"),
    path("capsuleers/tackle/", views.capsuleers_boosts, name="capsuleers_tackle"),
    path("capsuleers/snowflakes/", views.capsuleers_boosts, name="capsuleers_snowflakes"),
    ### Capsuleers Caps
    path("capsuleers/caps/", views.capsuleers_caps, name="capsuleers_caps"),
    path("capsuleers/fax/", views.capsuleers_fax, name="capsuleers_fax"),
    path("capsuleers/supers/", views.capsuleers_supers, name="capsuleers_supers"),
    path("capsuleers/titans/", views.capsuleers_titans, name="capsuleers_titans"),
]
