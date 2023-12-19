import math

from celery import shared_task
from celery.result import AsyncResult
from django.core.cache import cache

from api.scrapper import Scrapper
from config.celery import app
from config.celery_helper import CeleryHelper


@shared_task(name="scrap")
def start_scraper():
    try:
        print("Starting scrapping")
        scrapper = Scrapper()
        scrapper.start()
        return True
    except Exception as e:
        print(e)
        return False
