from django.db.models.signals import post_save
from django.dispatch import receiver
from urllib.request import urlopen
from django.urls import reverse
import logging

from api.models import Menu

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Menu)
def run_after_save_menu_model(sender, instance, created, **kwargs):
    try:
        # Create menu.json
        urlopen('http://127.0.0.1:8000' + reverse('api:create_menu_json'), timeout=5)  # TODO Domain
    except Exception as e:
        logger.error('The try block part encountered an error: %s', str(e), exc_info=True)
