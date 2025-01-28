
import asyncio
import threading 
from client import Client, ClientConfig, GameConfig

if __name__ == "__main__":
    client = Client(ClientConfig(55224, "JK", ""), GameConfig("Factorio"))
    task = asyncio.run(client.run())
    asyncio.wait