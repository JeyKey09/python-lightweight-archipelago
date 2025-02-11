"""Utilities used when dealing with websocket packages in between server and client"""

from .server import PrintJSON
import inspect
from enum import Enum


def decode_packet(obj: dict | list):
    """Filters the special packets, modifies the dictionary
    and casts it into the appropriate object

       Returns the object back if it can't encapsulate it
    """
    if isinstance(obj, list):
        for i, v in enumerate(obj):
            obj[i] = decode_packet(v)
        return obj
    if isinstance(obj, dict) and ("cmd" in obj or "class" in obj):
        cls = globals()[obj.get("cmd") or obj.get("class")]
        del obj["cmd" if obj.get("cmd") is not None else "class"]
        if cls == PrintJSON:
            obj = {"type": obj.get("type"), "data": obj.get("data")}
        for i in filter(lambda x: isinstance(x[1], (dict, list)), obj.items()):
            obj[i[0]] = decode_packet(i[1])
        return cls(**obj)
    return obj


def encode_packet(obj):
    """Encodes the package into the standard archipelago wants
    so it can understand it.
    """
    if isinstance(obj, list):
        for i, v in enumerate(obj):
            obj[i] = encode_packet(v)
        return obj
    # Archipelagos method to ensure that the tuple is encoded correctly
    # Taken from line 97 in the NetUtils
    elif isinstance(obj, tuple) and hasattr(obj, "_fields"):
        data = obj._asdict()
        data["class"] = obj.__class__.__name__
        return data
    elif isinstance(obj, Enum) and hasattr(obj, "value"):
        return obj.value
    elif hasattr(obj, "__dict__"):
        obj_copy = obj.__dict__
        for i in inspect.getmembers(obj):
            if not i[0].startswith("_") and not inspect.ismethod(i[1]):
                obj_copy[i[0]] = encode_packet(getattr(obj, i[0]))
        obj = obj_copy
    return obj
