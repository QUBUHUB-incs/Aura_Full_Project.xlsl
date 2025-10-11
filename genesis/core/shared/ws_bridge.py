import asyncio
import json
import websockets
from core.shared.utils import AuraLogger

logger = AuraLogger("WSBridge")

class WSBridge:
    """Bridges Python MessageBus to WebPlugin WebSocket server"""
    def __init__(self, bus, ws_url="ws://localhost:8080"):
        self.bus = bus
        self.ws_url = ws_url

    async def start(self):
        logger.info(f"Connecting WSBridge to {self.ws_url}...")
        async with websockets.connect(self.ws_url) as ws:
            # Subscribe to relevant channels
            self.bus.subscribe("mood", lambda data: self.send(ws, data))
            self.bus.subscribe("thought", lambda data: self.send(ws, data))
            await asyncio.Future()  # Keep running

    async def send(self, ws, data):
        try:
            await ws.send(json.dumps(data))
        except Exception as e:
            logger.info(f"⚠️ WSBridge send error: {e}")
