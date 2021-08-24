from utils.mydifflib import get_close_matches_indexes

# TODO: Add rest of gamemodes and check the current ones
gamemodeNames = [
    'Deathmatch',
    'Team deathmatch',
    'Capture the flag',
    'Kill confirmed',
    'King of the hill',
    'Last team standing',
    'Last man standing',
    'Search and destroy'
]

gamemodes = [
    'DM',
    'TDM',
    'CTF',
    'KC',
    'KOTH',
    'LTS',
    'LMS',
    'SAD'
]


def getGamemode(gamemodeToFind: str):
    closestMatch = get_close_matches_indexes(
        gamemodeToFind, gamemodes + gamemodeNames, 1, 0)[0]
    gamemode = gamemodes[closestMatch % len(gamemodes)]
    return gamemode


def isValidGamemode(gamemode):
    if(gamemode in gamemodes):
        return True
    return False
