# server.py
import asyncio
import os
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
    # Use PORT from environment (for Render.com), default to 8765 if local
    port = int(os.environ.get("PORT", 8765))
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"WebSocket server running on port {port}")
        await asyncio.Future()  # run forever

asyncio.run(main())

