from pymongo import MongoClient
from datetime import datetime

# ✅ MongoDB connection string (must be a string)
MONGO_URI = "mongodb+srv://ahmedtammam458:JphqpRHTVV8RR5q9@cluster0.3cubnzr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# ✅ Connect to MongoDB
client = MongoClient(MONGO_URI)

# ✅ Use database "medical_chatbot"
db = client["medical_chatbot"]

# ✅ Use collection "chats"
chat_collection = db["chats"]

# ✅ Save a single chat record
def save_chat(username, prompt, response):
    chat_doc = {
        "username": username,
        "prompt": prompt,
        "response": response,
        "timestamp": datetime.now().isoformat()
    }
    chat_collection.insert_one(chat_doc)

# ✅ Get all chat history for a user
def get_chat_history(username):
    return list(chat_collection.find({"username": username}))
