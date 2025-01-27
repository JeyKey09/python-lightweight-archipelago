import asyncio
from enum import Enum
import inspect
import json 
import uuid
from websockets.asyncio.client import connect 
from .packets.client import Connect
from queue import Queue
from .packets.core.enums import ItemsHandlingFlags, Permission
#Import types into the namespace to be able to decode them
from .packets.server import *
from .packets.core import *


def decode_packet(obj : dict):
    """	Filters the special packets, modifies the dictionary 
    	and casts it into the appropriate object
            
        Returns None if this is not a packets
    """
    if isinstance(obj, list):
        for i,v in enumerate(obj):
            obj[i] = decode_packet(v)
        return obj
    if "cmd" in obj or "class" in obj:
        cls = globals()[obj.get("cmd") or obj.get("class")]
        del obj["cmd" if obj.get("cmd") is not None else "class"]
        if cls == PrintJSON:
            obj = {"type": obj["type"], "data": obj["data"]} 
        for i in inspect.getmembers(obj):
            if not i[0].startswith('_') and not inspect.ismethod(i[1]) and not inspect.isbuiltin(i[1]):
                obj[i[0]] = decode_packet(getattr(obj, i[0]))
        return cls(**obj)

    
def encode_packet(obj):
    if isinstance(obj, list):
        for i,v in enumerate(obj):
            obj[i] = encode_packet(v)
        return obj
    #Archipelagos method to ensure that the packet is encoded correctly
    #Taken from line 97 in the NetUtils
    elif isinstance(obj, tuple) and hasattr(obj, "_fields"): 
        data = obj._asdict()
        data["class"] = obj.__class__.__name__
        return data
    elif isinstance(obj, Enum) and hasattr(obj, "value"):
        return obj.value
    elif hasattr(obj, '__dict__'):
        obj_copy = {}
        try:
            obj_copy = obj.__dict__
        except AttributeError:
            pass 
        for i in inspect.getmembers(obj):
            if not i[0].startswith('_') and not inspect.ismethod(i[1]):
                obj_copy[i[0]] = encode_packet(getattr(obj, i[0]))
        obj = obj_copy
    return obj 
        

class GameConfig:
    def __init__(self, game : str, items_handling : ItemsHandlingFlags = ItemsHandlingFlags.ReceiveItems):
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
        self.active = True
        self._packages_to_be_sent = Queue()
        self._connection = None
        
    def add_package(self, package):
        self._packages_to_be_sent.put(package)
    
    async def __send_packages(self):
        while(self.active):
            if not self._packages_to_be_sent.empty():
                packages = [self._packages_to_be_sent.get() for _ in range(min(self._packages_to_be_sent.qsize(), 10))]
                for i,package in enumerate(packages):
                    packages[i] = encode_packet(package)
                    packages[i]["cmd"] = type(package).__name__
                await self.connection.send(json.dumps(packages))
            await asyncio.sleep(0.1)
    
    async def __process_server_packages(self):
        while(self.active):
            packets = decode_packet(json.loads(await self.connection.recv()))
            if packets is None:
                continue
            for packet in packets:
                if isinstance(packet, RoomInfo):
                    self.add_package(
                        Connect(self.client_config.password, self.game_config.game, self.client_config.player, 
                                self.client_config.client, self.client_config.version, self.game_config.items_handling, [], True)
                        )
                elif isinstance(packet, Connected):
                    self.connected = packet
                elif isinstance(packet, ReceivedItems):
                    self.received_items = packet
                else:
                    print(f"Unknown packet: {packet}")
        

    async def run(self):
        if not self.active:
            self.active = True
        counter = 0
        while(self.active):
            try:
                #TODO: Need to steal some code from archipelago to make it work with non-secure servers or add it's own SSL
                self.connection = await connect(f"wss://{self.client_config.address}:{self.client_config.port}")
                counter = 0
                await asyncio.gather(
                    asyncio.create_task(self.__process_server_packages()),
                    asyncio.create_task(self.__send_packages())
                )
            except ConnectionRefusedError as e:
                counter += 1
                print(f"Connection refused, {counter}/3 tries")
                if counter >= 3:
                    self.active = False
                 
