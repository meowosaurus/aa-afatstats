"""App Tasks"""

# Standard Library
import logging

# Third Party
from celery import shared_task

from .capsuleer_helper import recalculate_player_data
from .corporations_helper import recalculate_corp_data

logger = logging.getLogger(__name__)



# Create your tasks here


# afatstats Task
@shared_task
def afatstats_task():
    """afatstats Task"""

    logger.debug(f"Data Source")
    print("test1")

    pass

@shared_task
def recalculate_data():

    try:
        recalculate_player_data()
    except Exception as e:
        logger.debug(f"Unable to automatically recalculate player data")

    try:
        recalculate_corp_data()
    except Exception as e:
        logger.debug(f"Unable to automatically recalculate corporation data")

