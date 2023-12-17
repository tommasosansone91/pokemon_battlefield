# questo file lo richiamo solo se c'e l'ho in 
# app/management/commands/nome_file.py
# la linea from django.core.management.base import BaseCommand
# l'intestazione
# class Command(BaseCommand):
#     def handle(self, *args, **options):

# python manage.py fight


# import modules
####################

import os, sys
from django.core.management.base import BaseCommand

import json
import requests

import random
import numpy as np

from app_battle_simulator.models import pokemon
from app_battle_simulator.models import moveset, battle_stats_set, stats_set
from app_battle_simulator.models import move


# declare functions
#######################
class RetrieveDataError(Exception):
    pass

class Command(BaseCommand):
    def handle(self, *args, **options):

        # get the pokemon data
        #----------------------

        # pokemon_identifier_input_1 = 'charmeleon'
        # pokemon_identifier_input_2 = 'steelix'

        pokemon_identifier_input_1 = str(np.random.randint(1, 151))
        pokemon_identifier_input_2 = str(np.random.randint(1, 151))

        pokemon_identifier_input_1 = pokemon_identifier_input_1.lower()
        pokemon_identifier_input_2 = pokemon_identifier_input_2.lower()

        POKEMON_ID_ROOT_URL = 'https://pokeapi.co/api/v2/pokemon/'
        # argument can be id or name

        # url generating
        pokemon_1_id_api_URL = os.path.join(POKEMON_ID_ROOT_URL, pokemon_identifier_input_1)
        pokemon_2_id_api_URL = os.path.join(POKEMON_ID_ROOT_URL, pokemon_identifier_input_2)
    
         
        try:
            # go grab the api
            pokemon_1_api_request = requests.get(pokemon_1_id_api_URL)
            pokemon_2_api_request = requests.get(pokemon_2_id_api_URL)

            # load as json il contenuto di api_request in 
            pokemon_1_api_data = json.loads(pokemon_1_api_request.content)
            pokemon_2_api_data = json.loads(pokemon_2_api_request.content)


        except:
        # except Exception as e:
            # raise RetrieveDataError(
            #     "Cannot retreve the pokèmon information. Check that the names you typed in input are correct\n\n{}\n{}\n.".format(
            #         pokemon_identifier_input_1, pokemon_identifier_input_2))
            print("Cannot retrieve the pokèmon information. Check that the names you typed in input are correct\n\n{}\n{}\n.".format(
                    pokemon_identifier_input_1, pokemon_identifier_input_2))
            sys.exit(1)

        
        # print('\n\n', pokemon_1_api_data,'\n\n', pokemon_2_api_data)

        pokemon_data_list = [ pokemon_1_api_data , pokemon_2_api_data ]


        # clear the models
        pokemon.objects.all().delete()
        battle_stats_set.objects.all().delete()
        stats_set.objects.all().delete()
        # moveset.objects.all().delete()
        # move.objects.all().delete()

        # get the pokemon main properties
        #---------------------------------  

        for pokemon_data in pokemon_data_list:        

            new_pokemon = pokemon(

                Name = pokemon_data['name'],
                Pokedex_id = pokemon_data['id'],

                front_sprite_url = pokemon_data['sprites']['front_default'],
                back_sprite_url = pokemon_data['sprites']['back_default']

            )
            
            new_pokemon.save()

            # get the pokemon stats
            #--------------------------------- 
            
            # stats_list = [
            #     {
            #         'stat_name': stat['stat']['name'],
            #         'stat_value': stat['base_stat']
            #     }
            #     for stat in pokemon_data['stats']
            # ]      

            stats_dict = dict()
            for stat in pokemon_data['stats']:
                stats_dict[stat['stat']['name']] = stat['base_stat']


            new_stats_set = stats_set(

                Pokemon = pokemon.objects.get(id=new_pokemon.id),

                HP = stats_dict['hp'],
                ATK = stats_dict['attack'],
                DEF = stats_dict['defense'],
                SPD = stats_dict['speed']

            )
            
            new_stats_set.save()


            new_battle_stats_set = battle_stats_set(

                Pokemon = pokemon.objects.get(id=new_pokemon.id),

                HP = stats_dict['hp'],
                ATK = stats_dict['attack'],
                DEF = stats_dict['defense'],
                SPD = stats_dict['speed']

            )
            
            new_battle_stats_set.save()



        # get the pokemon stats
        #-----------------------

        # new_record = target_area_realtime_data(
        #                                         Target_area_name=target_area_input_data.objects.get(Name=place_name),
        #                                         Last_update_time=record_time,

        #                                         PM10_mean=PM10_mean,
        #                                         PM25_mean=PM25_mean,

        #                                         PM10_quality=PM10_quality, 
        #                                         PM25_quality=PM25_quality,

        #                                         PM10_cathegory=PM10_cathegory,
        #                                         PM25_cathegory=PM25_cathegory,

        #                                         n_selected_sensors=n_selected_sensors,
        # )
        
        # new_record.save()








        self.stdout.write(self.style.SUCCESS('*** Battle finished! ***')) 