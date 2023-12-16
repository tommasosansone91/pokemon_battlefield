from django.core.management.base import BaseCommand
from pm_lookup.models import target_area_realtime_data

class Command(BaseCommand):
    def handle(self, *args, **options):
        target_area_realtime_data.objects.all().delete()
