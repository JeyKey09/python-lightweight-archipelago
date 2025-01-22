"""Packets sent between the client and server"""

from typing import NamedTuple
import sys, inspect


ALL_CLIENT_PACKAGES =  { client_packet.__qualname__:client_packet for client_packet in inspect.getmembers(sys.modules[f"{__name__}.client", inspect.isclass])}
ALL_SERVER_PACKAGES =  { server_packet.__qualname__:server_packet for server_packet in inspect.getmembers(sys.modules[f"{__name__}.server", inspect.isclass])}

class Packet(NamedTuple):
    cmd : str