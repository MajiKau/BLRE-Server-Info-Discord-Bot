from utils.mydifflib import get_close_matches_indexes

# TODO: Add rest of playlists and check the current ones
playlistNames = [
    'Deathmatch',
    'Team deathmatch',
    'Capture the flag',
    'Kill confirmed',
    'King of the hill',
    'Last team standing',
    'Last man standing',
    'Search and destroy'
]

playlists = [
    'DM',
    'TDM',
    'CTF',
    'KC',
    'KOTH',
    'LTS',
    'LMS',
    'SAD'
]


def getPlaylist(playlistToFind: str):
    closestMatch = get_close_matches_indexes(
        playlistToFind, playlists + playlistNames, 1, 0)[0]
    playlist = playlists[closestMatch % len(playlists)]
    return playlist


def isValidPlaylist(playlist):
    if(playlist in playlists):
        return True
    return False
