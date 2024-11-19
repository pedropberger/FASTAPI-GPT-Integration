from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import sqlite3
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
ENDPOINT = os.getenv("ENDPOINT")

if not API_KEY or not ENDPOINT:
    raise ValueError("One or more environment variables are missing. Please check your .env file.")

# FastAPI instance
app = FastAPI()

# Database setup
DB_NAME = "responses.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            completion_id TEXT,
            model_used TEXT,
            created_timestamp TEXT,
            content TEXT,
            prompt_tokens INTEGER,
            completion_tokens INTEGER,
            total_tokens INTEGER
        )
        """)
        conn.commit()

init_db()

# Request payload schema
class MessageContent(BaseModel):
    type: str
    text: str

class Message(BaseModel):
    role: str
    content: List[MessageContent]

class Payload(BaseModel):
    messages: List[Message]
    temperature: float
    top_p: float
    max_tokens: int

# FastAPI route
@app.post("/process-payload/")
async def process_payload(payload: Payload):
    # Send the request to the external API
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload.dict())
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to contact external API: {e}")

    response_data = response.json()

    # Extract relevant fields
    try:
        message = payload.dict()
        completion_id = response_data.get("id")
        model_used = response_data.get("model", "unknown")
        created_timestamp = datetime.utcfromtimestamp(response_data.get("created", datetime.utcnow().timestamp()))
        content = response_data["choices"][0]["message"]["content"]
        usage = response_data.get("usage", {})
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        total_tokens = usage.get("total_tokens", 0)
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Unexpected response structure: {e}")

    # Store the data in the database
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO responses (message, completion_id, model_used, created_timestamp, content, prompt_tokens, completion_tokens, total_tokens)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(message),
                completion_id,
                model_used,
                created_timestamp.isoformat(),
                content,
                prompt_tokens,
                completion_tokens,
                total_tokens
            ))
            conn.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    # Return the content
    return {"content": content}
