
import asyncio
from client import Client, ClientConfig, GameConfig

if __name__ == "__main__":
    client = Client(ClientConfig(53528, "JK", ""), GameConfig("Factorio", ""))
    asyncio.run(client.run())