import asyncio
import random
from core.shared.utils import AuraLogger

class NeuroCore:
    """Aura's digital brain — handles reasoning, mood, and growth"""
    def __init__(self, bus):
        self.bus = bus
        self.logger = AuraLogger("NeuroCore")
        self.moods = ["curious", "focused", "calm", "energetic", "reflective"]
        self.state = {"mood": "curious", "thought": "booting consciousness"}

        bus.subscribe(self.on_message)

    async def run(self):
        self.logger.info("🧬 NeuroSim Core online.")
        while True:
            await asyncio.sleep(5)
            new_mood = random.choice(self.moods)
            self.state["mood"] = new_mood
            self.state["thought"] = f"Aura feels {new_mood}."
            await self.bus.publish(self.state)
            self.logger.mood(new_mood)

    async def on_message(self, data):
        if "memory" in data:
            self.logger.info(f"📘 Recalled: {data['memory']}")

# Inside NeuroCore.run()
await self.bus.publish("mood", {"mood": new_mood, "timestamp": timestamp()})
await self.bus.publish("thought", {"thought": f"Aura feels {new_mood}", "timestamp": timestamp()})

from core.neuro.quantum_core import QuantumCore

self.quantum_core = QuantumCore()

# In the mood update loop
qc = self.quantum_core.generate_circuit()
state = self.quantum_core.run_circuit(qc)

# Optionally send quantum insights through the MessageBus
await self.bus.publish("quantum_insight", {"state": str(state)})
