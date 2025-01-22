import json 
import uuid
from packets import create_packet_object
from websockets.asyncio.client import connect 
from packets.core import DataPackageObject, Version
from packets.server import RoomInfo
from packets.client import Connect, GetDataPackage

class GameConfig:
    def __init__(self, game : str, items_handling : int = 0b011):
        self.game = game
        self.items_handling = items_handling

class ClientConfig:
    client : str = str(uuid.uuid4())
    version : Version = Version.get_current()

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

    async def run(self):
        async with connect(f"wss://{self.client_config.address}:{self.client_config.port}") as websocket:
            self.connection = websocket
            temp_room_info = json.loads((await self.connection.recv()))[0]
            room_info : RoomInfo = create_packet_object(temp_room_info)
            if not room_info.games.__contains__(self.game_config.game):
                raise RuntimeError("Server does not contain the game")
            # await self.__send_packages([GetDataPackage([self.game_config.game])])
            # data_package = create_packet_object((await self.connection.recv()))
