
from dataclasses import dataclass
from typing import Dict, List, NamedTuple, Optional, TypedDict

from .enums import SlotType


class JSONMessagePart(TypedDict):
    type: Optional[str]
    text: Optional[str]
    color: Optional[str] # only available if type is a color
    flags: Optional[int] # only available if type is an item_id or item_name
    player: Optional[int] # only available if type is either item or location


class Version(NamedTuple):
    major: int
    minor: int
    build: int

    @staticmethod
    def get_current():
        return Version(major=0,minor=5,build=1)

@dataclass
class NetworkItem(NamedTuple):
    item: int
    location: int
    player: int
    flags: int

@dataclass
class NetworkPlayer(NamedTuple):
    team: int
    slot: int
    alias: str
    name: str

@dataclass
class NetworkSlot(NamedTuple):
   name: str
   game: str
   type: SlotType
   group_members: List[int] = []  # only populated if type == group

@dataclass
class Hint(NamedTuple):
    receiving_player: int
    finding_player: int
    location: int
    item: int
    found: bool
    entrance: str = ""
    item_flags: int = 0

@dataclass
class GameData(NamedTuple):
    item_name_to_id : Dict[str, int]
    location_name_to_id : Dict[str, int]
    checksum : str

@dataclass
class DataPackageObject(NamedTuple):
    games : Dict[str, GameData]

@dataclass
class DataStorageOperation(NamedTuple):
    operation : str
    value : any