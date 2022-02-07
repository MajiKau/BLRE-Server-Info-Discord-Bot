from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import jsonpickle
import pandas as pd
import ast
from classes.loadouts import Player, PlayerLoadouts

app = Flask(__name__)
api = Api(app)

playerLoadouts = PlayerLoadouts.Load('loadouts.json')

class AllPlayersAPI(Resource): # '/api/players/all'
    def get(self):
        jsondata = jsonpickle.encode(playerLoadouts.Loadouts, unpicklable=False)
        data = jsonpickle.decode(jsondata)
        return data, 200  # return data and 200 OK code

class PlayersAPI(Resource): # '/api/players?playerName=<playerName>'
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('playerName')
        args = parser.parse_args()
        playerName = args['playerName']
        remoteIP = request.remote_addr

        players = playerLoadouts.FindPlayer(remoteIP, playerName)
        jsondata = jsonpickle.encode(players, unpicklable=False)
        data = jsonpickle.decode(jsondata)

        return data, 200  # return data and 200 OK code

    def post(self):
        remoteIP = request.remote_addr
        data = request.json
        errors = PlayerLoadouts.GetJSONErrors(data)

        if(errors != ""):
            return {"errors": errors}, 400

        try:
            player = Player.LoadFromJson(data) 
            result = playerLoadouts.RegisterPlayerAPI(player, remoteIP)
            if(result == ''):
                playerLoadouts.SaveLoadouts('loadouts.json')
                print('Success!')
                return {'message': 'Player saved!'}, 200
            else:
                print('Fail!')
                print(result)
                return {'errors': result}, 200
        except:
            return {'errors': 'Unknown error! Something went wrong with setting your loadout.'}, 400

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('playerName')
        args = parser.parse_args()
        playerName = args['playerName']
        remoteIP = request.remote_addr

        result = playerLoadouts.RemovePlayer(remoteIP, playerName)

        if(result):
            return {'message': 'Player deleted'}, 200
        return {'error': 'Player not found'}, 200

api.add_resource(AllPlayersAPI, '/api/players/all')
api.add_resource(PlayersAPI, '/api/players')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)  # run our Flask app
    # app.run(host='0.0.0.0', port=7778)  # run our Flask app