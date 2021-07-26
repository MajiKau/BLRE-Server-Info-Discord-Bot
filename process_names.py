import win32gui
import re


def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        ctx.append((hwnd, win32gui.GetWindowText(hwnd)))


def pickServer():
    serverProcess = 0
    allProcesses = []
    win32gui.EnumWindows(winEnumHandler, allProcesses)
    matchingProcesses = [
        match for match in allProcesses if match[1].startswith('[VER')]

    i = 0
    print('All matching processes:')
    for process in matchingProcesses:
        print('[' + str(i) + '] ' + str(process))
        i += 1

    if(len(matchingProcesses) > 1):
        serverProcessIndex = max(
            0, min(int(input('Select process: ')), len(matchingProcesses)-1))
        serverProcess = matchingProcesses[serverProcessIndex][0]

    if(len(matchingProcesses) == 1):
        serverProcess = matchingProcesses[0][0]

    return serverProcess


def getProcessTitle(hwnd):
    return win32gui.GetWindowText(hwnd)


def getServerInfo(hwnd, playerCap):
    serverInfo = 'NOT ONLINE'

    processTitle = getProcessTitle(hwnd)

    # # Find the BLR Server window and extract the player count and map from it
    if(processTitle != ""):
        infoBlocks = re.findall(r'\[(.*?)\]', processTitle)
        playerCount = infoBlocks[1].strip('POP ')
        if(int(playerCount) > int(playerCap)):
            playerCount = '??'
        mapFileName = infoBlocks[2].strip('MAP ')
        mapName = getMapName(mapFileName)
        serverInfo = playerCount + '/' + playerCap + ' | ' + mapName

    # Return "{playerCount}/{playerCap} | {mapName}"
    return serverInfo


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
