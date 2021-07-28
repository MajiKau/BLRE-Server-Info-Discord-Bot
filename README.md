# BLRE-Server-Info-Discord-Bot
Discord bot that shows the player count and current map in its status.

Only tested on Windows 10 and Python 3.8.

Required Python modules:
* discord (https://discordpy.readthedocs.io/en/stable/intro.html#installing `pip install -U discord.py`)
* win32gui (https://pypi.org/project/pywin32/ `pip install pywin32`)

1. Make a discord bot and invite it to a channel. https://discordpy.readthedocs.io/en/stable/discord.html
2. Add server information to the bot's description
3. Set your bot token in <i>discord_bot.py</i>
4. Make sure your BLR server is running
5. Run <i>discord_bot.py</i> (Must be run on the same machine as the game server)

The bot will now update its status every 10 seconds.

Example of how the bot can look like:

![image](https://user-images.githubusercontent.com/25136341/127382678-c9b93f34-c9c3-49b3-a7ea-2133bd9f31fa.png)
