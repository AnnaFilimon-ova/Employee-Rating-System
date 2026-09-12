from fastapi import FastAPI
from database import connect
from pydantic import BaseModel

app = FastAPI()

#We see a list of managers.
@app.get("/")
def get_users():
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

#We add a manager.
@app.post("/users")
def add_users(user: User):
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