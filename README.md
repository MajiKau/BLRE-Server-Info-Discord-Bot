# BLRE-Server-Info-Discord-Bot
Discord bot that shows the player count and current map in its status.
Loadouts can be customized by sending the discord bot commands.

Only tested on Windows 10 and Python 3.8.

Required Python modules:
* discord (https://discordpy.readthedocs.io/en/stable/intro.html#installing `pip install -U discord.py`)
* win32gui (https://pypi.org/project/pywin32/ `pip install pywin32`)

1. Make a discord bot and invite it to a channel. https://discordpy.readthedocs.io/en/stable/discord.html I recommend creating your own discord channel and testing there first.
2. Add server information to the bot's description
3. Set your bot token in <i>src/token.txt</i>
4. Change the path to the game server executable in <i>src/discord_bot.py</i> if necessary
5. Run <i>discord_bot.py</i> from the src folder `py ./discord_bot.py`
6. Run <i>LoadoutChanger.exe</i> and click <i>Enable</i>

The bot will now update its status respond to commands such as <i>help</i>, <i>list</i> and <i>register</i>.

Example of how the bot can look like:

![image](https://user-images.githubusercontent.com/25136341/127382678-c9b93f34-c9c3-49b3-a7ea-2133bd9f31fa.png)
