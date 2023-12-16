# con questo script verifico 
# se sono ok e funzioni che aggiornano le serie storiche e relativi grafici

from django.core.management.base import BaseCommand

from pm_lookup.processing.scheduled_processing_2 import arrange_time_series_and_graphs
from pm_lookup.processing.scheduled_processing_3 import arrange_daily_time_series_and_graphs

# quando scrivo
# python manage.py predispose_historical_series
# la funzione command viene rannata automaticamente
class Command(BaseCommand):
    def handle(self, *args, **options):

        arrange_time_series_and_graphs()
        arrange_daily_time_series_and_graphs()