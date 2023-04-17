from datetime import datetime
import json
from subprocess import Popen
from discord import Client, Game, Status
from discord.ext import tasks
from classes.config import Config
from classes.maps import getMapName

from utils.process_names import getServerOnline, getWatchdogOnline

import os, os.path

import sys, shutil, logging

logging.basicConfig(filename='log.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Started logging...")

tokenFile = './token.txt'
configDir = '../../Configs/'
serverConfigDir = '../../Configs/server_utils/'
serverConfigFileOutput = 'C:/Program Files (x86)/Steam/steamapps/common/blacklightretribution/FoxGame/Config/BLRevive/server_utils/server_config.json'
token = open(tokenFile).readline()

class MyClient(Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if (len(sys.argv) > 1):
            configFile = sys.argv[1]
        else:
            configFiles = [configFile for configFile in os.listdir(configDir) if os.path.isfile(os.path.join(configDir, configFile))]
            numConfigFiles = len(configFiles)
            if (numConfigFiles == 1):
                configFile = configDir + configFiles[0]
            elif (numConfigFiles > 1):
                logging.info("Multiple config files detected, please select one:")
                for index, configFile in enumerate(configFiles):
                    logging.info(str(index+1) + ". " + configFile)
                configSelection = input("Please enter your selection (1-" + str(numConfigFiles) + "): ")
                while configSelection not in range(1, numConfigFiles+1):
                    try:
                        configSelection = int(configSelection)
                        if configSelection not in range(1, numConfigFiles+1):
                            configSelection = input("Invalid Selection!\nPlease enter your selection: ")
                    except:
                        configSelection = input("Invalid Selection!\nPlease enter your selection: ")
                configFile = configDir + "/" + configFiles[configSelection-1]

        if (len(sys.argv) > 2):
            shutil.copyfile(sys.argv[2], serverConfigFileOutput)
        else:
            serverConfigFiles = [serverConfigFile for serverConfigFile in os.listdir(serverConfigDir) if os.path.isfile(os.path.join(serverConfigDir, serverConfigFile))]
            numServerConfigFiles = len(serverConfigFiles)
            if (numServerConfigFiles == 1):
                serverConfigFile = serverConfigDir + serverConfigFiles[0]
            elif (numServerConfigFiles > 1):
                logging.info("Multiple server_utils config files detected, please select one:")
                for index, serverConfigFile in enumerate(serverConfigFiles):
                    logging.info(str(index+1) + ". " + serverConfigFile)
                serverConfigSelection = input("Please enter your selection (1-" + str(numServerConfigFiles) + "): ")
                while serverConfigSelection not in range(1, numServerConfigFiles+1):
                    try:
                        serverConfigSelection = int(serverConfigSelection)
                        if serverConfigSelection not in range(1, numServerConfigFiles+1):
                            serverConfigSelection = input("Invalid Selection!\nPlease enter your selection: ")
                    except:
                        serverConfigSelection = input("Invalid Selection!\nPlease enter your selection: ")
                serverConfigFile = serverConfigDir + "/" + serverConfigFiles[serverConfigSelection-1]
            shutil.copyfile(serverConfigFile, serverConfigFileOutput)

        self.Config = Config.LoadFromFile(configFile)
        self.args = self.Config.BLREdit + " -server " + self.Config.LaunchOptionsFile

        # self.Server = Server(configFile)
        self.currentServerInfo = 'NOT ONLINE'
        self.hwnd = 0
        self.Starting = True


    async def on_ready(self):
        logging.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logging.info('------')

        # logging.info(self.args)
        logging.info(f'{datetime.now()}    {self.args}')
        Popen(self.args)

        # Start the task to run in the background
        self.my_background_task.start()

    @tasks.loop(seconds=5)  # task runs every 5 seconds
    async def my_background_task(self):
        serverInfo = "STARTING..."
        self.hwnd = getServerOnline(self.hwnd)

        if (self.hwnd != 0):
            self.Starting = False
            try:
                file = open(self.Config.ServerInfoFile)
                data = json.loads(file.read())
                serverInfo = str(data["PlayerCount"]) + ' | ' +  data["GameMode"] + ' ' + ' | ' + getMapName(data["Map"])
            except Exception as e:
                logging.info('Failed to read output file: {}'.format(self.Config.ServerInfoFile))
                logging.info(e)
                return None
        if (self.Starting == False and getWatchdogOnline(self.hwnd) == 0):
            serverInfo = "SERVER IS DOWN..."

        if self.currentServerInfo != serverInfo:
            self.currentServerInfo = serverInfo
            gameInfo = Game(self.currentServerInfo)
            await client.change_presence(status=Status.idle, activity=gameInfo)

        if (self.Starting == False and getWatchdogOnline(self.hwnd) == 0):
            self.close()
            exit(404)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # Wait until the bot logs in


client = MyClient()
client.run(token)