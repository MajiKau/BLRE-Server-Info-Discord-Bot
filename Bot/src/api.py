# import json
from flask import Flask, request
from flask_restful import Resource, Api
import jsonpickle
# import pandas as pd
# import ast
from classes.maps import getMapName
from waitress import serve

app = Flask(__name__)
api = Api(app)

class InfoAPI(Resource):
    def get(self):
        fileName = 'C:/Program Files (x86)/Steam/steamapps/common/blacklightretribution/FoxGame/Config/BLRevive/server_utils/server_info.json'
        data = '{"PlayerCount": 0, "Map": "??", "PlayerList": []}'
        try:
            file = open(fileName)
            if file:
                jsondata = file.read()
                data = jsonpickle.decode(jsondata)
                data["Map"] = getMapName(data["Map"])
        except Exception as e:
            print('Failed to read server_info.json')
            print(e)
        return data, 200

api.add_resource(InfoAPI, '/api/server')

if __name__ == '__main__':
    #app.run(debug=False, host='0.0.0.0', port=80)  # run our Flask app
    serve(app, host='0.0.0.0', port=80)

    # app.run(host='0.0.0.0', port=7778)  # run our Flask app