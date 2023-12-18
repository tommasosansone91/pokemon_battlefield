# python manage.py fight


# import modules
####################

import os, sys

import json
import requests

import random
import numpy as np

from .models import pokemon
from .models import moveset, battle_stats_set, stats_set
from .models import move

import time

from django.http import JsonResponse

# declare functions
#######################
class RetrieveDataError(Exception):
    pass

class ParseDataError(Exception):
    pass
    
# path('api/launch_battle/<int:pkmn_id2>/<int:pkmn_id1>', api.launch_battle, name="launch_battle"),
def launch_battle(request, pkmn_id1, pkmn_id2):
    print("")
    print('************** Starting simulator **************') 
    print("")

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
    # pokemon_identifier_input_1 = str(np.random.randint(1, last_selectable_pokemon_index))
    # pokemon_identifier_input_2 = str(np.random.randint(1, last_selectable_pokemon_index))

    pokemon_identifier_input_1 = str(pkmn_id1)
    pokemon_identifier_input_2 = str(pkmn_id2)

    print("Got an external request with parameters {}, {}:".format(pokemon_identifier_input_1, pokemon_identifier_input_2))
    print("api/launch_battle/{}/{}".format(pokemon_identifier_input_1, pokemon_identifier_input_2))

    pokemon_identifier_input_1 = pokemon_identifier_input_1.lower()
    pokemon_identifier_input_2 = pokemon_identifier_input_2.lower()

    POKEMON_ID_ROOT_URL = 'https://pokeapi.co/api/v2/pokemon/'
    # argument can be id or name

    # url generating
    pokemon_1_id_api_URL = os.path.join(POKEMON_ID_ROOT_URL, pokemon_identifier_input_1)
    pokemon_2_id_api_URL = os.path.join(POKEMON_ID_ROOT_URL, pokemon_identifier_input_2)

    print("Asking the pokèmon data to http://pokeapi.com/ ")
    print(pokemon_1_id_api_URL)
    print(pokemon_2_id_api_URL)
    print("Please wait... ")

        
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
        print("Cannot retrieve the pokèmon information. Check that the names you typed in input are correct\n\n{}\n{}\n.".format(pokemon_identifier_input_1, pokemon_identifier_input_2))
        sys.exit(1)


    print("Data correctly received!")
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

            print("Asking the move data to http://pokeapi.com/ ")
            print(move_url)
            print("Please wait... ")

        
            try:
                # go grab the api
                # move_api_request = requests.get(move_info_dict['url'])
                move_api_request = requests.get(move_url)

                # load as json il contenuto di api_request in 
                move_api_data = json.loads(move_api_request.content)


            except:
                print("Cannot retrieve the pokèmon moves information. Check that the identifier number in input are correct\n\n{}\n.".format(move_url))
                sys.exit(1)      


            # get the move attributes
            #--------------------------

            # name
            move_name = move_api_data['name']    

            # description
            try:
                move_description = move_api_data.get('effect_entries', "no_description")[0].get('effect', "no_description")
            except:
                print("Cannot find any element in effect_entries:\n{}\nAssigning value NO_DESCRIPTION to the move {}".format(move_api_data.get('effect_entries', "no_description"), move_name))
                
                move_description = "NO_DESCRIPTION"
            
            # power
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
        def __init__(self, fighter_id, defender_id):

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
            print("")
            print('************** Pokèmon battle showdown! **************') 
            time.sleep(1)
            print("") 
            print('The battle is about to begin!')
            print('Here are the opponents:') 
            print("") 
            time.sleep(1)

            for opponent in self.opponents:
                print("******************************") 

                print("")          

                print("Name:\t{}".format(opponent['pokemon'].Name))
                print("Pokèdex id:\t{}".format(opponent['pokemon'].Pokedex_id))
                print("Picture:\t{}".format(opponent['pokemon'].Front_sprite_url))
                print("player id:\t{}".format(opponent['pokemon'].id))

                print("")

                print("\tMoveset:")
                print("\t-----------------")

                for opponent_move in opponent['moves_list']:
                    print("\t- {}\n\t\tPower: {}".format(opponent_move.Name, opponent_move.Power))
                    pass

                print("")

                print("\tStats:")
                print("\t-----------------")

                print("\t- HP:\t{}".format(opponent['stats_set'].HP))
                print("\t- ATK:\t{}".format(opponent['stats_set'].ATK))
                print("\t- DEF:\t{}".format(opponent['stats_set'].DEF))
                print("\t- SPD:\t{}".format(opponent['stats_set'].SPD))

                print("")

                time.sleep(3)
        
        def show_status(self):
            print("")
            print("- - - - - - - battle status - - - - - - -") 
            print("Turn number: {}".format(self.turn_count)) 
            for opponent in self.fixedorder_opponents:
                print("Name: {}\tHP: {}".format(opponent['pokemon'], opponent['battle_stats_set'].HP) )
                pass
            print("- - - - - - - - - - - - - - - - - - - - - ")
            print("")
            time.sleep(1)

        def ends_win(self):
            print("")
            print('************** Battle Ends! **************') 
            print("")
            time.sleep(1)
            self.show_status()
            print("")
            print("The winner is {} !!!".format(self.winner['pokemon']))
            print("")
            

        def ends_draw(self):
            print("")
            print('************** Battle Ends! **************') 
            print("")
            time.sleep(1)
            self.show_status()
            print("")
            print("This is a draw.\n{} turns have passed but nobody has won.".format(self.turn_count))
            print("")
            time.sleep(1)

        def begin(self):
            print("")
            print('************** Battle begins! **************') 
            print("")
            time.sleep(1)

            self.turn_count = 0

            
            while True:

                self.turn_count = self.turn_count + 1

                self.show_status()

                print("It's {} turn.".format(self.opponents[0]['pokemon'].Name))

            
                selected_move = random.choice(self.opponents[0]['moves_list'])

                print("{} uses {}.".format(self.opponents[0]['pokemon'].Name, selected_move.Name))

                # do the damage to the enemy
                adjustment_factor = 0.25
                caculated_damage = round( ( self.opponents[0]['battle_stats_set'].ATK / self.opponents[1]['battle_stats_set'].DEF ) * selected_move.Power * adjustment_factor )

                # enemy_s_HPs = self.opponents[1]['battle_stats_set'].HP
                self.opponents[1]['battle_stats_set'].HP = max(0, self.opponents[1]['battle_stats_set'].HP - caculated_damage) # HPs cannot go below 0
                self.opponents[1]['battle_stats_set'].save()

                print("{} loses {} HPs !".format(self.opponents[1]['pokemon'], caculated_damage))


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



    # battle = Battle(*pokemon_model_ids)
    battle = Battle(pokemon_model_ids[0], pokemon_model_ids[1])

    battle.showdown()

    battle.begin()

    response = JsonResponse({})

    return response