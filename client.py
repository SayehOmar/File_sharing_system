import asyncio
import websockets
import os
import json

SERVER_IP = "192.168.1.X"  # Replace with your Windows laptop's IP
UPLOADS_FOLDER = "Uploads"


async def send_file():
    """Monitors the Uploads folder and sends new files to the server."""
    sent_files = set()

    while True:
        for filename in os.listdir(UPLOADS_FOLDER):
            if filename.endswith(".zip") and filename not in sent_files:
                file_path = os.path.join(UPLOADS_FOLDER, filename)

                with open(file_path, "rb") as f:
                    file_content = f.read()

                file_info = json.dumps(
                    {
                        "filename": filename,
                        "content": file_content.decode(
                            errors="ignore"
                        ),  # Convert to string
                    }
                )

                async with websockets.connect(f"ws://{SERVER_IP}:8765") as websocket:
                    await websocket.send(file_info)
                    print(f"📤 Sent file: {filename} to {SERVER_IP}")
                    sent_files.add(filename)

        await asyncio.sleep(5)  # Check every 5 seconds


async def main():
    print(f"🚀 Connecting to server at {SERVER_IP}:8765...")
    await send_file()


if __name__ == "__main__":
    asyncio.run(main())
