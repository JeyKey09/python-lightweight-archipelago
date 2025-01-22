"""Packets Util"""

import json
from typing import Dict
from .server import *
from .client import *


def create_packet_object(plain_packet : Dict):
	if isinstance(plain_packet, str):
		plain_packet = json.loads(plain_packet)
	cls = globals()[plain_packet.get("cmd") or plain_packet.get("class")]
	if cls == None:
		raise ValueError("Class, not found")
	del plain_packet["cmd" if plain_packet.get("cmd") != None else "class"]
	for (key,value) in plain_packet.items():
		if isinstance(value,dict) and (value.get("class") != None):
			plain_packet[key] = create_packet_object(value)
	return cls(**plain_packet)