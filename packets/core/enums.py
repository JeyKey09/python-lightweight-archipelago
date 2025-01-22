"""Enums defined in the network diagram documentation"""

import enum

class SlotType(enum.IntFlag):
    spectator = 0b00
    player = 0b01
    group = 0b10

class ClientStatus(enum.IntEnum):
    CLIENT_UNKNOWN = 0
    CLIENT_CONNECTED = 5
    CLIENT_READY = 10
    CLIENT_PLAYING = 20
    CLIENT_GOAL = 30

class Permission(enum.IntEnum):
    disabled = 0b000  # 0, completely disables access
    enabled = 0b001  # 1, allows manual use
    goal = 0b010  # 2, allows manual use after goal completion
    auto = 0b110  # 6, forces use after goal completion, only works for release and collect
    auto_enabled = 0b111  # 7, forces use after goal completion, allows manual use any time

class PrintJsonType(str, enum.Enum):
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
    cmd = "cmd"
    argument = "arguments"

class ItemsHandlingFlags(enum.IntEnum):
    ReceiveNone = 0b000
    ReceiveItems = 0b001
    ReceieveFromSelf = 0b010
    """Needs to be combined with RecieveItems"""
    RecieveStartInventory = 0b100
    """Needs to be combined with RecieveItems"""