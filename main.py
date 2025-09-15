from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # Leser .env fil

app = FastAPI()

# CORS – lar frontend kommunisere med API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Les verdiene fra .env
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

def get_connection():
    conn = psycopg2.connect(
        dbname=DBNAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    return conn

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
