"""Packets the server sends"""

from typing import Dict, List, Optional
from .core import DataPackageObject, JSONMessagePart, NetworkItem, NetworkSlot, Version, NetworkPlayer
from .core.enums import Permission, PrintJsonType

class RoomInfo:
    """Sent after Client connects to server"""
    
    version : Version
    """Version of the archipelago"""
    
    generator_version : Version
    """The version of archipelago that generated"""
    
    tags : List[str]
    """Different tags for the client"""
    
    password : bool
    """If it requires password"""
    
    permissions : dict[str, Permission]
    """Mapping permission name to keys"""
    
    hint_cost : int
    """Cost of a hint"""
    
    location_check_points : int
    
    games : List[str]
    """A list of the different games"""
    
    datapackage_checksums : dict[str,str]
    """Checksum for the datapackage"""
    
    seed_name : str
    """Unique identifier for the generation"""

    time : float
    """The time for now"""

class ConnectionRefused():
    errors : list[str]

class Connected():
    team : int
    slot : int
    players : List[NetworkPlayer]
    missing_locations : List[int]
    checked_locations : List[int]
    slot_data : Dict[str, any]
    slot_info : Dict[int, NetworkSlot]
    hint_points : int 

class ReceivedItems:
    """Sent to clients when they receive an item."""
    
    index : int
    items : List[NetworkItem]

class LocationInfo:
    locations : List[NetworkItem]

class RoomUpdate(RoomInfo, Connected):
    players : List[NetworkPlayer]
    checked_locations : List[int]

class PrintJSON:
    data : List[JSONMessagePart]
    type : PrintJsonType
    receiving : int
    item : NetworkItem
    found : bool
    team : int
    slot : int
    message : str
    tags : List[str]
    countdown : int

class DataPackage:
    data : DataPackageObject

class Bounced:
    games : List[str]
    slots : List[str]
    tags : List[str]
    data : Dict

class InvalidPacket:
    type : str
    original_cmd : Optional[str]
    text : str

class Retrieved:
    keys : Dict[str, any]

class SetReply:
    key : str
    value : any
    original_value : any