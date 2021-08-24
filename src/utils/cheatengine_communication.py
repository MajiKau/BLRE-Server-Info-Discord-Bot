import struct

def scan_players(totalPlayers):
    f = open(r'\\.\pipe\blrevive','wb')

    lua = "Update30Seconds({})".format(totalPlayers)
    luaBytes = bytes(lua, 'utf-8')

    csz = len(luaBytes)

    tosend = struct.pack("<bi"+str(csz)+"sq", 1, csz, luaBytes, 0)

    ret = f.write(tosend)
    f.flush()
    f.close()

def update_loadouts():
    f = open(r'\\.\pipe\blrevive','wb')

    lua = "Update5Seconds()"
    luaBytes = bytes(lua, 'utf-8')

    csz = len(luaBytes)

    tosend = struct.pack("<bi"+str(csz)+"sq", 1, csz, luaBytes, 0)

    ret = f.write(tosend)
    f.flush()
    f.close()