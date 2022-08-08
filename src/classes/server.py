import json
from classes.gamemodes import getGamemode, isValidGamemode
from classes.items import Barrels, Gear, Grips, Lists, Magazines, Muzzles, Receivers, Scopes, Stocks, Tactical
from classes.loadouts import Player, PlayerLoadouts
from classes.playlists import getPlaylist, isValidPlaylist
from classes.maps import getMapFileName, getMapName, isValidMap
from classes.commands import CommandType, getMessageType
from classes.server_structs import ServerOptions, ServerInfo
from discord.message import Message
from utils.process_runner import restartServer, startServer, get_hwnds_for_pid
from utils.process_names import getServerInfo
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
        if(self.Info.PlayerCount > self.Options.LaunchOptions.MaxPlayers):
            return '??/' + str(self.Options.LaunchOptions.MaxPlayers) + ' | ' + self.Info.Map
        if(self.Info.Map == ''):
            return 'NOT ONLINE'
        return self.Options.LaunchOptions.Playlist + ' ' + str(self.Info.PlayerCount) + '/' + str(self.Options.LaunchOptions.MaxPlayers) + ' | ' + self.Info.Map

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

    def RegisterLoadout(self, discordId: int, jsonLoadout: str):
        try:
            data = json.loads(jsonLoadout)

            errors = PlayerLoadouts.GetJSONErrors(data)
            if(errors != ''):
                return errors

            player = Player.LoadFromJson(data) 
            result = self.PlayerLoadouts.RegisterPlayer(discordId, player)
            if(result == ''):
                self.PlayerLoadouts.SaveLoadouts('loadouts.json')
                return 'Loadout set successfully!'
            else:
                return result
        except Exception as e:
            print(e)
            return 'Unknown error! Something went wrong with setting your loadout.'

    async def Command(self, message: Message):

        content: str = message.content
        discordId: int = message.author.id

        command: CommandType = getMessageType(content)

        listHelp = 'Lists items for customization. Usage: `list` or `list <list name>` Available lists:\n'
        for list in Lists:
            listHelp += '`' +  list + '`\n'
        registerHelp = """Used to set player loadouts. Use the `list` command to get available weapon parts. Example usage:
```register 
{
"PlayerName": "YourPlayerNameHere",
"Loadout1": {
"Primary": {
"Receiver": "Bullpup Full Auto",
"Muzzle": 1,
"Stock": "Silverwood z1200 BPFA",
"Barrel": "Hullbreach 047BAR",
"Magazine": 152,
"Scope": "Aim Point Ammo Counter",
"Grip": "",
"Camo": 12
},
"Secondary": {
"Receiver": "Snub 260",
"Muzzle": 0,
"Stock": "No Stock",
"Barrel": "No Barrel Mod",
"Magazine": 177,
"Scope": "No Optic Mod",
"Grip": "",
"Camo": 32
},
"Gear1": 15,
"Gear2": 25,
"Gear3": 5,
"Gear4": 6,
"Tactical": 1,
"Camo": 78,
"UpperBody": 6,
"LowerBody": 4,
"Helmet": 17,
"IsFemale": true,
"Skin":0,
"Trophy":1
},
"Loadout2": {
"Primary": {
"Receiver": "Combat Rifle",
"Muzzle": 3,
"Stock": "Krane Extender Stock",
"Barrel": "Silverwood Light Accuracy Barrel",
"Magazine": 24,
"Scope": "4X Ammo Counter Scope",
"Grip": "",
"Camo": 43
},
"Secondary": {
"Receiver": "Shotgun",
"Muzzle": 0,
"Stock": "Redsand Compensator Stock",
"Barrel": "Krane SG Bar-20",
"Magazine": 29,
"Scope": "EMI Infrared Scope",
"Grip": "Briar BrSGP1",
"Camo": 65
},
"Gear1": 7,
"Gear2": 8,
"Gear3": 9,
"Gear4": 10,
"Tactical": 6,
"Camo": 13,
"UpperBody": 5,
"LowerBody": 7,
"Helmet": 15,
"IsFemale": true,
"Skin":34,
"Trophy":2
},
"Loadout3": {
"Primary": {
"Receiver": "Assault Rifle",
"Muzzle": 2,
"Stock": "Taurex Stabilizing Stock",
"Barrel": "Briar Accuracy Barrel",
"Magazine": 14,
"Scope": "EMI Tech Scope",
"Grip": "",
"Camo": 73
},
"Secondary": {
"Receiver": "Heavy Pistol",
"Muzzle": 15,
"Stock": "Silverwood Compensator Stock",
"Barrel": "V2 Z900 Mod",
"Magazine": 48,
"Scope": "EMI Infrared Scope Mk. 2",
"Grip": "",
"Camo": 91
},
"Gear1": 11,
"Gear2": 12,
"Gear3": 13,
"Gear4": 14,
"Tactical": 4,
"Camo": 92,
"UpperBody": 2,
"LowerBody": 2,
"Helmet": 50,
"IsFemale": false,
"Skin":4294967296,
"Trophy":3
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
            parts = content.split('\n', 1)
            if(len(parts) == 1):
                await message.channel.send(registerHelp)
                return
            json = parts[1]
            result = self.RegisterLoadout(discordId, json)
            await message.channel.send(result)
            return

        if(command == CommandType.List):
            parts = content.split(' ', 1)
            if(len(parts) == 1):
                await message.channel.send(listHelp)
                return
            if(parts[1].lower() == 'receivers'):
                response = ''
                for item in Receivers:
                    response += '`' + item + '`\n'
                await message.channel.send(response)
                return
            if(parts[1].lower() == 'stocks'):
                response = ''
                for item in Stocks:
                    response += '`' + item + '`\n'
                await message.channel.send(response)
                return
            if(parts[1].lower() == 'barrels'):
                response = ''
                for item in Barrels:
                    response += '`' + item + '`\n'
                await message.channel.send(response)
                return
            if(parts[1].lower() == 'scopes'):
                response = ''
                for item in Scopes:
                    response += '`' + item + '`\n'
                await message.channel.send(response)
                return
            if(parts[1].lower() == 'muzzles'):
                response = ''
                for item in Muzzles:
                    response += '`' + item + '`\n'
                await message.channel.send(response)
                return
            if(parts[1].lower() == 'magazines'):
                response = ''
                for item in Magazines:
                    response += '`' + item + '`\n'
                    if(len(response)>1500):
                        await message.channel.send(response)
                        response = ""
                await message.channel.send(response)
                return
            if(parts[1].lower() == 'grips'):
                response = ''
                for item in Grips:
                    response += '`' + item + '`\n'
                await message.channel.send(response)
                return
            if(parts[1].lower() == 'gear'):
                response = ''
                for item in Gear:
                    response += '`' + item + '`\n'
                await message.channel.send(response)
                return
            if(parts[1].lower() == 'tactical'):
                response = ''
                for item in Tactical:
                    response += '`' + item + '`\n'
                await message.channel.send(response)
                return
            await message.channel.send('Not a valid list. Use `list` to get available lists.')
            return