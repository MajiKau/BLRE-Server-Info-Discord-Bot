from dataclasses import dataclass

@dataclass
class ServerInfo:
    PlayerCount: int = 0
    Map: str = ''
    PlayerList: 'list[str]' = None
    ServerName: str = ''
    GameMode: str = ''

@dataclass
class LaunchOptions:
    Map: str = ''
    Servername: str = 'Custom Server'
    Gamemode: str = ''
    Port: int = 7778
    BotCount: int = 0
    MaxPlayers: int = 16
    Playlist: str = 'DM'
    SCP: int = 0
    TimeLimit: int = None

    def LoadFromJson(jsonStr):
        return LaunchOptions(**jsonStr)