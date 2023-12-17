import numpy as np

from pm_lookup.models import target_area_input_data
from pm_lookup.models import target_area_realtime_data
from pm_lookup.models import target_area_history_data
from pm_lookup.models import target_area_daily_time_serie

# importo i drawers
from pm_lookup.drawers.drawer1 import draw_timeserie_PM10_graph
from pm_lookup.drawers.drawer1 import draw_timeserie_PM25_graph

# per rivalutare le categorie di qualità dell'aria dei valori di mede giornalieri
from .auxiliary_processing import evaluate_PM10
from .auxiliary_processing import evaluate_PM25

#  per strippare le date dell'ora
from datetime import datetime

# per usare la funzione fllor in caso i dati storici orari non siano sufficienti per coprire i n giorni di dati medi dichiarati
import math

# aggiunto per fixare il fatto che nei grafici è mostrato orario come se fosse in UTC
# errore sopraggiunto dopo il reset del db?
from pm_lookup.processing.auxiliary_processing import fix_timezone_mismatch_1


def arrange_daily_time_series_and_graphs():

    target_area_daily_time_serie.objects.all().delete()

    print("Eliminate tutte le serie storiche giornaliere in target_area_daily_time_serie!")

    # print("Inizio disposizione dati in serie storiche giornaliere per ogni località...")




    for area_di_interesse in target_area_input_data.objects.all():

        print("Predisposizione dati ed elementi del grafico per la serie storica giornaliera per %s..." % area_di_interesse.Name)

        # prendo i record delle 24 ore degli ultimi x giorni
        # aggiornamento unitùà temporali al default
        n_ore = 24
        n_giorni = 30
        Lunghezza_temporale = n_ore * n_giorni

        # isola i record di una località - è cmq un gruppo di oggetti
        records_serie_storica = target_area_history_data.objects.filter(Target_area_input_data=area_di_interesse)
        
        n_target_area_history_data_records = records_serie_storica.count()


        # se Se i dati storici non contengono abbastanza record 
        # da raggiungere i giorni dichiarati per la lunghezza della serie storica giornaliera 
        # ( per default ho messo 30 giorni),  
        # allora Bisogna porre il numero di giorni uguale 
        # alla divisione arrotondata per difetto tra 
        # i dati presenti nel modello storico orario e 24 ore 
        if n_target_area_history_data_records < Lunghezza_temporale:
            
            print("Non ci sono dati sufficienti per realizzare la serie storica di almeno %s giorni." % n_giorni)
            
            # aggiornamento unitùà temporali
            n_giorni = int (math.floor( n_target_area_history_data_records / n_ore ) )
            Lunghezza_temporale = n_ore * n_giorni

            

            # Se i dati storici non contengono abbastanza record da raggiungere 
            # Neanche le 24 ore necessario per comporre una serie storica di lunghezza un giorno,
            # Allora Bisogna porre il numero di giorni pari ad uno e 
            # il numero di ore pari 
            # alla quantità di dati presenti all'interno del modello storico giornaliero
            if n_giorni == 0:
                
                print("Non ci sono dati sufficienti per realizzare la serie storica di almeno 1 giorno.")
                
                # aggiornamento unitùà temporali
                n_giorni = 1
                n_ore = n_target_area_history_data_records                
                Lunghezza_temporale = n_ore * n_giorni
                # in pratica sto dicendo di far finta che un giorno abbia n_ore con n_ore < 24
                print("Viene eseguita la media dei valori solo sui %s dati contenuti in target_area_history_data." % n_ore)
                
                # non ha senso fare il check di 1 ora perchè lo script è lanciato solo 1 volta ogni 24 ore, quindi ce ne sono sicuramente più di una 
                # a meno che il db sia cancellato tra le 23 e le 24

            print("Viene mostrata una serie storica lunga solo %s giorni." % n_giorni)

        records_serie_storica = records_serie_storica[: Lunghezza_temporale - 1]

        # nota: i dati sno già ordinati per default in ordine decrescente

        # records_serie_storica = [  round( np.mean( records_serie_storica[ 0 + 24*i : 24 + 24*i] ) , 2)  for i in range(n_giorni)]

        PM10_mean = [i.PM10_mean for i in records_serie_storica]
        PM25_mean = [i.PM25_mean for i in records_serie_storica]
        n_selected_sensors = [i.n_selected_sensors for i in records_serie_storica]
        Last_update_time = [ i.Last_update_time for i in records_serie_storica]


        # aggiunto per fixare il fatto che nei grafici è mostrato orario come se fosse in UTC
        # errore sopraggiunto dopo il reset del db?
        Last_update_time = fix_timezone_mismatch_1(Last_update_time)


        # nota che non ho bsogno di ritrasformare la stringa salvata nel db in numeri, me li legge già come numeri.
        PM10_daily_mean = [ round( np.mean( PM10_mean[ 0 + n_ore*i : n_ore + n_ore*i] ) , 2)  for i in range(n_giorni) ]
        PM25_daily_mean = [ round( np.mean( PM25_mean[ 0 + n_ore*i : n_ore + n_ore*i] ) , 2)  for i in range(n_giorni) ]

        PM10_daily_quality = [ evaluate_PM10(i)[0] for i in PM10_daily_mean ]
        PM25_daily_quality = [ evaluate_PM25(i)[0] for i in PM25_daily_mean ]

        PM10_daily_cathegory = [ evaluate_PM10(i)[1] for i in PM10_daily_mean ]
        PM25_daily_cathegory = [ evaluate_PM25(i)[1] for i in PM25_daily_mean ]


        Mean_n_selected_sensors = [ round( np.mean( n_selected_sensors[ 0 + n_ore*i : n_ore + n_ore*i] ) , 2)  for i in range(n_giorni) ]

        Update_date = [ Last_update_time[ 0 + n_ore*i ]  for i in range(n_giorni) ]
        
        # le date+ore vengono strippate delle ore, lasciando solo il giorno
        Update_date = [ element.date() for element in Update_date ]

        serie_storica = {
                        #ce n'è solo una perchè l'ho filtrata
                        "Target_area_input_data" : area_di_interesse.Name,

                        # questi sono vettori di valori

                        "Update_date" : Update_date,

                        "PM10_daily_mean" : PM10_daily_mean,
                        "PM25_daily_mean" : PM25_daily_mean,

                        "PM10_daily_quality" : PM10_daily_quality,
                        "PM25_daily_quality" : PM25_daily_quality,

                        "PM10_daily_cathegory" : PM10_daily_cathegory,
                        "PM25_daily_cathegory" : PM25_daily_cathegory,

                        "Mean_n_selected_sensors" : Mean_n_selected_sensors,

                        }



        

        # la posizione di serie storiche indica la città

        # print(serie_storiche[0].keys())

        # time array
        time_values = np.array(serie_storica['Update_date'])

        # values
        PM10_values = np.array(serie_storica['PM10_daily_mean'])
        PM25_values = np.array(serie_storica['PM25_daily_mean'])  

            # colora il retro del grafico per fasce anzchè fare le linee di soglia

        # a questo script si applicano i limiti normativi giornalieri

        # pm10 maxs
        PM10_daily_max_35_days_max = np.array([50 for i in time_values])
        # PM10_annual_mean_max = np.array([40 for i in time_values])

        #PM2.5 maxs
        # PM25_annual_mean_max = np.array([20 for i in time_values])

        # trovare un modo per far comparire nelle etichette del grafico
         
            

        # traccio i grafici e ottengo il javascript
        graph_PM10_title = "Serie storiche giornaliere del PM10 per "+area_di_interesse.Name
        graph_PM25_title = "Serie storiche giornaliere del PM2.5 per "+area_di_interesse.Name

        graph_PM10 = draw_timeserie_PM10_graph(time_values, PM10_values, PM10_daily_max_35_days_max=PM10_daily_max_35_days_max, graph_title=graph_PM10_title)
        graph_PM25 = draw_timeserie_PM25_graph(time_values, PM25_values, graph_title=graph_PM25_title)

        

        elementi_grafico = target_area_daily_time_serie(
                                                    # errore qui
                                                    Target_area_input_data = target_area_input_data.objects.get(Name=area_di_interesse.Name),

                                                    # questi sono vettori di valori

                                                    Record_time_values = '[' + ', '.join(str(e) for e in  serie_storica['Update_date'] ) +']',

                                                    PM10_mean_values = '[' + ', '.join(str(e) for e in  serie_storica['PM10_daily_mean'] ) +']',
                                                    PM25_mean_values = '[' + ', '.join(str(e) for e in  serie_storica['PM25_daily_mean'] ) +']',

                                                    PM10_quality_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM10_daily_quality'] ) +'"]',
                                                    PM25_quality_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM25_daily_quality'] ) +'"]',

                                                    PM10_cathegory_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM10_daily_cathegory'] ) +'"]',
                                                    PM25_cathegory_values = '["' + '", "'.join(str(e) for e in  serie_storica['PM25_daily_cathegory'] ) +'"]',

                                                    n_selected_sensors_values = '[' + ', '.join(str(e) for e in  serie_storica['Mean_n_selected_sensors'] ) +']',

                                                    PM10_graph_div = graph_PM10,
                                                    PM25_graph_div = graph_PM25,

                                                    )

        elementi_grafico.save()

        print("Predisposti dati ed elementi del grafico per la serie storica giornaliera per %s!" % area_di_interesse.Name)  

    print("Predisposti dati ed elementi dei grafici per le serie storiche giornaliere per tutte le località!")  