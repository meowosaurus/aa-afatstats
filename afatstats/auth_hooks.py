"""Hook into Alliance Auth"""

# Django
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

# AA afatstats App
from afatstats import urls

from .tasks import recalculate_data


class afatstatsMenuItem(MenuItemHook):
    """This class ensures only authorized users will see the menu entry"""

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _("FAT Leaderboard"),
            "fas fa-list-ol fa-fw",
            "afatstats:index",
            navactive=["afatstats:"],
        )

        # Recalculate data immediately after plugin is loaded (it will use celery!)
        recalculate_data.delay()

    def render(self, request):
        """Render the menu item"""

        if request.user.has_perm("afatstats.basic_access"):
            return MenuItemHook.render(self, request)

        return ""


@hooks.register("menu_item_hook")
def register_menu():
    """Register the menu item"""

    return afatstatsMenuItem()


@hooks.register("url_hook")
def register_urls():
    """Register app urls"""

    return UrlHook(urls, "fat-leaderboard", r"^fat-leaderboard/")
