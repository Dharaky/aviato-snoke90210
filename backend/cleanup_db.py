
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'aviato_db')

async def cleanup_duplicates():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("Scanning for duplicates...")
    
    # Get all conversations
    conversations = await db.conversations.find().to_list(1000)
    
    # Group by sorted participants tuple
    seen = {}
    duplicates = []
    
    for conv in conversations:
        participants = tuple(sorted(conv['participants']))
        if participants in seen:
            duplicates.append(conv['_id'])
        else:
            seen[participants] = conv['_id']
            
    print(f"Found {len(duplicates)} duplicate conversations.")
    
    if duplicates:
        result = await db.conversations.delete_many({"_id": {"$in": duplicates}})
        print(f"Deleted {result.deleted_count} duplicates.")
    else:
        print("No duplicates found.")

if __name__ == "__main__":
    asyncio.run(cleanup_duplicates())
