from utils.mydifflib import get_close_matches_indexes

# TODO: Add rest of the maps (Death Metal, ...)
mapNames = ['Lobby',
            'Helodeck',
            'Heavy Metal',
            'Safehold',
            'Decay',
            'SeaPort',
            'Piledriver',
            'Vortex',
            'Vertigo',
            'Crashsite',
            'Convoy',
            'Outpost',
            'Containment',
            'Trench',
            'Deadlock',
            'Evac',
            'Metro',
            'Rig',
            'Death Metal']

mapFileNames = ['FoxEntry',
                'helodeck',
                'heavymetal',
                'safehold',
                'decay',
                'seaport',
                'piledriver1',
                'vortex',
                'vertigo',
                'crashsite',
                'convoy',
                'outpost',
                'containment',
                'trench',
                'deadlock',
                'evac',
                'metro',
                'rig',
                'deathmetal']


def getMapName(mapFileName):
    if(mapFileName == 'FoxEntry'):
        return 'Lobby'
    if(mapFileName == 'helodeck'):
        return 'Helodeck'
    if(mapFileName == 'heavymetal'):
        return 'Heavy Metal'
    if(mapFileName == 'safehold'):
        return 'Safehold'
    if(mapFileName == 'decay'):
        return 'Decay'
    if(mapFileName == 'seaport'):
        return 'SeaPort'
    if(mapFileName == 'piledriver1'):
        return 'Piledriver'
    if(mapFileName == 'vortex'):
        return 'Vortex'
    if(mapFileName == 'vertigo'):
        return 'Vertigo'
    if(mapFileName == 'crashsite'):
        return 'Crashsite'
    if(mapFileName == 'convoy'):
        return 'Convoy'
    if(mapFileName == 'outpost'):
        return 'Outpost'
    if(mapFileName == 'containment'):
        return 'Containment'
    if(mapFileName == 'trench'):
        return 'Trench'
    if(mapFileName == 'deadlock'):
        return 'Deadlock'
    if(mapFileName == 'evac'):
        return 'Evac'
    if(mapFileName == 'metro'):
        return 'Metro'
    if(mapFileName == 'rig'):
        return 'Rig'
    if(mapFileName == 'deathmetal'):
        return 'Death Metal'
    return mapFileName


def getMapFileName(mapNameToFind: str):
    closestMatch = get_close_matches_indexes(
        mapNameToFind.lower(), mapNames + mapFileNames, 1, 0)[0]
    mapFileName = mapFileNames[closestMatch % len(mapFileNames)]
    return mapFileName


def isValidMap(mapName):
    if(mapName in mapFileNames):
        return True
    return False
