import os # to hide token
import urllib.request
import json

API_KEY = "api_key=" + os.environ.get("RIOT_TOKEN")

class Riot_api:

    #def __init__(self,)

    def getID(self, sn:str):
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
        except: # need more strict direction later
            print("The Summoner Name you entered does not exist.")
            SID = "-1"

            return SID

