import os
import uuid
from developer_agents.src.dev_agents.tools.mathematical_tools import compute_exponential, compute_factorial, compute_fibonacci
from infrastructure.appsettings import settings
from typing import List
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from pymongo import MongoClient

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
MONGODB_URI = ''
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


agent = Agent(
    name="Numeric Computation Agent with History",
    instructions=(
        "You are a numeric computation specialist with conversation memory. "
        "You can calculate factorial, exponential (power), and Fibonacci numbers. "
        "You remember previous calculations in the conversation. "
        "When the user asks for computations, use the appropriate tool. "
        "For factorial, use `compute_factorial`. "
        "For exponential (power), use `compute_exponential`. "
        "For Fibonacci, use `compute_fibonacci`. "
        "You can reference previous calculations when answering follow-up questions."
    ),
    model="gpt-5-mini",
    tools=[compute_factorial, compute_exponential, compute_fibonacci],
)

print("✓ Agent initialized successfully")


async def chat_with_history(chat_id: str, user_message: str):
    """
    Send a message to the agent with conversation history.
    
    Args:
        chat_id: The chat session ID
        user_message: The user's message
        
    Returns:
        The agent's response
    """
    # Save user message to history
    history_manager.save_message(chat_id, "user", user_message)

    # Get conversation history
    history = history_manager.get_history(chat_id)

    # Build context from history for the agent
    context_messages = []
    for msg in history:
        context_messages.append(f"{msg['role']}: {msg['content']}")

    # Create input with full conversation context
    full_input = "\n".join(context_messages)

    # Run the agent with context
    result = await Runner.run(agent, input=full_input)
    response = str(result.final_output)

    # Save assistant response to history
    history_manager.save_message(chat_id, "assistant", response)

    return response

print("✓ Chat function created")


# Generate a unique chat session ID
chat_id = str(uuid.uuid4())
print(f"🆕 New chat session created: {chat_id}")


async def run_chat_agent():
 
    response = await chat_with_history(chat_id, "Calculate the factorial of 3")
    print(f"Agent: {response}")

    print("=" * 60)
    print("... 🧐" * 60)

    response = await chat_with_history(
        chat_id,
        "Can you calculate 2 raised to the power of the number you just computed?"
    )
    print(f"Agent: {response}")


