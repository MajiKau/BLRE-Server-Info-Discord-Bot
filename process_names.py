import win32gui
import re


def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        ctx.append(win32gui.GetWindowText(hwnd))


def getServerInfo(playerCap):
    windowTitles = []
    title = 'NOT ONLINE'

    win32gui.EnumWindows(winEnumHandler, windowTitles)

    # Find the BLR Server window and extract the player count and map from it
    for windowTitle in windowTitles:
        if(windowTitle.startswith('[VER')):
            info = re.findall(r'\[(.*?)\]', windowTitle)
            playerCount = info[1].strip('POP ')
            if(int(playerCount) > int(playerCap)):
                playerCount = '??'
            mapFileName = info[2].strip('MAP ')
            mapName = getMapName(mapFileName)
            title = playerCount + '/' + playerCap + ' | ' + mapName
            break

    # Return "{playerCount}/{playerCap} | {mapName}"
    return title


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
    return mapFileName
