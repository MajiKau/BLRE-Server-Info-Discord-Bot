from dataclasses import dataclass
import json

from classes.commands import CommandType

@dataclass
class ServerInfo:
    PlayerCount: int = 0
    Map: str = ''
    PlayerList: 'list[str]' = None


@dataclass
class LaunchOptions:
    Map: str = ''
    Servername: str = 'Cow Server'
    Gamemode: str = ''
    Port: int = 7778
    BotCount: int = 0
    MaxPlayers: int = 16
    Playlist: str = 'DM'
    SCP: int = 0
    TimeLimit: int = None

    def LoadFromJson(jsonStr):
        return LaunchOptions(**jsonStr)


@dataclass
class ServerOptions:
    LaunchOptions: LaunchOptions = LaunchOptions()
    AutoRestartInLobby: bool = False
    AllowedCommands: 'list[CommandType]' = None

    def LoadFromFile(fileName: str):
        try:
            file = open(fileName)
            data = json.loads(file.read())
            return ServerOptions(LaunchOptions.LoadFromJson(data['LaunchOptions']), data['AutoRestartInLobby'], list(map(lambda x: CommandType(x), data['AllowedCommands'])))
        except:
            print('Failed to read configuration file: {}'.format(fileName))
            return None