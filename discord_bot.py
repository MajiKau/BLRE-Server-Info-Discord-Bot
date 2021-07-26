from discord.ext import tasks

import discord
import process_names

tokenFile = 'token.txt'
token = open(tokenFile).readline()
playerCap = '16'  # Change if max players is different


class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The current discord status of the bot
        self.currentServerInfo = ''

        # The current game server process ID
        self.currentServerProcess = 0

        # Start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        # Try to find the server process
        self.currentServerProcess = process_names.pickServer()
        if(self.currentServerProcess != 0):
            print('Server process ID: ' + str(self.currentServerProcess))
        else:
            print('Server process not found, will retry')

    @tasks.loop(seconds=5)  # task runs every 5 seconds
    async def my_background_task(self):

        # Try to find the server process if it hasn't been found yet
        if(self.currentServerProcess == 0):
            self.currentServerProcess = process_names.pickServer()
            if(self.currentServerProcess != 0):
                print('Server process ID: ' + str(self.currentServerProcess))
            else:
                print('Server process not found, will retry')

        if(self.currentServerProcess != 0):
            serverInfo = process_names.getServerInfo(
                self.currentServerProcess, playerCap)
            # Update the bot status if it has changed
            if(self.currentServerInfo != serverInfo):
                print(serverInfo)
                self.currentServerInfo = serverInfo
                gameInfo = discord.Game(self.currentServerInfo)
                # Change the bots status to show the server info. This can only be done once every 15 seconds
                await client.change_presence(status=discord.Status.idle, activity=gameInfo)

            # If the server process ID doesn't work anymore, find a new one
            if(self.currentServerInfo == 'NOT ONLINE'):
                print('Server process has gone offline, will try to find new one')
                self.currentServerProcess = 0

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # Wait until the bot logs in


client = MyClient()
client.run(token)
