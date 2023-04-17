from dataclasses import dataclass
import json

@dataclass
class Config:
    BLREdit: str = 'BLREdit.exe'
    LaunchOptionsFile: str = 'launch/DM.json'
    ServerInfoFile: str = 'C:/Program Files (x86)/Steam/steamapps/common/blacklightretribution/FoxGame/Config/BLRevive/server_utils/server_info.json'
    DomainName: str = 'mooserver.ddns.net'

    def LoadFromJson(jsonStr):
        return Config(**jsonStr)

    def LoadFromFile(fileName: str):
        try:
            file = open(fileName)
            data = json.loads(file.read())
            return Config.LoadFromJson(data)
        except Exception as e:
            print('Failed to read configuration file: {}'.format(fileName))
            print(e)
            return None