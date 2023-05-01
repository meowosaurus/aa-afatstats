"""App Tasks"""

# Standard Library
import logging

# Third Party
from celery import shared_task

logger = logging.getLogger(__name__)

# Create your tasks here


# afatstats Task
@shared_task
def afatstats_task():
    """afatstats Task"""

    pass
