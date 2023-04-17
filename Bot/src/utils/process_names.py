import win32gui
import re
from classes.server_structs import ServerInfo
from classes.maps import getMapName

def getServerOnline(hwnd: int):
    if(hwnd != 0):
        isOnline = win32gui.IsWindow(hwnd)
        if (isOnline):
            return hwnd
        return 0
    
    allProcesses = []
    win32gui.EnumWindows(winEnumHandler, allProcesses)
    matchingProcesses = [
        match for match in allProcesses if match[1].startswith('[VER')]

    if(len(matchingProcesses) > 1):
        serverProcessIndex = len(matchingProcesses)-1
        return matchingProcesses[serverProcessIndex][0]

    if(len(matchingProcesses) == 1):
        return matchingProcesses[0][0]

    return 0


def getWatchdogOnline(hwnd: int):
    if(hwnd != 0):
        isOnline = win32gui.IsWindow(hwnd)
        if (isOnline):
            return hwnd
        return 0
    
    allProcesses = []
    win32gui.EnumWindows(winEnumHandler, allProcesses)
    matchingProcesses = [
        match for match in allProcesses if match[1].startswith('[Watchdog')]

    if(len(matchingProcesses) > 1):
        serverProcessIndex = len(matchingProcesses)-1
        return matchingProcesses[serverProcessIndex][0]

    if(len(matchingProcesses) == 1):
        return matchingProcesses[0][0]

    return 0



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


def getServerInfo(hwnd):
    serverInfo = ServerInfo()

    try:
        processTitle = getProcessTitle(hwnd)

        # # Find the BLR Server window and extract the player count and map from it
        if(processTitle != ''):
            infoBlocks = re.findall(r'\[(.*?)\]', processTitle)
            if(len(infoBlocks) >= 3):
                playerCount = int(infoBlocks[1].strip('POP '))
                mapFileName = infoBlocks[2].strip('MAP ')
                mapName = getMapName(mapFileName)
                serverInfo.PlayerCount = playerCount
                serverInfo.Map = mapName

    except Exception as e:
        print('Failed to get server info')
        print(e)

    return serverInfo
