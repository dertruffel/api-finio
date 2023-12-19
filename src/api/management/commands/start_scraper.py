from django.core.management import BaseCommand
from api.tasks import start_scraper

class Command(BaseCommand):
    help = 'Starts the scraper'

    def handle(self, *args, **kwargs):
        print("Starting scrapping")
        start_scraper.delay()
        print("Scrapping started")
