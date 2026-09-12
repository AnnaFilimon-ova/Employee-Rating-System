from multiprocessing import connection
from fastapi import FastAPI
import psycopg2
from database import connect

app = FastAPI()

@app.get("/")
def Users():
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
