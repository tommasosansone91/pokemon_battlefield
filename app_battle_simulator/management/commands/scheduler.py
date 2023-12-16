from django.core.management.base import BaseCommand

# from datetime import datetime
# from apscheduler.schedulers.blocking import BlockingScheduler

# from pm_lookup.processing.scheduled_processing import save_history_pm

# # quando scrivo
# # python manage.py calcolo1
# # la funzione command viene rannata automaticamente

# class Command(BaseCommand):
#     def handle(self, *args, **options):

#         # Start the scheduler
#         sched = BlockingScheduler()
#         sched.start()

#         @sched.interval_schedule(seconds=10)
#         def job_function():
#             save_history_pm()


        

        # Schedule job_function to be called every two hours
        # sched.add_interval_job(job_function, minutes=0.03)

# --------------------------------------


# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqi_luftdaten.settings')

# from apscheduler.schedulers.blocking import BlockingScheduler

# from pm_lookup.processing.scheduled_processing import save_history_pm

# sched = BlockingScheduler()

# sched.add_job(save_history_pm, 'cron', id='run_every_1_min', minute='*/1')


# sched.start()


# -------------


# @sched.scheduled_job('interval', minutes=1)
# def timed_job():
#     save_history_pm()
#     print('This job is run every five minutes.')

# # @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# # def scheduled_job():
# #     print('This job is run every weekday at 5pm.')

# sched.start()


# poi type
# heroku ps:scale clock=1