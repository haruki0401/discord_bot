import os # to hide token
import urllib.request
import json

import traceback


#key
from key import RIOT_TOKEN

API_KEY = "api_key=" + RIOT_TOKEN

class Riot_api:

    #def __init__(self,)

    def getID(self, sn: str):
        SN = urllib.parse.quote(sn)

        # get summonerID
        try:
            SUMMONER_V4 = "https://jp1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
            s = urllib.request.urlopen(SUMMONER_V4 + SN + '?' + API_KEY)
            summoner_array = json.loads(s.read().decode('utf-8'))
            s.close()
            SID = summoner_array["id"]
            print("SID: "+SID)

            return SID

        
        except urllib.error.HTTPError as err:
            if err.code == 401:
                print("RIOT api_token is not correct.")
                return "401"
            elif err.code == 404:
                print("The Summoner Name you entered does not exist.")
                return "404"
        

        except: # need more strict direction later

            traceback.print_exc()
            print("Something error!")

            return "-1"


    def getRank(self, SID: str):
        try:
            LEAGUE_V4 = "https://jp1.api.riotgames.com/lol/league/v4/positions/by-summoner/"
            r = urllib.request.urlopen(LEAGUE_V4 + SID+ '?' + API_KEY)
            rank_array = json.loads(r.read().decode('utf-8'))
            r.close()

            solo_array = -1
            flex_array = -1

            for index, array in enumerate(rank_array):
                if array["queueType"] == "RANKED_SOLO_5x5":
                    solo_array = index
                
                elif array["queueType"] == "RANKED_FLEX_SR":
                    flex_array = index
            

            SOLO_RANK = "UNRANKED"
            FLEX_RANK = "UNRANKED"

            if solo_array != -1:
                SOLO_RANK = rank_array[solo_array]["tier"] + " " + rank_array[solo_array]["rank"]

            if flex_array != -1:
                FLEX_RANK = rank_array[flex_array]["tier"] + " " + rank_array[flex_array]["rank"]

            return SOLO_RANK, FLEX_RANK

        except:
            print("Something error!")   
            traceback.print_exc()
            return '-1'         

    def currentGame(self,SID : str):
        try:
            SPECTATOR_V4 = "https://jp1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/"
            r = urllib.request.urlopen(SPECTATOR_V4 + SID+ '?' + API_KEY)
            game_array = json.loads(r.read().decode('utf-8'))
            r.close()

            gameMode = game_array["gameQueueConfigId"]


            GAME_MODE = None

            if gameMode == 420:
                GAME_MODE = "Solo Rank"
            elif gameMode == 430:
                GAME_MODE = "Nomal"
            elif gameMode == 440:
                GAME_MODE = "Flex Rank"
            else:
                return "OTHER" #other game mode

            PLAYERS = game_array["participants"]

            BANNS = game_array["bannedChampions"] 

            TIME = game_array["gameLength"]

            return {'GAME_MODE':GAME_MODE, 'PLAYERS':PLAYERS, 'BANNS':BANNS, 'TIME':TIME}

        except urllib.error.HTTPError as err:
            if err.code == 404:
                print("This Summoner is not in game.")
                return "404"


        except:
            print("Something error!")   
            traceback.print_exc()
            return '-1'        