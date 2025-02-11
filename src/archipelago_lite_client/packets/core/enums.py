"""Enums defined in the network diagram documentation"""

import enum


class SlotType(enum.IntFlag):
    """The different kind of slot"""

    spectator = 0b00
    player = 0b01
    group = 0b10


class ClientStatus(enum.IntEnum):
    """The int numbers of the different statuses of a client"""

    CLIENT_UNKNOWN = 0
    CLIENT_CONNECTED = 5
    CLIENT_READY = 10
    CLIENT_PLAYING = 20
    CLIENT_GOAL = 30


class Permission(enum.IntEnum):
    """The permissions of clients"""

    disabled = 0b000
    """completely disables access"""
    enabled = 0b001
    """allows manual use"""
    goal = 0b010
    """allows manual use after goal completion"""
    auto = 0b110
    """forces use after goal completion, only works for release and collect"""
    auto_enabled = 0b111
    """forces use after goal completion, allows manual use any time"""


class PrintJsonType(str, enum.Enum):
    """The different types of PrintJsonType"""

    ItemSend = "ItemSend"
    ItemCheat = "ItemCheat"
    Hint = "Hint"
    Join = "Join"
    Part = "Part"
    Chat = "Chat"
    ServerChat = "ServerChat"
    Tutorial = "Tutorial"
    TagsChanged = "TagsChanged"
    CommandResult = "CommandResult"
    AdminCommandResult = "AdminCommandResult"
    Goal = "Goal"
    Release = "Release"
    Collect = "Collect"
    Countdown = "Countdown"


class PacketProblemType(str, enum.Enum):
    """The different kind of problems the packet can have"""

    cmd = "cmd"
    argument = "arguments"


class ItemsHandlingFlags(enum.IntEnum):
    ReceiveNone = 0b000
    ReceiveItems = 0b001
    """ Recieve items from other players trough the server. 
    
        Can be combined with `ReceieveFromSelf` and/or `RecieveStartInventory`
    """
    ReceieveFromSelf = 0b010
    """Needs to be combined with RecieveItems"""
    RecieveStartInventory = 0b100
    """Needs to be combined with RecieveItems"""
