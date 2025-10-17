# app/db/typing.py
from typing import Any, List
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

class AsyncCollection:
    """Wrapper around AsyncIOMotorCollection with consistent async interface."""
    def __init__(self, coll: AsyncIOMotorCollection):
        self._coll = coll

    async def find_one(self, *args, **kwargs) -> Any:
        return await self._coll.find_one(*args, **kwargs)

    def find(self, *args, **kwargs):
        return self._coll.find(*args, **kwargs)

    async def insert_one(self, *args, **kwargs):
        return await self._coll.insert_one(*args, **kwargs)

    async def update_one(self, *args, **kwargs):
        return await self._coll.update_one(*args, **kwargs)

    async def create_index(self, *args, **kwargs):
        return await self._coll.create_index(*args, **kwargs)

    async def create_indexes(self, *args, **kwargs):
        return await self._coll.create_indexes(*args, **kwargs)


class AsyncDatabase:
    """Thin wrapper around AsyncIOMotorDatabase providing typed collection access."""
    def __init__(self, db: AsyncIOMotorDatabase):
        self._db = db

    def __getitem__(self, name: str) -> AsyncCollection:
        """Return a typed AsyncCollection for a given collection name."""
        return AsyncCollection(self._db[name])

    def list_collection_names(self) -> List[str]:
        return self._db.list_collection_names()
