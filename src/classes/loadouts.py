from classes.items import Barrels, Grips, Receivers, Scopes, Stocks, AmmoTypes, Magazines
from dataclasses import dataclass, fields
from typing import Any
import json
import jsonpickle

requiredPlayerKeys = [
    'PlayerName'
]

requiredLoadouts = [
    'Loadout1',
    'Loadout2',
    'Loadout3'
]

requiredLoadoutKeys = [
    'Primary',
    'Secondary'
]

requiredWeaponKeys = [
    'Receiver'
]

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
    Tag: int = 1
    Camo: int = 0
    AmmoType: str = ''
    
    def GetAmmoType(magazineIndex: int):
        magazine = Magazines[magazineIndex]
        if('Bow' in magazine or 'Breech' in magazine):
            return 'None'
        for ammoType in AmmoTypes:
            if(ammoType.split()[0] in magazine):
                return ammoType
        return 'None'

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
        if 'Tag' not in json:
            json['Tag'] = 1
        if 'Camo' not in json:
            json['Camo'] = 0
        if 'AmmoType' not in json:
            json['AmmoType'] = Weapon.GetAmmoType(json['Magazine'])
        return Weapon(json['Receiver'],json['Muzzle'],json['Stock'],json['Barrel'],json['Magazine'],json['Scope'],json['Grip'],json['Tag'],json['Camo'],json['AmmoType'])

@dataclass
class Loadout:		
    Primary: Weapon = Weapon()
    Secondary: Weapon = Weapon()
    Gear1: int = 1
    Gear2: int = 2
    Gear3: int = 0
    Gear4: int = 0
    Tactical: int = 0
    Camo: int = 0
    UpperBody: int = 0
    LowerBody: int = 0
    Helmet: int = 0
    IsFemale: bool = 0
    Skin: int = 0xFFFFFFFF
    Trophy: int = 0
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
        if 'Camo' not in json:
            json['Camo'] = 0
        if 'UpperBody' not in json:
            json['UpperBody'] = 0
        if 'LowerBody' not in json:
            json['LowerBody'] = 0
        if 'Helmet' not in json:
            json['Helmet'] = 0
        if 'IsFemale' not in json:
            json['IsFemale'] = False
        if 'Skin' not in json:
            json['Skin'] = 0xFFFFFFFF
        if 'Trophy' not in json:
            json['Trophy'] = 0
        return Loadout(Weapon.LoadFromJson(json['Primary']),Weapon.LoadFromJson(json['Secondary']), json['Gear1'], json['Gear2'], json['Gear3'], json['Gear4'], json['Tactical'], json['Camo'], json['UpperBody'], json['LowerBody'], json['Helmet'], json['IsFemale'], json['Skin'], json['Trophy'])

@dataclass
class Player(NoneRefersDefault):		
    DiscordId: int = 0
    PlayerName: str = ''
    IP: str = ''
    Loadout1: Loadout = DefaultVal(Loadout(Weapon('Assault Rifle'),Weapon('Light Pistol')))
    Loadout2: Loadout = DefaultVal(Loadout(Weapon('Submachine Gun'),Weapon('Light Pistol')))
    Loadout3: Loadout = DefaultVal(Loadout(Weapon('Bolt-Action Rifle'),Weapon('Light Pistol')))
    def LoadFromJson(json):
        if 'DiscordId' not in json:
            json['DiscordId'] = 0
        if 'IP' not in json:
            json['IP'] = ''
        return Player(json['DiscordId'],json['PlayerName'],json['IP'],Loadout.LoadFromJson(json['Loadout1']),Loadout.LoadFromJson(json['Loadout2']),Loadout.LoadFromJson(json['Loadout3']))

@dataclass
class PlayerLoadouts:		
    Loadouts: 'list[Player]' = None
    def LoadFromJson(jsonStr):
        return PlayerLoadouts(**jsonStr)

    def GetWeaponErrors(weapon: Weapon):
        errors = ""
        if(type(weapon.Receiver) is not str): errors += 'Receiver should be a string!\n'
        elif(weapon.Receiver != "" and weapon.Receiver not in Receivers): errors += weapon.Receiver + ' is not a valid Receiver!\n'

        if(type(weapon.Stock) is not str): errors += 'Stock should be a string!\n'
        elif(weapon.Stock != "" and weapon.Stock not in Stocks): errors += weapon.Stock + ' is not a valid Stock!\n'

        if(type(weapon.Barrel) is not str): errors += 'Barrel should be a string!\n'
        elif(weapon.Barrel != "" and weapon.Barrel not in Barrels): errors += weapon.Barrel + ' is not a valid Barrel!\n'

        if(type(weapon.Scope) is not str): errors += 'Scope should be a string!\n'
        elif(weapon.Scope != "" and weapon.Scope not in Scopes): errors += weapon.Scope + ' is not a valid Scope!\n'

        if(type(weapon.Grip) is not str): errors += 'Grip should be a string!\n'
        elif(weapon.Grip != "" and weapon.Grip not in Grips): errors += weapon.Grip + ' is not a valid Grip!\n'

        if(type(weapon.Muzzle) is not int): errors += 'Muzzle should be an integer!\n'
        if(type(weapon.Magazine) is not int): errors += 'Magazine should be an integer!\n'
        if(type(weapon.Tag) is not int): errors += 'Tag should be an integer!\n'
        if(type(weapon.Camo) is not int): errors += 'Camo should be an integer!\n'
        return errors

    def GetLoadoutErrors(loadout: Loadout):
        errors = ""
        errors += PlayerLoadouts.GetWeaponErrors(loadout.Primary)
        errors += PlayerLoadouts.GetWeaponErrors(loadout.Secondary)
        if(type(loadout.Gear1) is not int): errors += 'Gear1 should be an integer!\n'
        if(type(loadout.Gear2) is not int): errors += 'Gear2 should be an integer!\n'
        if(type(loadout.Gear3) is not int): errors += 'Gear3 should be an integer!\n'
        if(type(loadout.Gear4) is not int): errors += 'Gear4 should be an integer!\n'
        if(type(loadout.Tactical) is not int): errors += 'Tactical should be an integer!\n'
        if(type(loadout.Camo) is not int): errors += 'Camo should be an integer!\n'
        if(type(loadout.UpperBody) is not int): errors += 'UpperBody should be an integer!\n'
        if(type(loadout.LowerBody) is not int): errors += 'LowerBody should be an integer!\n'
        if(type(loadout.Helmet) is not int): errors += 'Helmet should be an integer!\n'
        if(type(loadout.IsFemale) is not bool): errors += 'IsFemale should be a boolean!\n'
        if(type(loadout.Skin) is not int): errors += 'Skin should be an integer!\n'
        if(type(loadout.Trophy) is not int): errors += 'Trophy should be an integer!\n'

        return errors

    def GetJSONErrors(data):
        errors = ''
        for playerKey in requiredPlayerKeys:
            if(playerKey not in data):
                errors += playerKey + ' not found!\n'

        for loadout in requiredLoadouts:
            if(loadout not in data):
                errors += loadout + ' not found!\n'
            else:
                for loadoutKey in requiredLoadoutKeys:
                    if(loadoutKey not in data[loadout]):
                        errors += loadoutKey + ' not found in ' + loadout + '!\n'
                    else:
                        for weaponKey in requiredWeaponKeys:
                            if(weaponKey not in data[loadout][loadoutKey]):
                                errors += weaponKey + ' not found in ' + loadout + ' ' + loadoutKey + '!\n'
        return errors
        
    def GetPlayerErrors(player: Player):
        errors = ""
        errors += PlayerLoadouts.GetLoadoutErrors(player.Loadout1)
        errors += PlayerLoadouts.GetLoadoutErrors(player.Loadout2)
        errors += PlayerLoadouts.GetLoadoutErrors(player.Loadout3)
        return errors

    def RemovePlayer(self, IP: str, playerName: str):
        for storedPlayer in self.Loadouts:
            if(storedPlayer.IP == IP and storedPlayer.PlayerName == playerName):
                self.Loadouts.remove(storedPlayer)
                return True
        return False

    def FindPlayer(self, IP: str, playerName: str = None):
        players = list()
        for storedPlayer in self.Loadouts:
            if(storedPlayer.IP == IP):
                if(playerName == None):
                    players.append(storedPlayer)
                elif(storedPlayer.PlayerName == playerName):
                    players.append(storedPlayer)
                    break
        return players
        
    def RegisterPlayerAPI(self, player: Player, IP: str):
        player.IP = IP
        playerCountForIP = 0
        for storedPlayer in self.Loadouts:
            if(storedPlayer.IP == IP):
                playerCountForIP += 1
                if(storedPlayer.PlayerName == player.PlayerName):
                    self.Loadouts.remove(storedPlayer)
                    playerCountForIP -= 1
                    break
                
        if(playerCountForIP >= 10):
            return 'You have too many saved accounts. Remove or edit an existing one.'
        self.Loadouts.append(player)
        return ''

    def RegisterPlayer(self, discordId: int, player: Player):

        errors = ""
        #print(player)
        errors +=PlayerLoadouts.GetPlayerErrors(player)
        if(errors != ""): return errors

        if(discordId != 0): #Discord
            for storedPlayer in self.Loadouts:
                if(storedPlayer.PlayerName == player.PlayerName):
                    if(storedPlayer.DiscordId != discordId):
                        return 'Player name is already taken!'
                    else:
                        player.DiscordId = discordId
                        self.Loadouts.remove(storedPlayer)
                        break
        else: #API
            for storedPlayer in self.Loadouts:
                if(storedPlayer.PlayerName == player.PlayerName):
                    if(storedPlayer.PassCode != player.PassCode):
                        return 'Wrong passcode!'
                    else:
                        player.DiscordId = storedPlayer.DiscordId
                        self.Loadouts.remove(storedPlayer)
                        break

        for storedPlayer in self.Loadouts:
            if(storedPlayer.PlayerName == player.PlayerName):
                if(discordId != 0): #Discord
                    if(storedPlayer.DiscordId != discordId):
                        return 'Player name is already taken!'
                    else:
                        player.DiscordId = discordId
                        self.Loadouts.remove(storedPlayer)
                        break
                else: #API
                    if(storedPlayer.PassCode != player.PassCode):
                        return 'Wrong passcode!'
                    else:
                        player.DiscordId = storedPlayer.DiscordId
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
        except Exception as e:
            print('Failed to read configuration file: {}'.format(fileName))
            print(e)
            return False


    def SaveLoadouts(self, fileName: str):
        try:
            data = jsonpickle.encode(self, unpicklable=False, indent=4)
            file = open(fileName, 'w')
            file.write(data)
            return True
        except Exception as e:
            print('Failed to read configuration file: {}'.format(fileName))
            print(e)
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
        except Exception as e:
            print('Failed to read configuration file: {}'.format(fileName))
            print(e)
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