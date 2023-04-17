# BLRE-Server-Info-Discord-Bot

Discord bot that shows the player count, game mode and current map in its status.

Required Python modules:
* discord (https://discordpy.readthedocs.io/en/stable/intro.html#installing `pip install -U discord.py`)
* win32gui (https://pypi.org/project/pywin32/ `pip install pywin32`)
* some other stuff

1. Make a discord bot and invite it to a channel. https://discordpy.readthedocs.io/en/stable/discord.html I recommend creating your own discord channel and testing there first.
2. Add server information to the bot's description
3. Set your bot token in <i>src/token.txt</i>
4. If BLR isn't installed in <i>C:/Program Files (x86)/Steam/steamapps/common/blacklightretribution</i> update serverConfigFileOutput in <i>src/discord_bot.py</i> and .json files in Configs folder
5. Copy BLREdit to the BLREdit folder
6. Run <i>run.bat</i> or <i>discord_bot.py</i> from the src folder `py ./discord_bot.py`