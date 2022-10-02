from datetime import datetime
from discord import Client, Message, ChannelType, Game, Status
from discord.ext import tasks

from classes.server import Server

import utils.process_runner as pr

import os, os.path

import jsonpickle

tokenFile = './token.txt'
configDir = './configs/'
pr.gameServerFile = '\"C:/Program Files (x86)/Steam/steamapps/common/blacklightretribution/Binaries/Win32/FoxGame-win32-Shipping-Patched-Server.exe\"'
token = open(tokenFile).readline()


class MyClient(Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        configFiles = [configFile for configFile in os.listdir(configDir) if os.path.isfile(os.path.join(configDir, configFile))]
        numConfigFiles = len(configFiles)
        if (numConfigFiles == 1):
            configFile = configDir + configFiles[0]
        elif (numConfigFiles > 1):
            print("Multiple config files detected, please select one:")
            for index, configFile in enumerate(configFiles):
                print(str(index+1) + ". " + configFile)
            configSelection = input("Please enter your selection (1-" + str(numConfigFiles) + "): ")
            while configSelection not in range(1, numConfigFiles+1):
                try:
                    configSelection = int(configSelection)
                    if configSelection not in range(1, numConfigFiles+1):
                        configSelection = input("Invalid Selection!\nPlease enter your selection: ")
                except:
                    configSelection = input("Invalid Selection!\nPlease enter your selection: ")
            configFile = configDir + "/" + configFiles[configSelection-1]

        self.Server = Server(configFile)
        self.currentServerInfo = 'NOT ONLINE'

        # Start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        self.Server.Start()

    @tasks.loop(seconds=5)  # task runs every 5 seconds
    async def my_background_task(self):
        serverInfo = self.Server.GetServerInfo()
        # Update the bot status if it has changed
        if(self.currentServerInfo != serverInfo):
            print(f'{datetime.now()}    {serverInfo}')
            self.currentServerInfo = serverInfo
            gameInfo = Game(self.currentServerInfo)

            fileName = '../output/server_info.json'
            data = self.Server.Info
            try:
                file = open(fileName, 'w')
                if file:
                    jsondata = jsonpickle.encode(data, unpicklable=False)
                    file.write(jsondata)
                    file.close()
            except Exception as e:
                print('Failed to write server_info.json')
                print(e)

            # Change the bots status to show the server info. This can only be done once every 15 seconds
            await client.change_presence(status=Status.idle, activity=gameInfo)

        if(self.Server.Starting == False and self.Server.Info.Map == 'Lobby' and self.Server.Options.AutoRestartInLobby == True):
            gameInfo = Game('RESTARTING')
            await client.change_presence(status=Status.idle, activity=gameInfo)
            self.Server.Restart()

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # Wait until the bot logs in

    async def on_message(self, message: Message):
        if(message.author == self.user):
            return

        if(message.channel.type != ChannelType.private):
            return

        await self.Server.Command(message)


client = MyClient()
client.run(token)
