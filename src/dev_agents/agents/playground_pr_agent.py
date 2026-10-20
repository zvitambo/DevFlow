import os
import re
import uuid
from typing import List, Optional, Tuple
from dotenv import load_dotenv
import requests
from infrastructure.appsettings import settings
from pymongo import MongoClient
from agents import Agent, function_tool, Runner
from agents.memory import Session
from ..agents.playground_chat_agent import ChatHistoryManager
# Load environment variables
load_dotenv()


# OpenAI API Key
api_key = settings.openai_api_key
if not api_key:
    print("⚠️ Warning: OPENAI_API_KEY not found")
else:
    print("✓ OpenAI API key loaded successfully")

# MongoDB Configuration
# For Docker Compose setup with authentication
MONGODB_URI = 'mongodb://admin:admin@mongodb:27017/?authSource=admin'
MONGODB_DB = os.getenv('MONGODB_DB', 'numeric_agent_db')


def initialise_db():
    try:
        mongo_client = MongoClient(MONGODB_URI)
        # Test the connection
        mongo_client.server_info()
        db = mongo_client[MONGODB_DB]
        print(f"✓ Connected to MongoDB at {MONGODB_URI}")
        print(f"✓ Using database: {MONGODB_DB}")
        return db
    except Exception as e:
        print(f"⚠️ Error connecting to MongoDB: {e}")
        print("Please ensure MongoDB is running (docker-compose up -d)")




# Initialize the manager
db = initialise_db()
history_manager = ChatHistoryManager(db)
print("✓ Chat History Manager initialized")

class MongoDBSession(Session):
    """Custom session implementation backed by ChatHistoryManager."""

    def __init__(self, session_id: str, agent_name: str, history_manager: ChatHistoryManager):
        self.session_id = session_id
        self.agent_name = agent_name
        self.history_manager = history_manager

    async def get_items(self, limit: Optional[int] = None) -> List[dict]:
        """Retrieve conversation history for the session."""
        items = self.history_manager.get_history(
            self.agent_name, self.session_id)
        if limit:
            return items[-limit:]
        return items

    async def add_items(self, items: List[dict]) -> None:
        """Store new items for the session."""
        for item in items:
            self.history_manager.save_message(
                self.agent_name, self.session_id, item)

    async def pop_item(self) -> Optional[dict]:
        """Remove and return the most recent item from the session."""
        return self.history_manager.pop_message(self.agent_name, self.session_id)

    async def clear_session(self) -> None:
        """Clear all items for the session."""
        self.history_manager.clear_history(self.agent_name, self.session_id)


# Load environment variables
load_dotenv()


# OpenAI API Key
api_key = settings.openai_api_key
if not api_key:
    print("⚠️ Warning: OPENAI_API_KEY not found")
else:
    print("✓ OpenAI API key loaded successfully")

# MongoDB Configuration
# For Docker Compose setup with authentication
MONGODB_URI = 'mongodb://admin:admin@mongodb:27017/?authSource=admin'
MONGODB_DB = os.getenv('MONGODB_DB', 'numeric_agent_db')


def initialise_db():
    try:
        mongo_client = MongoClient(MONGODB_URI)
        # Test the connection
        mongo_client.server_info()
        db = mongo_client[MONGODB_DB]
        print(f"✓ Connected to MongoDB at {MONGODB_URI}")
        print(f"✓ Using database: {MONGODB_DB}")
        return db
    except Exception as e:
        print(f"⚠️ Error connecting to MongoDB: {e}")
        print("Please ensure MongoDB is running (docker-compose up -d)")


class ChatHistoryManager:
    """Manages chat history storage in MongoDB"""

    def __init__(self, db, collection_name: str = "numeric_agent_history"):
        self.collection = db[collection_name]

    def save_message(self, chat_id: str, role: str, content: str):
        """Save a message to the chat history"""
        message = {
            "role": role,
            "content": content
        }
        self.collection.update_one(
            {"_id": chat_id},
            {"$push": {"messages": message}},
            upsert=True
        )
        print(f"💾 Saved {role} message to chat {chat_id[:8]}...")

    def get_history(self, chat_id: str) -> List[dict]:
        """Retrieve all messages for a chat session"""
        doc = self.collection.find_one({"_id": chat_id})
        if not doc or "messages" not in doc:
            return []
        return doc["messages"]

    def clear_history(self, chat_id: str):
        """Clear the chat history for a specific chat"""
        self.collection.update_one(
            {"_id": chat_id},
            {"$set": {"messages": []}}
        )
        print(f"🗑️ Cleared history for chat {chat_id[:8]}...")

    def delete_chat(self, chat_id: str):
        """Delete a specific chat"""
        self.collection.delete_one({"_id": chat_id})
        print(f"🗑️ Deleted chat {chat_id[:8]}...")

    def get_all_chat_ids(self) -> List[str]:
        """Get all chat session IDs"""
        return [doc["_id"] for doc in self.collection.find({}, {"_id": 1})]


# Initialize the manager
db = initialise_db()
history_manager = ChatHistoryManager(db)
print("✓ Chat History Manager initialized")
