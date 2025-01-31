"""Packets the server sends"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from .core import DataPackageObject, JSONMessagePart, NetworkItem, NetworkSlot, Version, NetworkPlayer
from .core.enums import Permission, PrintJsonType

@dataclass
class RoomInfo():
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

@dataclass
class ConnectionRefused():
    errors : list[str]

@dataclass
class Connected():
    team : int
    slot : int
    players : List[NetworkPlayer]
    missing_locations : List[int]
    checked_locations : List[int]
    slot_data : Dict[str, any]
    slot_info : Dict[int, NetworkSlot]
    hint_points : int 

@dataclass
class ReceivedItems:
    """Sent to clients when they receive an item."""
    
    index : int
    items : List[NetworkItem]

@dataclass
class LocationInfo:
    locations : List[NetworkItem]

@dataclass
class RoomUpdate(RoomInfo, Connected):
    players : Optional[List[NetworkPlayer]]
    checked_locations : Optional[List[int]]

#Make subclasses of the different packets of PrintJSON
#or mark the other parameters as optional parameters
@dataclass
class PrintJSON:
    """Contains a JSON message part and an optional type

    @type: The type of the JSON message part
    @data: The JSON message part
    """
    data : List[JSONMessagePart]
    type : Optional[PrintJsonType]

@dataclass
class DataPackage:
    data : DataPackageObject

@dataclass
class Bounced:
    games : List[str]
    slots : List[str]
    tags : List[str]
    data : Dict

@dataclass
class InvalidPacket:
    type : str
    original_cmd : Optional[str]
    text : str

@dataclass
class Retrieved:
    keys : Dict[str, any]

@dataclass
class SetReply:
    key : str
    value : any
    original_value : any