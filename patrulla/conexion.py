import mysql.connector

def conectar():
    mybd = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database= "patrulla"
    )
    return mybd