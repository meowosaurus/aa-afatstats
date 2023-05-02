"""App Tasks"""

# Standard Library
import logging

# Third Party
from celery import shared_task

from .capsuleer_helper import find_main_characters

logger = logging.getLogger(__name__)



# Create your tasks here


# afatstats Task
@shared_task
def afatstats_task():
    """afatstats Task"""

    logger.debug(f"Data Source")

    pass

@shared_task
def get_main_characters():
    print("test")
    find_main_characters()

