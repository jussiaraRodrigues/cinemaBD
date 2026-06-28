import mysql.connector
from tkinter import messagebox


def conectar():

    try:

        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",          # Coloque sua senha aqui
            database="cinema"
        )

        return conexao

    except mysql.connector.Error as erro:

        messagebox.showerror(
            "Erro de conexão",
            f"Não foi possível conectar ao banco.\n\n{erro}"
        )

        return None
