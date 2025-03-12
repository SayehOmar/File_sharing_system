import asyncio
import websockets
import os
import json

UPLOADS_FOLDER = "Uploads"


async def handler(websocket, path):
    """Handles incoming file sync requests."""
    print(f"🔗 New connection from {websocket.remote_address}")

    while True:
        try:
            message = await websocket.recv()
            file_info = json.loads(message)

            filename = file_info["filename"]
            file_content = file_info["content"].encode()

            file_path = os.path.join(UPLOADS_FOLDER, filename)
            with open(file_path, "wb") as f:
                f.write(file_content)

            print(f"✅ Received and saved: {filename}")
        except websockets.exceptions.ConnectionClosed:
            print("⚠️ Connection lost.")
            break


async def main():
    server = await websockets.serve(
        handler, "0.0.0.0", 8765
    )  # Listen on all interfaces
    print("🚀 WebSocket Server Running on port 8765...")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
