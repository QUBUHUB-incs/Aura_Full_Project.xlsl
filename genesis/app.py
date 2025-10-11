import asyncio
import json
from core.shared.message_bus import MessageBus
from core.neuro.neural_core import NeuroCore
from core.daemon.daemon_loop import AuraDaemon
from core.shared.utils import AuraLogger

logger = AuraLogger("Aura")

async def main():
    logger.info("🌌 Initializing Aura Genesis System...")

    # Initialize the message bus
    bus = MessageBus()

    # Initialize cores
    neuro = NeuroCore(bus)
    daemon = AuraDaemon(bus)

    # Run both systems concurrently
    await asyncio.gather(
        neuro.run(),
        daemon.run()
    )

if __name__ == "__main__":
    asyncio.run(main())
