import numpy as np

from pm_lookup.models import target_area_input_data
from pm_lookup.models import target_area_realtime_data
from pm_lookup.models import target_area_history_data
from pm_lookup.models import target_area_time_serie

# importo i drawers
from pm_lookup.drawers.drawer1 import draw_timeserie_PM10_graph
from pm_lookup.drawers.drawer1 import draw_timeserie_PM25_graph

# aggiunto per fixare il fatto che nei grafici è mostrato orario come se fosse in UTC
# errore sopraggiunto dopo il reset del db?
from pm_lookup.processing.auxiliary_processing import fix_timezone_mismatch_1

def arrange_time_series_and_graphs():

    target_area_time_serie.objects.all().delete()

    print("Eliminate tutte le serie storiche in target_area_time_serie!")

    print("Inizio disposizione dati in serie storiche per ogni località...")

    # prendo i record delle 24 ore degli ultimi 30 giorni
    Lunghezza_temporale = 24*30

    for area_di_interesse in target_area_input_data.objects.all():

        print("Predisposizione dati ed elementi del grafico per la serie storica per %s..." % area_di_interesse.Name)

        # isola i record di una località - è cmq un gruppo di oggetti
        records_serie_storica = target_area_history_data.objects.filter(Target_area_input_data=area_di_interesse)
        
        records_serie_storica = records_serie_storica[: Lunghezza_temporale - 1]

        # nota: i dati sno già ordinati per default in ordine decrescente

        serie_storica = {
                        #ce n'è solo una perchè l'ho filtrata
                        "Target_area_input_data" : area_di_interesse.Name,

                        # questi sono vettori di valori

                        "Last_update_time" : [i.Last_update_time for i in records_serie_storica],

                        "PM10_mean" : [i.PM10_mean for i in records_serie_storica],
                        "PM25_mean" : [i.PM25_mean for i in records_serie_storica],

                        "PM10_quality" : [i.PM10_quality for i in records_serie_storica],
                        "PM25_quality" : [i.PM25_quality for i in records_serie_storica],

                        "PM10_cathegory" : [i.PM10_cathegory for i in records_serie_storica],
                        "PM25_cathegory" : [i.PM25_cathegory for i in records_serie_storica],

                        "n_selected_sensors" : [i.n_selected_sensors for i in records_serie_storica],

                        }


        # aggiunto per fixare il fatto che nei grafici è mostrato orario come se fosse in UTC
        # errore sopraggiunto dopo il reset del db?
        serie_storica["Last_update_time"] = fix_timezone_mismatch_1(serie_storica["Last_update_time"])


        # la posizione di serie storiche indica la città

        # print(serie_storiche[0].keys())

        # time array
        time_values = np.array(serie_storica['Last_update_time'])

        # values
        PM10_values = np.array(serie_storica['PM10_mean'])
        PM25_values = np.array(serie_storica['PM25_mean'])  

            # colora il retro del grafico per fasce anzchè fare le linee di soglia


        # questo script è orario, non servono i limiti normativi
        
        # pm10 maxs
        # PM10_daily_max_35_days_max = np.array([50 for i in time_values])
        # PM10_annual_mean_max = np.array([40 for i in time_values])

        #PM2.5 maxs
        # PM25_annual_mean_max = np.array([20 for i in time_values])

        # trovare un modo per far comparire nelle etichette del grafico
         
            

        # traccio i grafici e ottengo il javascript
        graph_PM10_title = "Serie storiche orarie del PM10 per "+area_di_interesse.Name
        graph_PM25_title = "Serie storiche orarie del PM2.5 per "+area_di_interesse.Name

        graph_PM10 = draw_timeserie_PM10_graph(time_values, PM10_values, graph_title=graph_PM10_title)
        graph_PM25 = draw_timeserie_PM25_graph(time_values, PM25_values, graph_title=graph_PM25_title)

        

        elementi_grafico = target_area_time_serie(
                                                    # errore qui
                                                    Target_area_input_data = target_area_input_data.objects.get(Name=area_di_interesse.Name),

                                                    # questi sono vettori di valori

                                                    Record_time_values = '[' + ', '.join(str(e) for e in  serie_storica['Last_update_time'] ) +']',

                                                    PM10_mean_values = '[' + ', '.join(str(e) for e in  serie_storica['PM10_mean'] ) +']',
                                                    PM25_mean_values = '[' + ', '.join(str(e) for e in  serie_storica['PM25_mean'] ) +']',

                                                    PM10_quality_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM10_quality'] ) +'"]',
                                                    PM25_quality_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM25_quality'] ) +'"]',

                                                    PM10_cathegory_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM10_cathegory'] ) +'"]',
                                                    PM25_cathegory_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM25_cathegory'] ) +'"]',

                                                    n_selected_sensors_values = '[' + ', '.join(str(e) for e in  serie_storica['n_selected_sensors'] ) +']',

                                                    PM10_graph_div = graph_PM10,
                                                    PM25_graph_div = graph_PM25,

                                                    )

        elementi_grafico.save()

        print("Predisposti dati ed elementi del grafico per la serie storica per %s!" % area_di_interesse.Name)  

    print("Predisposti dati ed elementi dei grafici per le serie storiche per tutte le località!")  
