"""App Configuration"""

# Django
from django.apps import AppConfig

# AA afatstats App
from afatstats import __version__


class afatstatsConfig(AppConfig):
    """App Config"""

    name = "afatstats"
    label = "afatstats"
    verbose_name = f"afatstats App v{__version__}"
