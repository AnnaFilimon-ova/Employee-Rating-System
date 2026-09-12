from fastapi import FastAPI
from database import connect
from pydantic import BaseModel

app = FastAPI()

#We see a list of managers.
@app.get("/")
def Get_managers():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "id": user[0],
            "name": user[1],
            "password": user[2],
            "status": user[3]
        }
        for user in users
    ]

class User(BaseModel):
    name: str
    password: str

#Manager sign up
@app.post("/users")
def Register_manager(user: User):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO users (name, password)
        VALUES (%s, %s)
        """,
        (user.name, user.password)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return {"message": "User added successfully"}

#Manager sign in
@app.post("/login")
def Login_manager(user: User):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        """
        select id, name, status from users
        where name = %s and password = %s
        """,
        (user.name, user.password)
    )

    manager = cursor.fetchone()
    cursor.close()
    connection.close()

    if manager is None:
        return {"message": "User not found"}

    return {
        "message": "Logged in successfully",
        "id": manager[0],
        "name": manager[1],
        "status": manager[2]
    }