import asyncio
import websockets

async def handle_client(websocket, path):
    print(f"Client connected from {websocket.remote_address}")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            response = {
                "status": "received",
                "original_message": message,
            }
            await websocket.send(json.dumps(response))
    except websockets.exceptions.ConnectionClosed:
        print(f"Client {websocket.remote_address} disconnected")

async def start_server():
    async with websockets.serve(handle_client, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # run forever

async def main():
    # Start server in background
    server_task = asyncio.create_task(start_server())
    # Give server time to start
    await asyncio.sleep(1)
    # Run client
    await client_example()
    # Stop server
    server_task.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
