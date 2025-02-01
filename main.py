
import asyncio
from client import Client, ClientConfig, GameConfig

async def main():
    client = Client(ClientConfig(55224, "JK", ""), GameConfig("Factorio"))
    await client.run()
    
if __name__ == "__main__":
    asyncio.run(main())