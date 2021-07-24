from discord.ext import tasks

import discord
import process_names

token = 'TOKEN HERE'
playerCap = '16'  # Change if max players is different


class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The current discord status of the bot
        self.currentServerInfo = ''

        # Start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=10)  # task runs every 10 seconds
    async def my_background_task(self):
        serverInfo = process_names.getServerInfo(playerCap)
        # Only change the bot status if we need to
        if(self.currentServerInfo != serverInfo):
            print(serverInfo)
            self.currentServerInfo = serverInfo
            gameInfo = discord.Game(self.currentServerInfo)
            # Change the bots status to show the server info
            await client.change_presence(status=discord.Status.idle, activity=gameInfo)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # Wait until the bot logs in


client = MyClient()
client.run(token)
