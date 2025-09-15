from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from urllib.parse import urlparse

app = FastAPI()

# CORS – lar frontend kommunisere med API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# Hent Railway DATABASE_URL fra miljøvariabler
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# Skjema for data
class UserData(BaseModel):
    name: str
    email: str
    message: str = None

@app.get("/users")
def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_data")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"users": rows}

@app.post("/users")
def add_user(user: UserData):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users_data (name, email, message) VALUES (%s, %s, %s)",
        (user.name, user.email, user.message)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User added successfully!", "data": user}
