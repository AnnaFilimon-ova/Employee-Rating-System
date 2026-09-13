from fastapi import FastAPI, HTTPException
from database import connect
from pydantic import BaseModel, Field
import bcrypt

app = FastAPI()

#We see a list of managers.
@app.get("/")
def get_managers():
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT id, name, status FROM users")
        users = cursor.fetchall()

        return [
            {
                "id": user[0],
                "name": user[1],
                "status": user[2]
            }
            for user in users
        ]
    finally:
        cursor.close()
        connection.close()

class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=9, max_length=50)

class LoginRequest(BaseModel):
    name: str
    password: str

#Manager sign up
@app.post("/users")
def register_manager(user: RegisterRequest):
    connection = connect()
    cursor = connection.cursor()

    try:
        hashed_password = bcrypt.hashpw(
            user.password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute(
            """
            INSERT INTO users (name, password)
            VALUES (%s, %s)
            returning id, name, status
            """,
            (user.name, hashed_password)
        )

        manager = cursor.fetchone()
        connection.commit()
        return {
            "message": "Registration is successfully",
            "id": manager[0],
            "name": manager[1],
            "status": manager[2]
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

#Manager sign in
@app.post("/login")
def login_manager(user: LoginRequest):
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            select id, name, password, status from users
            where name = %s 
            """,
            (user.name,)
        )

        manager = cursor.fetchone()

        if manager is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        password_correct = bcrypt.checkpw(
            user.password.encode("utf-8"),
            manager[2].encode("utf-8")
        )

        if not password_correct:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        return {
            "message": "Logged in successfully",
            "id": manager[0],
            "name": manager[1],
            "status": manager[3]
        }

    finally:
        cursor.close()
        connection.close()