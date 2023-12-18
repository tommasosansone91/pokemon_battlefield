from django.urls import path
from . import views # nota che con questo importo tutte le liste
from . import api # devo aggiungerlo perchè ho delle altre views

urlpatterns = [

    # # path, vista, nome di richiamo

    path('', views.home, name="home"),
    
    path(
        'api/launch_battle/<int:pkmn_id1>/<int:pkmn_id2>/', 
         api.launch_battle, 
         name="launch_battle"
         ),
    
    # mantieni lo standard di nomenclatura tra i tre termini
]