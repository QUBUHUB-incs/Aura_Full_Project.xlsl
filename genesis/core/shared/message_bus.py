import asyncio
import json

class MessageBus:
    """Shared async message bus for inter-core communication"""
    def __init__(self):
        self.subscribers = []

    def subscribe(self, callback):
        self.subscribers.append(callback)

    async def publish(self, data):
        for callback in self.subscribers:
            await callback(data)
