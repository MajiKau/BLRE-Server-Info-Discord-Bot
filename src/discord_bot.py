from discord import Client, Message, ChannelType, Game, Status
from discord.ext import tasks

from classes.server import Server

import utils.process_runner as pr

tokenFile = './token.txt'
configFile = './configs/server_config.json'
pr.gameServerFile = '\"C:/Program Files (x86)/Steam/steamapps/common/blacklightretribution/Binaries/Win32/FoxGame-win32-Shipping-Patched-Server.exe\"'
token = open(tokenFile).readline()


class MyClient(Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.Server = Server(configFile)  # TODO: List configs in folder and let user select one
        self.currentServerInfo = 'NOT ONLINE'

        # Start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        self.Server.Start()
        self.backgroundTask30.start()
        self.backgroundTask5.start()

    @tasks.loop(seconds=5)  # task runs every 5 seconds
    async def my_background_task(self):
        serverInfo = self.Server.GetServerInfo()
        # Update the bot status if it has changed
        if(self.currentServerInfo != serverInfo):
            print(serverInfo)
            self.currentServerInfo = serverInfo
            gameInfo = Game(self.currentServerInfo)

            # Change the bots status to show the server info. This can only be done once every 15 seconds
            await client.change_presence(status=Status.idle, activity=gameInfo)

        if(self.Server.Starting == False and self.Server.Info.Map == 'Lobby' and self.Server.Options.AutoRestartInLobby == True):
            gameInfo = Game('RESTARTING')
            await client.change_presence(status=Status.idle, activity=gameInfo)
            self.Server.Restart()

    @tasks.loop(seconds=1)
    async def backgroundTask5(self):
        self.Server.UpdateLoadouts()

    @tasks.loop(seconds=30)
    async def backgroundTask30(self):
        self.Server.ScanPlayers()

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
