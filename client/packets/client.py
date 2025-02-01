"""Packets the client sends"""

from dataclasses import dataclass
from typing import Dict, List
from .core import DataStorageOperation, Version
from .core.enums import ClientStatus

@dataclass
class Connect:
    """ Packet for connecting to the server. 

        Sent as part of the handshake
    """
    password : str
    game : str
    name : str
    uuid : str
    version : Version
    items_handling : int
    tags : List[str]
    slot_data : bool

@dataclass
class ConnectUpdate:

    items_handling : int
    tags : List[str]

@dataclass
class Sync:
    """ Packet sent for syncing the items with the server in a scenario where a packet was lost"""
    pass

@dataclass
class LocationChecks:
    locations : List[int]

@dataclass
class LocationScouts:
    locations: List[int]
    create_as_hint : int = 2 
    """If non-zero then scout and broadcast. If 2 only broadcast new hints"""

@dataclass
class StatusUpdate:
    status : ClientStatus

@dataclass
class Say:
    text : str

@dataclass
class GetDataPackage:
    games : List[str]

@dataclass
class Bounce:
    games : List[str]
    slots : List[int]
    tags : List[str]
    data : Dict

@dataclass
class Get:
    """Used to request a single or multiple values from the server's data storage, 
        see the Set package for how to write values to the data storage. 
        A Get package will be answered with a Retrieved package."""
    keys : List[str]

@dataclass
class Set:
    key : str
    default : any
    want_reply : bool
    operations : List[DataStorageOperation]

@dataclass
class SetNotify:
    keys : List[str]