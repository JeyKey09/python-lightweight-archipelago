
import asyncio
import threading 
from client import Client, ClientConfig, GameConfig

if __name__ == "__main__":
    client = Client(ClientConfig(53528, "JK", ""), GameConfig("Factorio", ""))
    thread = threading.Thread(None,client.run)
    thread.start()
    thread.join()
    