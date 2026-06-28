import tkinter as tk
from tkinter import ttk, messagebox

from conexao import conectar
from componentes.frame_scroll import FrameScroll


class TelaSessoes:

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

        self.filmes = {}
        self.salas = {}

        # ==================================
        # Título
        # ==================================

        titulo = tk.Label(
            self.frame,
            text="GERENCIAR SESSÕES",
            font=("Arial",20,"bold"),
            fg="#FFD700",
            bg="#1F1F1F"
        )

        titulo.pack(pady=15)

        # ==================================
        # Frame dos Campos
        # ==================================

        frame = tk.Frame(
            self.frame,
            bg="#1F1F1F"
        )

        frame.pack()

        # Filme

        tk.Label(
            frame,
            text="Filme",
            width=20,
            anchor="e",
            fg="white",
            bg="#1F1F1F"
        ).grid(row=0,column=0,padx=10,pady=5)

        self.comboFilme = ttk.Combobox(
            frame,
            width=35,
            state="readonly"
        )

        self.comboFilme.grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        # Sala

        tk.Label(
            frame,
            text="Sala",
            width=20,
            anchor="e",
            fg="white",
            bg="#1F1F1F"
        ).grid(row=1,column=0,padx=10,pady=5)

        self.comboSala = ttk.Combobox(
            frame,
            width=35,
            state="readonly"
        )

        self.comboSala.grid(
            row=1,
            column=1,
            padx=10,
            pady=5
        )

        # Data

        tk.Label(
            frame,
            text="Data",
            width=20,
            anchor="e",
            fg="white",
            bg="#1F1F1F"
        ).grid(row=2,column=0,padx=10,pady=5)

        self.entryData = tk.Entry(
            frame,
            width=20
        )

        self.entryData.grid(
            row=2,
            column=1,
            sticky="w",
            padx=10,
            pady=5
        )

        # Hora

        tk.Label(
            frame,
            text="Hora",
            width=20,
            anchor="e",
            fg="white",
            bg="#1F1F1F"
        ).grid(row=3,column=0,padx=10,pady=5)

        self.entryHora = tk.Entry(
            frame,
            width=20
        )

        self.entryHora.grid(
            row=3,
            column=1,
            sticky="w",
            padx=10,
            pady=5
        )

        # Idioma

        tk.Label(
            frame,
            text="Idioma",
            width=20,
            anchor="e",
            fg="white",
            bg="#1F1F1F"
        ).grid(row=4,column=0,padx=10,pady=5)

        self.comboIdioma = ttk.Combobox(
            frame,
            width=18,
            state="readonly",
            values=[
                "Dublado",
                "Legendado"
            ]
        )

        self.comboIdioma.grid(
            row=4,
            column=1,
            sticky="w",
            padx=10,
            pady=5
        )

        # Valor

        tk.Label(
            frame,
            text="Valor do Ingresso",
            width=20,
            anchor="e",
            fg="white",
            bg="#1F1F1F"
        ).grid(row=5,column=0,padx=10,pady=5)

        self.entryValor = tk.Entry(
            frame,
            width=20
        )

        self.entryValor.grid(
            row=5,
            column=1,
            sticky="w",
            padx=10,
            pady=5
        )

        # ==================================
        # Botões
        # ==================================

        frameBotoes = tk.Frame(
            self.frame,
            bg="#1F1F1F"
        )

        frameBotoes.pack(pady=10)

        tk.Button(
            frameBotoes,
            text="Cadastrar",
            width=15,
            command=self.cadastrar_sessao
        ).grid(row=0,column=0,padx=5)

        tk.Button(
            frameBotoes,
            text="Excluir",
            width=15,
            command=self.excluir_sessao
        ).grid(row=0,column=1,padx=5)

        tk.Button(
            frameBotoes,
            text="Limpar",
            width=15,
            command=self.limpar_campos
        ).grid(row=0,column=2,padx=5)

        # ==================================
        # Tabela
        # ==================================

        colunas = (
            "ID",
            "Filme",
            "Sala",
            "Capacidade",
            "Vendidos",
            "Livres",
            "Data/Hora",
            "Idioma"
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
        self.tabela.column("Filme",width=220)
        self.tabela.column("Sala",width=100)
        self.tabela.column("Capacidade",width=90)
        self.tabela.column("Vendidos",width=80)
        self.tabela.column("Livres",width=80)
        self.tabela.column("Data/Hora",width=150)
        self.tabela.column("Idioma",width=100)

        self.tabela.pack(pady=15)

        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.selecionar_sessao
        )

        self.carregar_filmes()
        self.carregar_salas()
        self.listar_sessoes()
    
    # =====================================
    # Carregar Filmes
    # =====================================

    def carregar_filmes(self):

        conexao = conectar()

        if conexao is None:
            return

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT filme_id, titulo
            FROM filme
            ORDER BY titulo
        """)

        self.filmes.clear()

        lista = []

        for filme_id, titulo in cursor.fetchall():

            self.filmes[titulo] = filme_id

            lista.append(titulo)

        self.comboFilme["values"] = lista

        cursor.close()
        conexao.close()

    # =====================================
    # Carregar Salas
    # =====================================

    def carregar_salas(self):

        conexao = conectar()

        if conexao is None:
            return

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                sala_id,
                nome,
                capacidade
            FROM vw_salas
            ORDER BY nome
        """)

        self.salas.clear()

        lista = []

        for sala_id, nome, capacidade in cursor.fetchall():

            texto = f"{nome} ({capacidade} lugares)"

            self.salas[texto] = sala_id

            lista.append(texto)

        self.comboSala["values"] = lista

        cursor.close()
        conexao.close()

    # =====================================
    # Listar Sessões
    # =====================================

    def listar_sessoes(self):

        conexao = conectar()

        if conexao is None:
            return

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                sessao_id,
                titulo,
                nome,
                capacidade,
                vendidos,
                disponiveis,
                data_hora,
                idioma
            FROM vw_sessoes
            ORDER BY data_hora
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
    # Cadastrar Sessão
    # =====================================

    def cadastrar_sessao(self):

        filme = self.comboFilme.get()

        sala = self.comboSala.get()

        data = self.entryData.get()

        hora = self.entryHora.get()

        idioma = self.comboIdioma.get()

        valor = self.entryValor.get().replace(",", ".")

        if (
            filme == "" or
            sala == "" or
            data == "" or
            hora == "" or
            idioma == "" or
            valor == ""
        ):

            messagebox.showwarning(
                "Aviso",
                "Preencha todos os campos."
            )

            return

        try:
            valor = float(valor)

        except ValueError:

            messagebox.showerror(
                "Erro",
                "Valor inválido."
            )

            return

        conexao = conectar()

        if conexao is None:
            return

        cursor = conexao.cursor()

        cursor.callproc(

            "sp_criar_sessao_e_gerar_ingressos",

            (
                f"{data} {hora}:00",
                idioma,
                self.filmes[filme],
                self.salas[sala],
                valor
            )

        )

        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo(
            "Sucesso",
            "Sessão cadastrada!"
        )

        self.limpar_campos()

        self.listar_sessoes()

    # =====================================
    # Excluir Sessão
    # =====================================

    def excluir_sessao(self):

        selecionado = self.tabela.focus()

        if selecionado == "":

            messagebox.showwarning(
                "Aviso",
                "Selecione uma sessão."
            )

            return

        if not messagebox.askyesno(
            "Excluir",
            "Deseja excluir esta sessão?"
        ):
            return

        dados = self.tabela.item(selecionado)

        sessao_id = dados["values"][0]

        conexao = conectar()

        if conexao is None:
            return

        cursor = conexao.cursor()

        cursor.callproc(
            "sp_deletar_sessao",
            (sessao_id,)
        )

        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo(
            "Sucesso",
            "Sessão excluída."
        )

        self.limpar_campos()

        self.listar_sessoes()

    # =====================================
    # Selecionar Sessão
    # =====================================

    def selecionar_sessao(self, event):

        selecionado = self.tabela.focus()

        if selecionado == "":
            return

        dados = self.tabela.item(selecionado)

        valores = dados["values"]

        if len(valores) == 0:
            return

        self.limpar_campos()

        self.comboFilme.set(valores[1])

        sala = f"{valores[2]} ({valores[3]} lugares)"

        self.comboSala.set(sala)

        data_hora = str(valores[6])

        if " " in data_hora:

            data, hora = data_hora.split(" ")

            self.entryData.insert(0, data)

            self.entryHora.insert(0, hora[:5])

        self.comboIdioma.set(valores[7])

    # =====================================
    # Limpar Campos
    # =====================================

    def limpar_campos(self):

        self.comboFilme.set("")

        self.comboSala.set("")

        self.entryData.delete(0, tk.END)

        self.entryHora.delete(0, tk.END)

        self.comboIdioma.set("")

        self.entryValor.delete(0, tk.END)