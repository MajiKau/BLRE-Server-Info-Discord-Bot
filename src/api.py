from distutils.log import error
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
from classes.loadouts import Player, PlayerLoadouts

app = Flask(__name__)
api = Api(app)

playerLoadouts = PlayerLoadouts.Load('loadouts.json')

class Items(Resource):
    def get(self):
        # data = pd.read_json('items.json')  # read CSV
        # data = data.to_dict()  # convert dataframe to dictionary
        # return {'data': data}, 200  # return data and 200 OK code
        return {'data': "Woah"}, 200  # return data and 200 OK code
    
class Loadout(Resource):
    def post(self):
        data = request.json
        errors = ""

        requiredPlayerKeys = [
            'PlayerName'
        ]

        requiredLoadouts = [
            'Loadout1',
            'Loadout2',
            'Loadout3'
        ]

        requiredLoadoutKeys = [
            'Primary',
            'Secondary'
        ]

        requiredWeaponKeys = [
            'Receiver'
        ]
        for playerKey in requiredPlayerKeys:
            if(playerKey not in data):
                errors += playerKey + ' not found!\n'

        for loadout in requiredLoadouts:
            if(loadout not in data):
                errors += loadout + ' not found!\n'
            else:
                for loadoutKey in requiredLoadoutKeys:
                    if(loadoutKey not in data[loadout]):
                        errors += loadoutKey + ' not found in ' + loadout + '!\n'
                    else:
                        for weaponKey in requiredWeaponKeys:
                            if(weaponKey not in data[loadout][loadoutKey]):
                                errors += weaponKey + ' not found in ' + loadout + ' ' + loadoutKey + '!\n'

        if(errors != ""):
            return {"errors": errors}, 400

        try:
            player = Player.LoadFromJson(data) 
            result = playerLoadouts.RegisterPlayer(0, player)
            if(result == ''):
                playerLoadouts.SaveLoadouts('loadouts.json')
                print('Success!')
                return {'message': 'Loadout set successfully!'}, 200
            else:
                print('Fail!')
                print(result)
                return {'errors': result}, 200
        except:
            return {'errors': 'Unknown error! Something went wrong with setting your loadout.'}, 400


api.add_resource(Items, '/items')  # '/users' is our entry point for Users
api.add_resource(Loadout, '/loadout')  # and '/locations' is our entry point for Locations

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7778)  # run our Flask app