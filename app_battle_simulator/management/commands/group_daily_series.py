# creo uno script per poterlo usare nell'heroku scheduler
# ne faccio un base command, così ogni tot heroku lo ranna ed è come se lo runnasse da consolle

#da runnare ogni giorno a mezzanotte

from django.core.management.base import BaseCommand

from pm_lookup.processing.scheduled_processing_3 import arrange_daily_time_series_and_graphs

# quando scrivo
# python manage.py group_daily_series
# la funzione command viene rannata automaticamente

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        #arrangia le serie storiche giornaliere
        arrange_daily_time_series_and_graphs()