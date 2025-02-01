from abc import abstractmethod
import asyncio
import json 
from ssl import SSLError
import uuid
from websockets import ConnectionClosed, State
from websockets.asyncio.client import connect 
from .packets.client import Connect, GetDataPackage, Sync
from queue import Queue
from .packets.core.enums import ItemsHandlingFlags
from .packets import  encode_packet, decode_packet
from threading import Lock
from .packets.server import Connected, ConnectionRefused, DataPackage, LocationInfo, PrintJSON, ReceivedItems, RoomInfo
from .packets.core import Version
from .games import cache_exist, save_cache
import logging
import sys


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler(sys.stdout)],
)

class GameConfig:
    """ A configuration class for the information about the game. 
    
        This includes the game name, how the server should handle items and a possible hash of the game datapackage 
    """
    def __init__(self, game : str, items_handling : ItemsHandlingFlags = ItemsHandlingFlags.ReceiveItems, hash : str = ""):
        self.game = game
        self.items_handling = items_handling
        self.hash = hash

class ClientConfig:
    """ A configuration class for the information for connecting to the client
        
        It is meant to be used as a parameter into a client class and includes stuff like:
        - Port
        - Slot/player name
        - Password
        - address : Defaults to archipelago.gg
        - SSL : Defaults it to be true.
    """
    version : Version = Version()

    def __init__(self, port : int, player : str, password : str, address : str = "archipelago.gg", ssl : bool= True):
        self.port = port
        self.player = player
        self.password = password
        self.address = address
        self.ssl = ssl
        self.client : str = str(uuid.uuid4())


class Client():
    """ A template class to be able to connect to the archipelago client

        Proper use would be to extend it, hardcode the game_config and setup the functions for
        `resolve_location_info` and `resolve_received_items` 
    
        Packets meant to be sent to the server can be queued in the the add_package function. A list of possible
        Packets that can be sent can be found in the packets.client package.
    """

    def __init__(self, client_config : ClientConfig, game_config : GameConfig):
        self.client_config = client_config
        self.game_config = game_config
        self._active = False
        self._handshake_done = False
        self.room_info = None
        self._packages_to_be_sent = Queue()
        self._item_index = 0
        self._connection = None
        self._sender_lock = Lock()
        
    def add_package(self, package):
        """Adds a packet to the queue to be sent to the server"""
        self._packages_to_be_sent.put(package)
    
    async def _send_packages(self, packets):
        """ Allows for sending a packet or packets
            
            Takes in both a packet object or multiple packets
        """
        if not isinstance(packets, list):
            packets = [packets]
        self._sender_lock.acquire()
        try:
            for i,package in enumerate(packets):
                packets[i] = encode_packet(package)
                packets[i]["cmd"] = type(package).__name__

            await self._connection.send(json.dumps(packets))
        except ConnectionClosed:
                return
        except Exception as e:
                logging.info(f"Something went wrong, under the process {e.args}")
        self._sender_lock.release()
    
    async def _packet_sender(self):
        """ A internal routine that takes care of 
            sending packets that is in the queue
        """
        while(self._active and self._connection.state is State.OPEN):
            if self._handshake_done and not self._packages_to_be_sent.empty():
                packages = [self._packages_to_be_sent.get() for _ in range(min(self._packages_to_be_sent.qsize(), 10))]
                await self.__send_packages(packets=packages)
            await asyncio.sleep(0.5)

    async def _process_server_packages(self):
        """Internal routine that takes care of the packets received from the server"""
        while(self._active and self._connection.state is State.OPEN):
            try:
                packets = decode_packet(json.loads(await self._connection.recv()))
                if packets is None:
                    continue
                for packet in packets:
                    match packet: 
                        case RoomInfo():
                            self.room_info = packet
                            self._handle_handshake()

                        case DataPackage():
                            self._handle_datapackage(packet)

                        case Connected():
                            logging.info("Connection established to the archipelago server")
                            self.connected = packet
                            self._handshake_done = True

                        case ConnectionRefused():
                            logging.exception("The connection was refused, may be due to wrong client info")
                            for error in packet.errors:
                                logging.error(error)
                            self._active = False

                        case ReceivedItems():
                            if packet.index == self._item_index+1:
                                self._item_index += len(packet.items)
                                self.resolve_received_items(packet)
                            else:
                                self._item_index = 0
                                self.add_package(Sync())
                    
                        case LocationInfo():
                            self.resolve_location_info(packet)

                        case PrintJSON():
                            self.handle_print(packet)
                            
                        case _:
                            logging.exception(f"Unknown packet: {packet}")

            except ConnectionClosed:
                return
    
    @abstractmethod
    def resolve_received_items(self, items : ReceivedItems):
        """Function called when a items are sent from the server"""
        pass

    @abstractmethod
    def resolve_location_info(self, packet : LocationInfo):
        """Function called when a locationInfo package is sent from the server"""
        pass

    def handle_print(self, packet : PrintJSON): 
        """Function called when a PrintJSON package is sent from the server"""
        logging.info("type: %s | data: %s", packet.type, packet.data)

    def _handle_handshake(self):
        missing_games = []
        for game,checksum in self.room_info.datapackage_checksums.items():
            if not cache_exist(checksum):
                missing_games.append(game)
        if len(missing_games) > 0:
            asyncio.create_task(self._send_packages(GetDataPackage(missing_games)))
        else:
            asyncio.create_task(self._send_packages(Connect(self.client_config.password, self.game_config.game, 
                                                  self.client_config.player, self.client_config.client, 
                                                  self.client_config.version, self.game_config.items_handling, [], True)))
    def _handle_datapackage(self, packet):
        """Function that takes care of the datapackage packet"""
        save_cache(packet)
        self._handle_handshake()

    def stop(self):
        """ Stops the client when in a running state
        
            Returns bool: True if it stopped, False if it was in a state where it couldn't 
        """
        if self._connection.state and self._connection.state is not State.OPEN:
            return False    
        self._active = False
        asyncio.create_task(self._connection.close())
        return True
        
    async def run(self):
        """Starts the client to be ran"""
        if self._active:
            raise RuntimeError("The client is already running, stop it first")
        self._active = True
        counter = 0
        while(self._active):
            try:
                self._connection = await connect(f"{"wss" if self.client_config.ssl else "ws"}://{self.client_config.address}:{self.client_config.port}")
                counter = 0
                await asyncio.gather(
                    asyncio.create_task(self._process_server_packages()),
                    asyncio.create_task(self._packet_sender())
                )
                if self._active:
                    logging.error("The connection to the archipelago server was closed unexpected, will try to reconnect")
            except ConnectionRefusedError:
                counter += 1
                logging.warning(f"Connection refused, {counter}/3 tries")
                #Wait a bit in between to not spam
                await asyncio.sleep(1)
                if counter >= 3:
                    logging.exception("Closing down client due to not getting access")
                    self._active = False
            except SSLError:
                self.client_config.ssl = False