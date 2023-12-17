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

import time


# declare functions
#######################
class RetrieveDataError(Exception):
    pass

class ParseDataError(Exception):
    pass

class Command(BaseCommand):
    def handle(self, *args, **options):

        self.stdout.write(self.style.WARNING('************** Starting simulator **************')) 
        self.stdout.write("")

        # get the pokemon data
        #----------------------

        # pokemon_identifier_input_1 = 'charmeleon'
        # pokemon_identifier_input_1 = 'metapod'
        # pokemon_identifier_input_1 = 'ditto'
        # pokemon_identifier_input_2 = 'ditto'
        # pokemon_identifier_input_2 = 'steelix'
        # pokemon_identifier_input_2 = 'ditto'

        last_selectable_pokemon_index = 352

        # pseudorandom extraction from “discrete uniform” distribution
        pokemon_identifier_input_1 = str(np.random.randint(1, last_selectable_pokemon_index))
        pokemon_identifier_input_2 = str(np.random.randint(1, last_selectable_pokemon_index))

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
        moveset.objects.all().delete()
        move.objects.all().delete()

        pokemon_model_ids = list()

        # get the pokemon main properties
        #---------------------------------  

        for pokemon_data in pokemon_data_list:        

            new_pokemon = pokemon(

                Name = pokemon_data['name'],
                Pokedex_id = pokemon_data['id'],

                Front_sprite_url = pokemon_data['sprites']['front_default'],
                Back_sprite_url = pokemon_data['sprites']['back_default']

            )
            
            new_pokemon.save()

            pokemon_model_ids.append(new_pokemon.id)

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


            # get the pokemon BATTLE stats
            #---------------------------------

            new_battle_stats_set = battle_stats_set(

                Pokemon = pokemon.objects.get(id=new_pokemon.id),

                HP = stats_dict['hp'],
                ATK = stats_dict['attack'],
                DEF = stats_dict['defense'],
                SPD = stats_dict['speed']

            )
            
            new_battle_stats_set.save()


            # get the pokemon moveset
            #-----------------------

            new_moveset = moveset(

                Pokemon = pokemon.objects.get(id=new_pokemon.id),

            )
            
            new_moveset.save()


            # get the pokemon moves
            #-----------------------

            # I need only 4 moves per pokemon

            max_moves_available = 4
            lenght_available_moves = len(pokemon_data['moves'])
            
            i = 0
            moves_indexes = []
            available_moves_indexes = list(range(lenght_available_moves))

            while len(moves_indexes) < max_moves_available and len(available_moves_indexes) > 0:
                move_index = random.choice(available_moves_indexes)
                moves_indexes.append(move_index)
                available_moves_indexes.remove(move_index)
                
                # let's suppose you get a pokemon like ditto or magikarp
                if i > max_moves_available:
                    break

                i = i+1


            for move_index in moves_indexes:

                move_url = pokemon_data['moves'][move_index]['move']['url']
        
            
                try:
                    # go grab the api
                    # move_api_request = requests.get(move_info_dict['url'])
                    move_api_request = requests.get(move_url)

                    # load as json il contenuto di api_request in 
                    move_api_data = json.loads(move_api_request.content)


                except:
                    print("Cannot retrieve the pokèmon moves information. Check that the identifier number in input are correct\n\n{}\n.".format(
                            move_url))
                    sys.exit(1)      


                # get the move attributes
                try:
                    move_description = move_api_data.get('effect_entries', "no_description")[0].get('effect', "no_description")
                except:
                    print("Cannot get elements in effect_entries.\n\n{}".format(move_api_data.get('effect_entries', "no_description")))
                    move_description = "no_description"
                
                move_power = move_api_data.get('power', 0)
                # turn to zero where power is none
                if not isinstance(move_power, int):
                    move_power = 0

                new_move = move(

                    Moveset = moveset.objects.get(id=new_moveset.id),

                    Name = move_api_data['name'],
                    Description = move_description,
                    Power = move_power

                )
                
                new_move.save()

        

        class Battle():
            def __init__(self, handle_stdout_attr, handle_style_attr, fighter_id, defender_id):

                self.stdout = handle_stdout_attr
                self.style = handle_style_attr

                self.fighter_id = fighter_id
                self.defender_id = defender_id

                self.fighter = dict()
                self.defender = dict()

                self.fighter['pokemon'] = pokemon.objects.get(id=self.fighter_id)
                self.defender['pokemon'] = pokemon.objects.get(id=self.defender_id)

                self.opponents = [ self.fighter, self.defender ]
                self.fixedorder_opponents = [ self.fighter, self.defender ]

                self.fighter['moveset'] = moveset.objects.get(Pokemon=self.fighter_id)
                self.defender['moveset'] = moveset.objects.get(Pokemon=self.defender_id)

                self.fighter['moves_list'] = move.objects.all().filter(Moveset=self.fighter['moveset'].id) # list
                self.defender['moves_list'] = move.objects.all().filter(Moveset=self.defender['moveset'].id) # list

                self.fighter['stats_set'] = stats_set.objects.get(Pokemon=self.fighter_id)
                self.defender['stats_set'] = stats_set.objects.get(Pokemon=self.defender_id)                

                self.fighter['battle_stats_set'] = battle_stats_set.objects.get(Pokemon=self.fighter_id)
                self.defender['battle_stats_set'] = battle_stats_set.objects.get(Pokemon=self.defender_id)  

                self.turn_count = None
                self.winner = None
                self.loser = None

                self.threshold_turn = 20


            def showdown(self):
                self.stdout.write(self.style.WARNING('************** Pokèmon battle showdown! **************')) 
                time.sleep(1)
                self.stdout.write("") 
                self.stdout.write('The battle is about to begin!')
                self.stdout.write('Here are the opponents:') 
                self.stdout.write("") 
                time.sleep(1)

                for opponent in self.opponents:
                    self.stdout.write("******************************") 

                    self.stdout.write("")          

                    self.stdout.write("Name:\t{}".format(opponent['pokemon'].Name))
                    self.stdout.write("Pokèdex id:\t{}".format(opponent['pokemon'].Pokedex_id))
                    self.stdout.write("Picture:\t{}".format(opponent['pokemon'].Front_sprite_url))
                    self.stdout.write("player id:\t{}".format(opponent['pokemon'].id))

                    self.stdout.write("")

                    self.stdout.write("\tMoveset:")
                    self.stdout.write("\t-----------------")

                    for opponent_move in opponent['moves_list']:
                        self.stdout.write("\t- {}\n\t\tPower: {}".format(opponent_move.Name, opponent_move.Power))

                    self.stdout.write("")

                    self.stdout.write("\tStats:")
                    self.stdout.write("\t-----------------")

                    self.stdout.write("\t- HP:\t{}".format(opponent['stats_set'].HP))
                    self.stdout.write("\t- ATK:\t{}".format(opponent['stats_set'].ATK))
                    self.stdout.write("\t- DEF:\t{}".format(opponent['stats_set'].DEF))
                    self.stdout.write("\t- SPD:\t{}".format(opponent['stats_set'].SPD))

                    self.stdout.write("")

                    time.sleep(3)
            
            def show_status(self):
                self.stdout.write("")
                self.stdout.write("- - - - - - - battle status - - - - - - -") 
                self.stdout.write("Turn number: {}".format(self.turn_count)) 
                for opponent in self.fixedorder_opponents:
                    self.stdout.write("Name: {}\tHP: {}".format(opponent['pokemon'], opponent['battle_stats_set'].HP) )
                self.stdout.write("- - - - - - - - - - - - - - - - - - - - - ")
                self.stdout.write("")
                time.sleep(1)

            def ends_win(self):
                self.stdout.write("")
                self.stdout.write(self.style.SUCCESS('************** Battle Ends! **************')) 
                self.stdout.write("")
                self.show_status()
                self.stdout.write("")
                self.stdout.write("The winner is {} !!!".format(self.winner['pokemon']))
                time.sleep(1)

            def ends_draw(self):
                self.stdout.write("")
                self.stdout.write(self.style.NOTICE('************** Battle Ends! **************')) 
                self.stdout.write("")
                self.show_status()
                self.stdout.write("")
                self.stdout.write("This is a draw.\n{} turns have passed but nobody has won.".format(self.turn_count))
                self.stdout.write("")
                time.sleep(1)

            def begin(self):
                self.stdout.write("")
                self.stdout.write(self.style.NOTICE('************** Battle begin! **************')) 
                self.stdout.write("")
                time.sleep(1)

                self.turn_count = 0

                
                while True:

                    self.turn_count = self.turn_count + 1

                    self.show_status()

                    self.stdout.write("It's {} turn.".format(self.opponents[0]['pokemon'].Name))

                
                    selected_move = random.choice(self.opponents[0]['moves_list'])

                    self.stdout.write("{} uses {}.".format(self.opponents[0]['pokemon'].Name, selected_move.Name))

                    # do the damage to the enemy
                    adjustment_factor = 0.25
                    caculated_damage = round( ( self.opponents[0]['battle_stats_set'].ATK / self.opponents[1]['battle_stats_set'].DEF ) * selected_move.Power * adjustment_factor )

                    # enemy_s_HPs = self.opponents[1]['battle_stats_set'].HP
                    self.opponents[1]['battle_stats_set'].HP = max(0, self.opponents[1]['battle_stats_set'].HP - caculated_damage) # HPs cannot go below 0
                    self.opponents[1]['battle_stats_set'].save()

                    self.stdout.write("{} loses {} HPs !".format(self.opponents[1]['pokemon'], caculated_damage))


                    # battle termination conditions
                    #--------------------------------

                    if self.opponents[1]['battle_stats_set'].HP == 0:
                        self.winner = self.opponents[0]
                        self.loser = self.opponents[1]
                        self.ends_win()
                        
                        break

                    elif self.turn_count == self.threshold_turn and self.opponents[1]['battle_stats_set'].HP != 0:
                        self.ends_draw()
                        
                        break
                    
                    self.opponents.reverse()




                    



                    # seleziona mossa
                
                    # sottrai ad hp ma non sotto zero
                
                    # hp =0 ?
                
                    # se sì -> battle end, winner is

        # opponents: list of dicts
        # opponent['<model_name>'].object_attribute

        battle = Battle(self.stdout, self.style, *pokemon_model_ids)

        battle.showdown()

        battle.begin()

