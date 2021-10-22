from classes.items import Receivers
from dataclasses import dataclass, fields
from typing import Any
import json
import jsonpickle

@dataclass
class DefaultVal:
    val: Any

@dataclass
class NoneRefersDefault:
    def __post_init__(self):
        for field in fields(self):

            # if a field of this data class defines a default value of type
            # `DefaultVal`, then use its value in case the field after 
            # initialization has either not changed or is None.
            if isinstance(field.default, DefaultVal):
                field_val = getattr(self, field.name)
                if isinstance(field_val, DefaultVal) or field_val is None:
                    setattr(self, field.name, field.default.val)


@dataclass
class Weapon:		
    Receiver: str = ''
    Muzzle: int = 0
    Stock: str = ''
    Barrel: str = ''
    Magazine: int = 0
    Scope: str = ''
    Grip: str = ''
    def LoadFromJson(json):
        if 'Muzzle' not in json:
            json['Muzzle'] = 0
        if 'Stock' not in json:
            json['Stock'] = ''
        if 'Barrel' not in json:
            json['Barrel'] = ''
        if 'Magazine' not in json:
            json['Magazine'] = 0
        if 'Scope' not in json:
            json['Scope'] = ''
        if 'Grip' not in json:
            json['Grip'] = ''
        return Weapon(json['Receiver'],json['Muzzle'],json['Stock'],json['Barrel'],json['Magazine'],json['Scope'],json['Grip'])

@dataclass
class Loadout:		
    Primary: Weapon = Weapon()
    Secondary: Weapon = Weapon()
    Gear1: int = 1
    Gear2: int = 2
    Gear3: int = 0
    Gear4: int = 0
    Tactical: int = 0
    def LoadFromJson(json):
        if 'Gear1' not in json:
            json['Gear1'] = 1
        if 'Gear2' not in json:
            json['Gear2'] = 2
        if 'Gear3' not in json:
            json['Gear3'] = 0
        if 'Gear4' not in json:
            json['Gear4'] = 0
        if 'Tactical' not in json:
            json['Tactical'] = 0
        return Loadout(Weapon.LoadFromJson(json['Primary']),Weapon.LoadFromJson(json['Secondary']), json['Gear1'], json['Gear2'], json['Gear3'], json['Gear4'], json['Tactical'])

@dataclass
class Player(NoneRefersDefault):		
    DiscordId: int = 0
    PlayerName: str = ''
    Loadout1: Loadout = DefaultVal(Loadout(Weapon('Assault Rifle'),Weapon('Light Pistol')))
    Loadout2: Loadout = DefaultVal(Loadout(Weapon('Submachine Gun'),Weapon('Light Pistol')))
    Loadout3: Loadout = DefaultVal(Loadout(Weapon('Bolt-Action Rifle'),Weapon('Light Pistol')))
    def LoadFromJson(json):
        if 'DiscordId' not in json:
            json['DiscordId'] = 0
        return Player(json['DiscordId'],json['PlayerName'],Loadout.LoadFromJson(json['Loadout1']),Loadout.LoadFromJson(json['Loadout2']),Loadout.LoadFromJson(json['Loadout3']))

@dataclass
class PlayerLoadouts:		
    Loadouts: 'list[Player]' = None
    def LoadFromJson(jsonStr):
        return PlayerLoadouts(**jsonStr)

    def RegisterPlayer(self, discordId: int, player: Player):

        for storedPlayer in self.Loadouts:
            if(storedPlayer.PlayerName == player.PlayerName):
                if(storedPlayer.DiscordId != discordId):
                    return 'Player name is already taken!'

        if(player.Loadout1.Primary.Receiver not in Receivers): return player.Loadout1.Primary.Receiver + ' is not a valid receiver!'
        if(player.Loadout1.Secondary.Receiver not in Receivers): return player.Loadout1.Secondary.Receiver + ' is not a valid receiver!'
        if(player.Loadout2.Primary.Receiver not in Receivers): return player.Loadout2.Primary.Receiver + ' is not a valid receiver!'
        if(player.Loadout2.Secondary.Receiver not in Receivers): return player.Loadout2.Secondary.Receiver + ' is not a valid receiver!'
        if(player.Loadout3.Primary.Receiver not in Receivers): return player.Loadout3.Primary.Receiver + ' is not a valid receiver!'
        if(player.Loadout3.Secondary.Receiver not in Receivers): return player.Loadout3.Secondary.Receiver + ' is not a valid receiver!'

        for storedPlayer in self.Loadouts:
            if(storedPlayer.DiscordId == discordId):
                self.Loadouts.remove(storedPlayer)
                break
                
        player.DiscordId = discordId
        self.Loadouts.append(player)
        return ''

    def RegisterPlayerTemp(self, discordId: int, playerName: str, receiverP1: str, receiverS1: str, receiverP2: str, receiverS2: str, receiverP3: str, receiverS3: str):
        for player in self.Loadouts:
            if(player.DiscordId == discordId or player.PlayerName == playerName):
                self.Loadouts.remove(player)
        
        loadout1 = Loadout(Weapon(receiverP1),Weapon(receiverS1))
        loadout2 = Loadout(Weapon(receiverP2),Weapon(receiverS2))
        loadout3 = Loadout(Weapon(receiverP3),Weapon(receiverS3))

        newPlayer = Player(discordId, playerName, loadout1, loadout2, loadout3)
        self.Loadouts.append(newPlayer)

    def LoadLoadouts(self, fileName: str):
        try:
            file = open(fileName)
            data = json.loads(file.read())
            loadouts = list()
            for entry in data['Loadouts']:
                player: Player = Player.LoadFromJson(entry)
                loadouts.append(player)
            self.Loadouts = loadouts
            return True
        except:
            print('Failed to read configuration file: {}'.format(fileName))
            return False


    def SaveLoadouts(self, fileName: str):
        try:
            data = jsonpickle.encode(self, unpicklable=False, indent=4)
            file = open(fileName, 'w')
            file.write(data)
            return True
        except:
            print('Failed to read configuration file: {}'.format(fileName))
            return False
    
    def Load(fileName: str):
        try:
            file = open(fileName)
            data = json.loads(file.read())
            loadouts: PlayerLoadouts = PlayerLoadouts()
            loadouts.Loadouts = list()
            for entry in data['Loadouts']:
                player: Player = Player.LoadFromJson(entry)
                loadouts.Loadouts.append(player)
            return loadouts
        except:
            print('Failed to read configuration file: {}'.format(fileName))
            return None

# def LoadLoadouts(fileName: str):
#     try:
#         file = open(fileName)
#         data = json.loads(file.read())
#         loadouts: Loadouts = Loadouts()
#         loadouts.Loadouts = list()
#         for entry in data['Loadouts']:
#             player: Player = Player.LoadFromJson(entry)
#             loadouts.Loadouts.append(player)
#         return loadouts
#     except:
#         print('Failed to read configuration file: {}'.format(fileName))
#         return None


# def SaveLoadouts(loadouts: Loadouts, fileName: str):
#     data = jsonpickle.encode(loadouts, unpicklable=False, indent=4)
#     file = open(fileName, 'w')
#     file.write(data)