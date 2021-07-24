import win32gui
import re


def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        ctx.append(win32gui.GetWindowText(hwnd))


def getServerInfo(playerCap):
    windowTitles = []
    title = 'NOT FOUND'

    win32gui.EnumWindows(winEnumHandler, windowTitles)

    # Find the BLR Server window and extract the player count and map from it
    for windowTitle in windowTitles:
        if(windowTitle.startswith('[VER')):
            info = re.findall(r'\[(.*?)\]', windowTitle)
            playerCount = info[1].strip('POP ') + '/' + playerCap
            mapName = info[2]
            title = playerCount + ' | ' + mapName
            break

    # Return "{playerCount}/{playerCap} | MAP {CurrentMap}"
    return title
