import json 
import uuid
from packets import create_packet_object
from websockets.asyncio.client import connect 
from packets.core import DataPackageObject, GameData, NetworkItem, NetworkPlayer, NetworkSlot, Version
from packets.core.enums import Permission
from packets.server import *
from packets.client import Connect, GetDataPackage

def as_packet(obj : dict):
	"""	Filters the special packets, modifies the dictionary 
    	and casts it into the appropriate object
            
		Returns None if this is not a packets
	"""
	if isinstance(obj, list):
		for i,v in enumerate(obj):
			obj[i] = as_packet(v)
		return obj
	if "cmd" in obj:
		if obj["cmd"].__eq__("RoomInfo"):
			obj["version"] = Version(obj["version"]["major"], 
                                    obj["version"]["minor"], 
                                    obj["version"]["build"])
           
			obj["generator_version"] =  Version(obj["generator_version"]["major"], 
                                                     obj["generator_version"]["minor"], 
                                                     obj["generator_version"]["build"]),
			obj["permissions"] = {k:Permission(i) for k,i in obj["permissions"].items()}
            
		elif obj["cmd"].__eq__("Connected"):
			obj["players"] = [NetworkPlayer(**player) for player in obj["players"]]
			obj["slot_info"] = {k:NetworkSlot(**slot) for k,slot in obj["players"].items()}
            
		elif obj["cmd"].__eq__("ReceivedItems"):
			obj["items"] = [NetworkItem(**item) for item in obj["items"]]
            
		elif obj["cmd"].__eq__("DataPackageObject"):
			obj["games"] = {k:GameData(**data) for k,data in obj["games"].items()}

		cls = globals()[obj.get("cmd")]
		del obj["cmd"]
		return cls(**obj)
    
# def encode_packet(obj):
#     if isinstance(obj, list):
#         for i,v in enumerate(obj):
#               obj[i] = as_packet(v)
# 			return obj
#     elif 

class GameConfig:
    def __init__(self, game : str, items_handling : int = 0b011):
        self.game = game
        self.items_handling = items_handling

class ClientConfig:
    client : str = str(uuid.uuid4())
    version : Version = Version()

    def __init__(self, port : int, player : str, password : str, address : str = "archipelago.gg"):
        self.port = port
        self.player = player
        self.password = password
        self.address = address

class Client():
    def __init__(self, client_config : ClientConfig, game_config : GameConfig):
        self.client_config = client_config
        self.game_config = game_config
        self.packages_to_be_sent = []
        self.packages_received = []
        self.connection = None
    
    async def __send_packages(self, packages):
        if not isinstance(packages, list):
            packages = [packages]
        for i,package in enumerate(packages):
            packages[i] = package.__dict__
            packages[i]["cmd"] = type(package).__name__
        await self.connection.send(json.dumps(packages))
    
    async def process_server_packages():
        sds

    async def run(self):
        #TODO: Need to steal some code from archipelago to make it work with non-secure servers or add it's own SSL
        async with connect(f"wss://{self.client_config.address}:{self.client_config.port}") as websocket:
            self.connection = websocket
            room_info = as_packet(json.loads(await self.connection.recv()))[0]
            #room_info : RoomInfo = create_packet_object(temp_room_info)
            if not room_info.games.__contains__(self.game_config.game):
                raise RuntimeError("Server does not contain the game")
            #await self.__send_packages([GetDataPackage([self.game_config.game])])
            
            await self.__send_packages(Connect(self.client_config.password, self.game_config.game, self.client_config.player, self.client_config.client, self.client_config.version, self.game_config.items_handling, [], True))
            data_package = create_packet_object((await self.connection.recv()))
            print(data_package)
