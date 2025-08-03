import asyncio
import redis.asyncio as aioredis  # if you want to keep the same naming
import json
import logging
from typing import Dict, Any, Callable, List
from datetime import datetime

logger = logging.getLogger(__name__)

class EventBus:
    """Redis-based event bus for agent communication"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis = None
        self.pubsub = None
        self.subscribers = {}
        self.running = False
        
    async def connect(self):
        """Connect to Redis"""
        try:
            self.redis = aioredis.Redis.from_url(self.redis_url)
            
            logger.info("Connected to Redis event bus")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from Redis"""
        self.running = False
        if self.pubsub:
            await self.pubsub.close()
        if self.redis:
            await self.redis.close()
        logger.info("Disconnected from Redis")
    
    async def publish(self, channel: str, message: Dict[str, Any]):
        """Publish message to channel"""
        try:
            if not self.redis:
                await self.connect()
            
            # Add metadata
            enriched_message = {
                **message,
                "timestamp": datetime.now().isoformat(),
                "channel": channel
            }
            
            await self.redis.publish(channel, json.dumps(enriched_message))
            logger.debug(f"Published to {channel}: {message}")
            
        except Exception as e:
            logger.error(f"Failed to publish to {channel}: {e}")
            raise
    
    async def subscribe(self, channel: str, callback: Callable):
        """Subscribe to channel with callback"""
        try:
            if channel not in self.subscribers:
                self.subscribers[channel] = []
            
            self.subscribers[channel].append(callback)
            await self.pubsub.subscribe(channel)
            logger.info(f"Subscribed to channel: {channel}")
            
        except Exception as e:
            logger.error(f"Failed to subscribe to {channel}: {e}")
            raise
    
    async def start_listening(self):
        """Start listening for messages"""
        if not self.pubsub:
            await self.connect()
        
        self.running = True
        logger.info("Started listening for events")
        
        try:
            while self.running:
                message = await self.pubsub.get_message(timeout=1.0)
                if message and message['type'] == 'message':
                    await self._handle_message(message)
                    
        except Exception as e:
            logger.error(f"Error in event loop: {e}")
        finally:
            logger.info("Stopped listening for events")
    
    async def _handle_message(self, message):
        """Handle incoming message"""
        try:
            channel = message['channel'].decode('utf-8')
            data = json.loads(message['data'].decode('utf-8'))
            
            if channel in self.subscribers:
                for callback in self.subscribers[channel]:
                    await callback(channel, data)
                    
        except Exception as e:
            logger.error(f"Error handling message: {e}")

# Global event bus instance
event_bus = EventBus()
