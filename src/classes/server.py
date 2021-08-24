import json
from classes.gamemodes import getGamemode, isValidGamemode
from classes.items import Lists, Receivers
from classes.loadouts import Player, PlayerLoadouts
from classes.playlists import getPlaylist, isValidPlaylist
from classes.maps import getMapFileName, getMapName, isValidMap
from classes.commands import CommandType, getMessageType
from classes.server_structs import ServerOptions, ServerInfo
from discord.message import Message
from utils.process_runner import restartServer, startServer, get_hwnds_for_pid
from utils.process_names import getServerInfo
from utils.cheatengine_communication import scan_players, update_loadouts
from subprocess import Popen

class Server:

    def __init__(self, config: str = None):
        self.Options: ServerOptions = ServerOptions()
        self.Info: ServerInfo = ServerInfo()
        self.Process: Popen = None
        self.Hwnd: int = 0
        self.Starting: bool = True
        self.PlayerLoadouts: PlayerLoadouts = PlayerLoadouts.Load('loadouts.json')
        if(config != None):
            self.DefaultConfig = config
        else:
            self.DefaultConfig = './configs/server_config.json'
        if (self.LoadConfig(self.DefaultConfig)):
            print('Loaded configuration file {}'.format(self.DefaultConfig))

    def Start(self):
        self.Process = startServer(self.Options.LaunchOptions)
        self.Hwnd = get_hwnds_for_pid(self.Process.pid)[0]
        print("PID: " + str(self.Process.pid))
        print("HWND: " + str(self.Hwnd))
        self.Starting = False

    def GetServerInfo(self):
        if(self.Starting == True):
            return 'RESTARTING'
        self.Info = getServerInfo(self.Hwnd)
        if(self.Info.PlayerCount == -1):
            return '??/' + self.Options.LaunchOptions.MaxPlayers + ' | ' + self.Info.Map
        if(self.Info.Map == ''):
            return 'NOT ONLINE'
        return str(self.Info.PlayerCount) + '/' + str(self.Options.LaunchOptions.MaxPlayers) + ' | ' + self.Info.Map

    def Restart(self):
        self.Starting = True
        self.Process = restartServer(self.Options.LaunchOptions, self.Process)
        self.Hwnd = get_hwnds_for_pid(self.Process.pid)[0]
        self.Starting = False

    def SetMap(self, map):
        if(isValidMap(map)):
            self.Options.LaunchOptions.Map = map
            return True
        return False

    def SetBots(self, bots):
        try:
            newBots = int(bots)
            if(newBots < 0):
                newBots = 0
            if(newBots > 16):
                newBots = 16

            self.Options.LaunchOptions.BotCount = newBots
            return newBots
        except:
            return -1

    def SetPlaylist(self, playlist):
        if(isValidPlaylist(playlist)):
            self.Options.LaunchOptions.Playlist = playlist
            return True
        return False

    def SetGamemode(self, gamemode):
        if(isValidGamemode(gamemode)):
            self.Options.LaunchOptions.Gamemode = gamemode
            return True
        return False

    def SetSCP(self, scp):
        try:
            newSCP = int(scp)
            if(newSCP < 0):
                newSCP = 0
            if(newSCP > 999999):
                newSCP = 999999

            self.Options.LaunchOptions.SCP = newSCP
            return newSCP
        except:
            return -1

    def SetTimeLimit(self, timelimit):
        try:
            newTimeLimit = int(timelimit)
            if(newTimeLimit <= 0):
                newTimeLimit = None
            if(newTimeLimit > 999999):
                newTimeLimit = 999999

            self.Options.LaunchOptions.TimeLimit = newTimeLimit
            return newTimeLimit
        except:
            return -1

    def SetAutoRestart(self, autorestart: bool):
        try:
            self.Options.AutoRestartInLobby = autorestart
            return True
        except:
            return False

    def LoadConfig(self, configFile: str):
        options = ServerOptions.LoadFromFile(configFile)
        if(options != None):
            self.Options = options
            return True
        return False

    def ResetOptions(self):
        return self.LoadConfig(self.DefaultConfig)

    def ScanPlayers(self):
        if(self.Starting != True and self.Info.PlayerCount > 0):
            scan_players(self.Info.PlayerCount + self.Options.LaunchOptions.BotCount)
            #print('players')
        return

    def UpdateLoadouts(self):
        if(self.Starting != True and self.Info.PlayerCount > 0 and self.Info.Map != 'Lobby'):
            update_loadouts()
            #print('loadout')
        return

    def SetPrimary(self, playerName, receiverName):
        self.PlayerLoadouts[playerName] = receiverName

    def RegisterPlayer(self, discordId: int, playerName: str, receiverP1: str = 'Heavy Assault Rifle', receiverS1: str = 'Revolver', receiverP2: str = 'LMG-Recon', receiverS2: str = 'Machine Pistol', receiverP3: str = 'Combat Rifle', receiverS3: str = 'Heavy Pistol'):
        self.PlayerLoadouts.RegisterPlayerTemp(discordId, playerName, receiverP1, receiverS1, receiverP2, receiverS2, receiverP3, receiverS3)
        self.PlayerLoadouts.SaveLoadouts('loadouts.json')

    def RegisterLoadout(self, discordId: int, jsonLoadout: str):
        try:
            data = json.loads(jsonLoadout)
            player = Player.LoadFromJson(data) 
            result = self.PlayerLoadouts.RegisterPlayer(discordId, player)
            if(result == 0):
                self.PlayerLoadouts.SaveLoadouts('loadouts.json')
            return result
        except:
            return -1

    async def Command(self, message: Message):

        content: str = message.content
        discordId: int = message.author.id

        command: CommandType = getMessageType(content)

        listHelp = 'Lists items for customization. Usage: `list` or `list <list name>`'
        registerHelp = """Used to set player loadouts. Example usage:
```register 
{
    "DiscordId": 0,
    "PlayerName": "MagiCow",
    "Loadout1": {
        "Primary": {
            "Receiver": "M4X Rifle"
        },
        "Secondary": {
            "Receiver": "Revolver"
        }
    },
    "Loadout2": {
        "Primary": {
            "Receiver": "AK470 Rifle"
        },
        "Secondary": {
            "Receiver": "Heavy Pistol"
        }
    },
    "Loadout3": {
        "Primary": {
            "Receiver": "Combat Rifle"
        },
        "Secondary": {
            "Receiver": "Katana"
        }
    }
}```"""

        if(command not in self.Options.AllowedCommands):
            await message.channel.send("Command not enabled. Type help for available commands")
            return

        if(command == CommandType.Status):
            await message.channel.send(self.currentServerInfo)
            return

        if(command == CommandType.Help):
            parts = content.split(' ', 1)
            if(len(parts) == 1):
                response = 'Available commands:\n'
                for allowedCommand in self.Options.AllowedCommands:
                    response += '`' + allowedCommand.value + '`\n'
                response += 'For more detailed info on a command type: `help <command>`'
                await message.channel.send(response)
                return
            if(parts[1].lower() == 'register'):
                await message.channel.send(registerHelp)
                return
            if(parts[1].lower() == 'help'):
                await message.channel.send('Lists available commands and how to use them. Usage: `help` or `help <command>`')
                return
            if(parts[1].lower() == 'list'):
                await message.channel.send(listHelp)
                return

            await message.channel.send('Not a valid command')
            return

        if(command == CommandType.Restart):
            if(self.Info.PlayerCount != 0):
                await message.channel.send('Server is not empty, cannot restart.')
                return
            await message.channel.send('Restarting...')
            self.Restart()
            await message.channel.send('Restart complete!')
            return

        if(command == CommandType.Map):
            newMap = content.split(' ', 1)[1]
            mapFileName = getMapFileName(newMap)
            if(self.SetMap(mapFileName)):
                await message.channel.send('Map changed to ' + getMapName(mapFileName) + '. Restart for changes to take effect.')
                return

        if(command == CommandType.Bots):
            numberOfBots = int(content.split(' ', 1)[1])
            result = self.SetBots(numberOfBots)
            if(result != -1):
                await message.channel.send('Number of bots changed to ' + str(result) + '. Restart for changes to take effect.')
                return
            await message.channel.send('Number of bots should be a number between 0-16.')
            return

        if(command == CommandType.Playlist):
            playlistStr = content.split(' ', 1)[1]
            newPlaylist = getPlaylist(playlistStr)
            if(self.SetPlaylist(newPlaylist)):
                await message.channel.send('Playlist changed to ' + newPlaylist + '. Restart for changes to take effect.')
                return

        if(command == CommandType.Gamemode):
            gamemodeStr = content.split(' ', 1)[1]
            newGamemode = getGamemode(gamemodeStr)
            if(self.SetGamemode(newGamemode)):
                await message.channel.send('Gamemode changed to ' + newGamemode + '. Restart for changes to take effect.')
                return

        if(command == CommandType.SCP):
            scp = int(content.split(' ', 1)[1])
            result = self.SetSCP(scp)
            if(result != -1):
                await message.channel.send('Starting CP changed to ' + str(result) + '. Restart for changes to take effect.')
                return
            await message.channel.send('Starting CP should be a number between 0-999999.')
            return

        if(command == CommandType.TimeLimit):
            timeLimit = int(content.split(' ', 1)[1])
            result = self.SetTimeLimit(timeLimit)
            if(result != -1):
                await message.channel.send('TimeLimit changed to ' + str(result) + ' minutes. Restart for changes to take effect.')
                return
            await message.channel.send('TimeLimit should be a number between 0-999999.')
            return

        if(command == CommandType.AutoRestart):
            autorestart = bool(content.split(' ', 1)[1].lower == 'true')
            if(self.SetAutoRestart(autorestart)):
                await message.channel.send('Auto restart in lobby changed to ' + str(autorestart) + '.')
                return
            await message.channel.send('Auto restart should be true or false.')
            return

        if(command == CommandType.Reset):
            return self.ResetOptions()

        if(command == CommandType.Register):
            parts = content.split(' ', 1)
            if(len(parts) == 1):
                await message.channel.send(registerHelp)
                return
            json = parts[1]
            result = self.RegisterLoadout(discordId, json)
            if(result == 0):
                await message.channel.send('Loadout set successfully!')
                return
            if(result == -1):
                await message.channel.send('Invalid loadout!')
                return
            if(result == 1):
                await message.channel.send('Player name is already taken!')
                return
            return

        if(command == CommandType.List):
            parts = content.split(' ', 1)
            if(len(parts) == 1):
                response = listHelp + ' Available lists:\n'
                for list in Lists:
                    response += '`' +  list + '`\n'
                await message.channel.send(response)
                return
            if(parts[1].lower() == 'receivers'):
                response = ''
                for receiver in Receivers:
                    response += '`' + receiver + '`\n'
                await message.channel.send(response)
                return
            await message.channel.send('Not a valid list')
            return