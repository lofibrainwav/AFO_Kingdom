"""
[Eternity: 永] AsyncRedisSaver for LangGraph Persistence.
Implements the CheckpointSaver interface using Redis to preserve the Kingdom's memories forever.
"""

import json
from collections.abc import AsyncIterator
from typing import Any

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import (
    BaseCheckpointSaver,
    Checkpoint,
    CheckpointMetadata,
    CheckpointTuple,
)
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

from AFO.utils.cache_utils import cache


class AsyncRedisSaver(BaseCheckpointSaver):
    """
    Redis-based Checkpoint Saver for LangGraph.
    Stores graph state in Redis to ensure [Eternity].
    """

    def __init__(self, key_prefix: str = "chancellor_checkpoint:"):
        super().__init__()
        self.key_prefix = key_prefix
        self.serde = JsonPlusSerializer()

    def get_tuple(self, config: RunnableConfig) -> CheckpointTuple | None:
        """Get a checkpoint tuple from Redis."""
        thread_id = config["configurable"]["thread_id"]
        key = f"{self.key_prefix}{thread_id}"

        if not cache.enabled or not cache.redis:
            return None

        # Fetch latest checkpoint
        data = cache.redis.get(key)
        if not data:
            return None

        try:
            saved_state = json.loads(data)
            checkpoint = self.serde.loads(saved_state["checkpoint"])
            metadata = self.serde.loads(saved_state["metadata"])
            parent_config = saved_state.get("parent_config")
            return CheckpointTuple(config, checkpoint, metadata, parent_config)
        except Exception as e:
            print(f"⚠️ Failed to load checkpoint: {e}")
            return None

    def list(
        self,
        config: RunnableConfig | None,
        *,
        filter: dict[str, Any] | None = None,
        before: RunnableConfig | None = None,
        limit: int | None = None,
    ) -> AsyncIterator[CheckpointTuple]:
        """List checkpoints (Not fully implemented for simple key-value)"""
        # Simplistic implementation: only returns current head if matches
        if config:
            latest = self.get_tuple(config)
            if latest:
                yield latest

    def put(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: dict[str, Any],
    ) -> RunnableConfig:
        """Save a checkpoint to Redis."""
        thread_id = config["configurable"]["thread_id"]
        key = f"{self.key_prefix}{thread_id}"

        if cache.enabled and cache.redis:
            try:
                # Serialize
                data = {
                    "checkpoint": self.serde.dumps(checkpoint),
                    "metadata": self.serde.dumps(metadata),
                    "parent_config": config,
                }
                # Save with persistence (TTL can be set if needed, but Eternity implies forever)
                # Setting 24h TTL for now to prevent memory leak until expiration policy is defined
                cache.redis.setex(key, 86400, json.dumps(data))
            except Exception as e:
                print(f"⚠️ Failed to save checkpoint to Redis: {e}")

        return {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_id": checkpoint["id"],
            }
        }
