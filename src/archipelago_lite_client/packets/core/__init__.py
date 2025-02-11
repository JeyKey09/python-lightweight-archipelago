"""Core objects used within archipelagos network protocol"""

from dataclasses import dataclass
from typing import Dict, List, NamedTuple, Optional

from .enums import SlotType


@dataclass
class JSONMessagePart:
    """A JSON messagePart sent when the server asks to printed"""

    type: Optional[str]
    text: Optional[str]
    color: Optional[str]  # only available if type is a color
    flags: Optional[int]  # only available if type is an item_id or item_name
    player: Optional[int]  # only available if type is either item or location


class Version(NamedTuple):
    """The version of the protocol the client support"""

    major: int = 0
    minor: int = 5
    build: int = 1


class NetworkItem(NamedTuple):
    """A representation of a item"""

    item: int
    location: int
    player: int
    flags: int


class NetworkPlayer(NamedTuple):
    """A representation of a player"""

    team: int
    slot: int
    alias: str
    name: str


@dataclass
class NetworkSlot:
    """A representation of a Slot within a game"""

    name: str
    game: str
    type: SlotType
    group_members: List[int]
    """Contains the different group members id. Only populated if the type == group"""


@dataclass
class Hint:
    """A representation of a session hint"""

    receiving_player: int
    finding_player: int
    location: int
    item: int
    found: bool
    entrance: str = ""
    item_flags: int = 0


@dataclass
class GameData:
    """The metadata of the location including item_name to id and location_name_to_id."""

    item_name_to_id: Dict[str, int]
    location_name_to_id: Dict[str, int]
    checksum: str


@dataclass
class DataPackageObject:
    """A object containing the link between a game and GameData"""

    games: Dict[str, GameData]


@dataclass
class DataStorageOperation:
    """A operation done on the storage within the server.

    Should not be necessary to be used unless for debugging purposes
    """

    operation: str
    value: any
