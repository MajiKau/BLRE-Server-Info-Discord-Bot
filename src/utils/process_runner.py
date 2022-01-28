from dataclasses import asdict
from classes.server_structs import LaunchOptions
import win32gui
import win32process
import time
from subprocess import Popen

gameServerFile = ''

def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


def startServer(options: LaunchOptions):

    url = ' server {Map}?Name=\"{Servername}\"?Game=FoxGame.FoxGameMP_{Gamemode}?Port={Port}?NumBots={BotCount}?MaxPlayers={MaxPlayers}?Playlist={Playlist}?SCP={SCP}?TimeLimit={TimeLimit}'.format(
        **asdict(options))

    args = gameServerFile + url
    print(args)
    process = Popen(args)
    time.sleep(15)  # Adjust this to make sure the server window is running

    return process


def stopServer(process: Popen):
    process.kill()


def restartServer(options: LaunchOptions, process: Popen):
    if(process != None):
        stopServer(process)

    return startServer(options)
