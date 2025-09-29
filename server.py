# server.py
import asyncio
import websockets

clients = set()

async def handler(websocket):
    clients.add(websocket)
    print(f"Client connected: {websocket.remote_address}")
    try:
        async for message in websocket:
            # Broadcast message to all clients except sender
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except:
        pass
    finally:
        clients.remove(websocket)
        print(f"Client disconnected: {websocket.remote_address}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server running on port 8765")
        await asyncio.Future()  # run forever

asyncio.run(main())
