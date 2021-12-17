from typing import Optional

import pytest

from saturn_engine.worker.inventories import BlockingInventory
from saturn_engine.worker.inventories import Item


@pytest.mark.asyncio
async def test_blocking_inventory() -> None:
    class BI(BlockingInventory):
        def next_batch_blocking(self, after: Optional[str] = None) -> list[Item]:
            # Don't really block here as we want tests to be fast.
            # This still tests almost completely that BlockingInventory works.
            return [Item(id="66", args={"after": after})]

    batch = list(await BI.from_options(dict()).next_batch())
    assert batch[0] == Item(id="66", args={"after": None})

    batch = list(await BI.from_options(dict()).next_batch(after="20"))
    assert batch[0] == Item(id="66", args={"after": "20"})
