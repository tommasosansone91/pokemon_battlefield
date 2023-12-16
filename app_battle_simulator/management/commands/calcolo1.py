from django.core.management.base import BaseCommand

# questo file lo richiamo solo se c'e l'ho in 
# app/management/commands/nome_file.py
# la linea from django.core.management.base import BaseCommand
# l'intestazione
# class Command(BaseCommand):
#     def handle(self, *args, **options):

# python manage.py calcolo1

class Command(BaseCommand):
    def handle(self, *args, **options):

        # import numpy as np 
        import math

        long_a = 45.514795
        long_b = 45.427391

        lat_a = 9.112599
        lat_b = 9.256506

        # distanza in unità di coordinate
        dist_coord = math.sqrt( (long_a - long_b )**2 + (lat_a - lat_b)**2 )

        # in realtà la distanza tra questi due punti è 14.9 km

        fattore_conversione = dist_coord/14.9 # da coordinate a km (coord/km)

        # delta_long = abs(long_a - long_b)
        # delta_lat = abs(lat_a - lat_b)

        # # raggio medio tra i due punti in formato di coordinate
        # mean_radius = np.mean([delta_long, delta_lat])/2

        # in realtà la distanza tra questi due punti è 14.9 km

        self.stdout.write(self.style.SUCCESS('Per milano il fattore di conversione medio è "%s"' % fattore_conversione)) 