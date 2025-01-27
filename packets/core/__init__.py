
from dataclasses import dataclass
from typing import Dict, List, NamedTuple, Optional, TypedDict

from .enums import SlotType

@dataclass
class JSONMessagePart():
    type: Optional[str]
    text: Optional[str]
    color: Optional[str] # only available if type is a color
    flags: Optional[int] # only available if type is an item_id or item_name
    player: Optional[int] # only available if type is either item or location


class Version(NamedTuple):
    major: int = 0
    minor: int = 0
    build: int = 0

@dataclass
class NetworkItem:
    item: int
    location: int
    player: int
    flags: int

@dataclass
class NetworkPlayer:
    team: int
    slot: int
    alias: str
    name: str

@dataclass
class NetworkSlot:
   name: str
   game: str
   type: SlotType
   group_members: List[int]   # only populated if type == group

@dataclass
class Hint:
    receiving_player: int
    finding_player: int
    location: int
    item: int
    found: bool
    entrance: str = ""
    item_flags: int = 0

@dataclass
class GameData:
    item_name_to_id : Dict[str, int]
    location_name_to_id : Dict[str, int]
    checksum : str

@dataclass
class DataPackageObject:
    games : Dict[str, GameData]

@dataclass
class DataStorageOperation:
    operation : str
    value : any