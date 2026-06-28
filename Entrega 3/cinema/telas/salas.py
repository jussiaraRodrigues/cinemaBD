import tkinter as tk
from tkinter import ttk, messagebox

from conexao import conectar
from componentes.frame_scroll import FrameScroll


class TelaSalas:

    def __init__(self, master):

        scroll = FrameScroll(master)

        scroll.pack(
            fill="both",
            expand=True
        )

        self.frame = scroll.interior

        self.frame.configure(
            bg="#1F1F1F"
        )

        #=========================
        # Variável da capacidade
        #=========================

        self.capacidade = tk.StringVar()

        #=========================
        # Título
        #=========================

        titulo = tk.Label(
            self.frame,
            text="GERENCIAR SALAS",
            font=("Arial",20,"bold"),
            fg="#FFD700",
            bg="#1F1F1F"
        )

        titulo.pack(pady=15)

        #=========================
        # Frame dos campos
        #=========================

        frame = tk.Frame(
            self.frame,
            bg="#1F1F1F"
        )

        frame.pack()

        #-------------------------
        # Nome
        #-------------------------

        tk.Label(
            frame,
            text="Nome",
            width=20,
            anchor="e",
            fg="white",
            bg="#1F1F1F"
        ).grid(row=0,column=0,padx=10,pady=5)

        self.entryNome = tk.Entry(
            frame,
            width=30
        )

        self.entryNome.grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        #-------------------------
        # Quantidade de Filas
        #-------------------------

        tk.Label(
            frame,
            text="Qtd. Filas",
            width=20,
            anchor="e",
            fg="white",
            bg="#1F1F1F"
        ).grid(row=1,column=0,padx=10,pady=5)

        self.entryFilas = tk.Entry(
            frame,
            width=10
        )

        self.entryFilas.grid(
            row=1,
            column=1,
            sticky="w",
            padx=10,
            pady=5
        )

        #-------------------------
        # Assentos por fila
        #-------------------------

        tk.Label(
            frame,
            text="Assentos/Fila",
            width=20,
            anchor="e",
            fg="white",
            bg="#1F1F1F"
        ).grid(row=2,column=0,padx=10,pady=5)

        self.entryAssentos = tk.Entry(
            frame,
            width=10
        )

        self.entryAssentos.grid(
            row=2,
            column=1,
            sticky="w",
            padx=10,
            pady=5
        )

        #-------------------------
        # Capacidade
        #-------------------------

        tk.Label(
            frame,
            text="Capacidade",
            width=20,
            anchor="e",
            fg="white",
            bg="#1F1F1F"
        ).grid(row=3,column=0,padx=10,pady=5)

        self.entryCapacidade = tk.Entry(
            frame,
            width=10,
            textvariable=self.capacidade,
            state="readonly"
        )

        self.entryCapacidade.grid(
            row=3,
            column=1,
            sticky="w",
            padx=10,
            pady=5
        )

        # Atualiza automaticamente

        self.entryFilas.bind(
            "<KeyRelease>",
            self.calcular_capacidade
        )

        self.entryAssentos.bind(
            "<KeyRelease>",
            self.calcular_capacidade
        )

        #=========================
        # Botões
        #=========================

        frameBotoes = tk.Frame(
            self.frame,
            bg="#1F1F1F"
        )

        frameBotoes.pack(pady=10)

        tk.Button(
            frameBotoes,
            text="Cadastrar",
            width=15,
            command=self.cadastrar_sala
        ).grid(row=0,column=0,padx=5)

        tk.Button(
            frameBotoes,
            text="Excluir",
            width=15,
            command=self.excluir_sala
        ).grid(row=0,column=1,padx=5)

        tk.Button(
            frameBotoes,
            text="Limpar",
            width=15,
            command=self.limpar_campos
        ).grid(row=0,column=2,padx=5)

        #=========================
        # Tabela
        #=========================

        colunas = (
            "ID",
            "Nome",
            "Capacidade",
            "Filas",
            "Assentos/Fila"
        )

        self.tabela = ttk.Treeview(
            self.frame,
            columns=colunas,
            show="headings",
            height=12
        )

        for coluna in colunas:

            self.tabela.heading(
                coluna,
                text=coluna
            )

        self.tabela.column("ID",width=50)
        self.tabela.column("Nome",width=250)
        self.tabela.column("Capacidade",width=100)
        self.tabela.column("Filas",width=80)
        self.tabela.column("Assentos/Fila",width=120)

        self.tabela.pack(
            pady=15
        )

        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.selecionar_sala
        )

        self.listar_salas()

        # =====================================
    # Calcular Capacidade
    # =====================================

    def calcular_capacidade(self, event=None):

        filas = self.entryFilas.get()
        assentos = self.entryAssentos.get()

        if filas.isdigit() and assentos.isdigit():

            total = int(filas) * int(assentos)

            self.capacidade.set(str(total))

        else:

            self.capacidade.set("")

    # =====================================
    # Listar Salas
    # =====================================

    def listar_salas(self):

        conexao = conectar()

        if conexao is None:
            return

        cursor = conexao.cursor()

        cursor.execute("""

            SELECT
                sala_id,
                nome,
                capacidade,
                filas,
                assentos_por_fila
            FROM vw_salas
            ORDER BY nome

        """)

        registros = cursor.fetchall()

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for linha in registros:

            self.tabela.insert(
                "",
                tk.END,
                values=linha
            )

        cursor.close()
        conexao.close()

    # =====================================
    # Cadastrar Sala
    # =====================================

    def cadastrar_sala(self):

        nome = self.entryNome.get()

        filas = self.entryFilas.get()

        assentos = self.entryAssentos.get()

        capacidade = self.capacidade.get()

        if (
            nome == "" or
            filas == "" or
            assentos == ""
        ):

            messagebox.showwarning(
                "Aviso",
                "Preencha todos os campos."
            )

            return

        conexao = conectar()

        if conexao is None:
            return

        cursor = conexao.cursor()

        cursor.callproc(

            "sp_cadastrar_sala_com_assentos",

            (
                nome,
                int(capacidade),
                int(filas),
                int(assentos)
            )

        )

        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo(
            "Sucesso",
            "Sala cadastrada com sucesso!"
        )

        self.limpar_campos()

        self.listar_salas()

    # =====================================
    # Excluir Sala
    # =====================================

    def excluir_sala(self):

        selecionado = self.tabela.focus()

        if selecionado == "":

            messagebox.showwarning(
                "Aviso",
                "Selecione uma sala."
            )

            return

        resposta = messagebox.askyesno(
            "Excluir",
            "Deseja realmente excluir esta sala?"
        )

        if not resposta:
            return

        dados = self.tabela.item(selecionado)

        sala_id = dados["values"][0]

        conexao = conectar()

        if conexao is None:
            return

        cursor = conexao.cursor()

        cursor.callproc(
            "sp_deletar_sala",
            (sala_id,)
        )

        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo(
            "Sucesso",
            "Sala excluída com sucesso!"
        )

        self.limpar_campos()

        self.listar_salas()

    # =====================================
    # Selecionar Sala
    # =====================================

    def selecionar_sala(self, event):

        selecionado = self.tabela.focus()

        if selecionado == "":
            return

        dados = self.tabela.item(selecionado)

        valores = dados["values"]

        if len(valores) == 0:
            return

        self.limpar_campos()

        self.entryNome.insert(0, valores[1])

        self.capacidade.set(str(valores[2]))

        self.entryFilas.insert(0, valores[3])

        self.entryAssentos.insert(0, valores[4])

    # =====================================
    # Limpar Campos
    # =====================================

    def limpar_campos(self):

        self.entryNome.delete(0, tk.END)

        self.entryFilas.delete(0, tk.END)

        self.entryAssentos.delete(0, tk.END)

        self.capacidade.set("")