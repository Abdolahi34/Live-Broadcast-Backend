from django.db.models.signals import post_save
from django.dispatch import receiver
from urllib.request import urlopen
from django.urls import reverse

from Api.models import Program, Menu


@receiver(post_save, sender=Program)
def run_after_save_program_model(sender, instance, created, **kwargs):
    try:
        # Set timestamps on Save Program
        urlopen('http://127.0.0.1:8000' + reverse('Api:set_timestamps'), timeout=5)  # TODO Domain
        # Create programs.json
        urlopen('http://127.0.0.1:8000' + reverse('Api:create_programs_json'), timeout=5)  # TODO Domain
    except:
        pass


@receiver(post_save, sender=Menu)
def run_after_save_menu_model(sender, instance, created, **kwargs):
    try:
        # Create menu.json
        urlopen('http://127.0.0.1:8000' + reverse('Api:create_menu_json'), timeout=5)  # TODO Domain
    except:
        pass
