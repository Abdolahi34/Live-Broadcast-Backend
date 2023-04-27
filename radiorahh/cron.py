from django.urls import reverse
import requests


def every_10_second():
    requests.get('http://127.0.0.1:8000' + reverse('api:every_10_second'), timeout=6)  # TODO Domain
