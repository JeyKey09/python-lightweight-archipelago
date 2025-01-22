"""Packets the client sends"""

from typing import Dict, List
from .core import DataStorageOperation, Version
from .core.enums import ClientStatus

class Connect:
    password : str
    game : str
    name : str
    uuid : str
    version : Version
    items_handling : int
    tags : List[str]
    slot_data : bool

class ConnectUpdate:
    items_handling : int
    tags : List[str]

class Sync:
    pass

class LocationChecks:
    locations : List[int]

class LocationScouts:
    locations: List[int]
    create_as_hint : int = 2 
    """If non-zero then scout and broadcast. If 2 only broadcast new hints"""

class StatusUpdate:
    status : ClientStatus

class Say:
    text : str

class GetDataPackage:
    games : List[str]

class Bounce:
    games : List[str]
    slots : List[int]
    tags : List[str]
    data : Dict

class Get:
    """Used to request a single or multiple values from the server's data storage, 
        see the Set package for how to write values to the data storage. 
        A Get package will be answered with a Retrieved package."""
    keys : List[str]

class Set:
    key : str
    defualt : any
    want_reply : bool
    operations : List[DataStorageOperation]

class SetNotify:
    keys : List[str]