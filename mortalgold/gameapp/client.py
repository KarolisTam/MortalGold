#client.py
import asyncio
import websockets

async def connect_to_server():
    async with websockets.connect('ws://localhost:8001/ws/') as websocket:
        while True:
            # Send data to the server
            await websocket.send("Hello, server!")

            # Receive data from the server
            response = await websocket.recv()
            print(response)

async def main():
    await connect_to_server()

# Create and run the event loop
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()

