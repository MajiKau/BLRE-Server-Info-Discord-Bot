from enum import Enum, auto

class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

class CommandType(AutoName):
    Unknown = auto()
    Help = auto()
    Status = auto()
    Restart = auto()
    Map = auto()
    Bots = auto()
    Playlist = auto()
    Gamemode = auto()
    SCP = auto()
    TimeLimit = auto()
    AutoRestart = auto()
    Reset = auto()
    Register = auto()
    Primary = auto()
    List = auto()


def getMessageType(message: str):
    if(message.lower().startswith('help')):
        return CommandType.Help
    if(message.lower().startswith('status')):
        return CommandType.Status
    if(message.lower().startswith('restart')):
        return CommandType.Restart
    if(message.lower().startswith('map')):
        return CommandType.Map
    if(message.lower().startswith('bots')):
        return CommandType.Bots
    if(message.lower().startswith('playlist')):
        return CommandType.Playlist
    if(message.lower().startswith('gamemode')):
        return CommandType.Gamemode
    if(message.lower().startswith('scp')):
        return CommandType.SCP
    if(message.lower().startswith('timelimit')):
        return CommandType.TimeLimit
    if(message.lower().startswith('autorestart')):
        return CommandType.AutoRestart
    if(message.lower().startswith('reset')):
        return CommandType.Reset
    if(message.lower().startswith('register')):
        return CommandType.Register
    if(message.lower().startswith('primary')):
        return CommandType.Primary
    if(message.lower().startswith('list')):
        return CommandType.List
