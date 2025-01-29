"""Takes care of the caching and translating of Location/Items"""

import json
from pathlib import Path
import os

from client.packets.server import DataPackage

_path : Path = Path(Path(__file__).parent.resolve().absolute(), "game_cache")

_game_data_cache = {}
if not os.path.isdir(_path):
    _path.mkdir()

def cache_exist(checksum : str) -> bool:
    return os.path.isfile(Path(_path, f"{checksum}.json"))

def save_cache(package : DataPackage):
    for key,game in package.data["games"].items():
        if not os.path.exists(Path(_path, f"{game['checksum']}.json")):
            with open(Path(_path, f"{game['checksum']}.json"), "w") as file :
                file.write(json.dumps(game))
        _game_data_cache[key] = game