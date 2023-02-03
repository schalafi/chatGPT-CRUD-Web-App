from fastapi import FastAPI, Body
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Define the database and user model
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            """)
conn.commit()

class User(BaseModel):
    email: str
    password: str

@app.post("/users")
async def create_user(user: User):
    cursor.execute("INSERT INTO users (email, password) VALUES (?,?)", (user.email, user.password))
    conn.commit()
    return {"message": "User created"}

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    if not user:
        return {"error": "User not found"}
    return {"email": user[1], "password": user[2]}

@app.put("/users/{user_id}")
async def update_user(user_id: int, email: str = Body(None), password: str = Body(None)):
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    if not user:
        return {"error": "User not found"}
    if email:
        cursor.execute("UPDATE users SET email=? WHERE id=?", (email, user_id))
    if password:
        cursor.execute("UPDATE users SET password=? WHERE id=?", (password, user_id))
    conn.commit()
    return {"message": "User updated"}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    return {"message": "User deleted"}
