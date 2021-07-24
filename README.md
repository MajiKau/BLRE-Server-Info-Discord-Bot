# BLRE-Server-Info-Discord-Bot
Discord bot that shows the player count and current map in its status
Only tested on Windows 10

Required Python modules:
* discord https://discordpy.readthedocs.io/en/stable/intro.html#installing
* win32gui (pip install pywin32)

1. Make a discord bot and invite it to a channel https://discordpy.readthedocs.io/en/stable/discord.html
2. Set your bot token in discord_bot.py
3. Make sure BLR server is running
4. Run discord_bot.py (Must be run on the same machine as the game server)
The bot will now update its status every 10 seconds
