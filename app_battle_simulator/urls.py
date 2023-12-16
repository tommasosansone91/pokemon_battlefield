from django.urls import path
from . import views # nota che con questo importo tutte le liste
# from . import views_api # devo aggiungerlo perchè ho delle altre views

urlpatterns = [

    # # path, vista, nome di richiamo

    path('', views.home, name="home"),

    # path('catalogo_api', views.catalogo_api, name="catalogo_api"),
    # path('catalogo_localita', views.catalogo_localita, name="catalogo_localita"),
    
    # path('valori_realtime', views.valori_realtime, name="valori_realtime"),
    
    # # disabilitato
    # # path('valori_realtime_forced_to_history', views.valori_realtime_forced_to_history, name="valori_realtime_forced_to_history"),

    # path('serie_storiche', views.serie_storiche, name="serie_storiche"),
    # path('serie_storiche_giornaliere', views.serie_storiche_giornaliere, name="serie_storiche_giornaliere"),

    # # viste delle api

    # # generalmente si fa una app per le api 
    # # e poi si mette include negli urls globali di progetto gli urls dell'app api preceduti dal pattern api/

    # # api liste

    # # poichè ho messo la sua views in un altro py, devo metterne il nome prima della funzione di views
    # path('api/cities_list', views_api.cities_list_api, name="cities_list"),
    # path('api/realtime_data', views_api.realtime_data_api, name="realtime_data"),
    # path('api/historical_data', views_api.historical_data_api, name="historical_data"),    
    # path('api/time_series', views_api.time_series_api, name="time_series"),
    # path('api/daily_time_series', views_api.daily_time_series_api, name="daily_time_series"),    

    # # api di dettaglio, quindi devo passare in ingresso (URL) il parametro

    # path('api/city_detail/<int:pk>', views_api.city_detail_api, name="city_detail"),
    # path('api/realtime_data_detail/<int:pk>', views_api.realtime_data_detail_api, name="realtime_data_detail"),

    # # non c'è il dettaglio degli history data perchè così prendo un record solo. è inutile.. ho una ok per ogni record.
    # # prendere un insieme di record corrisondenti ad una città ... è prendere una serie storica, quindi tanto vale
    # # path('api/historical_data_detail/<int:pk>', views_api.historical_data_detail_api, name="historical_data_detail"),

    # path('api/time_serie_detail/<int:pk>', views_api.time_serie_detail_api, name="time_serie_detail"),
    # path('api/daily_time_serie_detail/<int:pk>', views_api.daily_time_serie_detail_api, name="daily_time_serie_detail"),

    
    # mantieni lo standard di nomenclatura tra i tre termini
]