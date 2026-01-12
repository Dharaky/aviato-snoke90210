
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'aviato_db')

async def check_conversations():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    users = await db.users.find().to_list(100)
    print("Users:")
    for u in users:
        print(f"ID: {u['_id']}, Name: {u['name']}")
        
    print("\nConversations:")
    conversations = await db.conversations.find().to_list(100)
    for c in conversations:
        print(f"ID: {c['_id']}, Participants: {c['participants']}")

if __name__ == "__main__":
    asyncio.run(check_conversations())
