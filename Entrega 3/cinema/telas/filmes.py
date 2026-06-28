import tkinter as tk
from tkinter import ttk, messagebox

from conexao import conectar
from componentes.frame_scroll import FrameScroll

class TelaFilmes:

    def __init__(self, master):

        # ==========================
        # Cria a janela
        # ==========================

        scroll = FrameScroll(master)

        scroll.pack(
            fill="both",
            expand=True
        )

        self.frame = scroll.interior

        self.frame.configure(
            bg="#1F1F1F"
        )

        # ==========================
        # Título
        # ==========================

        titulo = tk.Label(
            self.frame,
            text="GERENCIAR FILMES",
            font=("Arial",20,"bold"),
            fg="#FFD700",
            bg="#1F1F1F"
        )

        titulo.pack(pady=15)

        # ==========================
        # Frame dos campos
        # ==========================

        frame = tk.Frame(self.frame,bg="#1F1F1F")
        frame.pack()

        # ---------- Título ----------

        tk.Label(
            frame,
            text="Título",
            fg="white",
            bg="#1F1F1F",
            width=15,
            anchor="e"
        ).grid(row=0, column=0, padx=10, pady=5)

        self.entryTitulo = tk.Entry(frame, width=35)
        self.entryTitulo.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # ---------- Duração ----------

        tk.Label(
            frame,
            text="Duração",
            fg="white",
            bg="#1F1F1F",
            width=15,
            anchor="e"
        ).grid(row=1, column=0, padx=10, pady=5)

        self.entryDuracao = tk.Entry(frame, width=10)
        self.entryDuracao.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # ---------- Categoria ----------

        tk.Label(
            frame,
            text="Categoria",
            fg="white",
            bg="#1F1F1F",
            width=15,
            anchor="e"
        ).grid(row=2, column=0, padx=10, pady=5)

        self.comboCategoria = ttk.Combobox(
            frame,
            values=[
                "Ação",
                "Aventura",
                "Animação",
                "Comédia",
                "Drama",
                "Fantasia",
                "Ficção Científica",
                "Romance",
                "Suspense",
                "Terror"
            ],
            state="readonly",
            width=15
        )

        self.comboCategoria.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # ---------- Classificação ----------

        tk.Label(
            frame,
            text="Classificação",
            fg="white",
            bg="#1F1F1F",
            width=15,
            anchor="e"
        ).grid(row=3, column=0, padx=10, pady=5)

        self.comboClassificacao = ttk.Combobox(
            frame,
            values=[
                "Livre",
                "10",
                "12",
                "14",
                "16",
                "18"
            ],
            state="readonly",
            width=15
        )

        self.comboClassificacao.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # ==========================
        # Botões
        # ==========================

        frameBotoes = tk.Frame(self.frame,bg="#1F1F1F")
        frameBotoes.pack(pady=10)

        tk.Button(
            frameBotoes,
            text="Cadastrar",
            width=15,
            command=self.cadastrar_filme
        ).grid(row=0,column=0,padx=5)

        tk.Button(
            frameBotoes,
            text="Excluir",
            width=15,
            command=self.excluir_filme
        ).grid(row=0,column=1,padx=5)

        tk.Button(
            frameBotoes,
            text="Limpar",
            width=15,
            command=self.limpar_campos
        ).grid(row=0,column=2,padx=5)

        # ==========================
        # Tabela
        # ==========================

        colunas = (
            "ID",
            "Título",
            "Duração",
            "Categoria",
            "Classificação"
        )

        self.tabela = ttk.Treeview(
            self.frame,
            columns=colunas,
            show="headings",
            height=12
        )

        for coluna in colunas:
            self.tabela.heading(coluna,text=coluna)

        self.tabela.column("ID",width=40)
        self.tabela.column("Título",width=320)
        self.tabela.column("Duração",width=100)
        self.tabela.column("Categoria",width=120)
        self.tabela.column("Classificação",width=120)

        self.tabela.pack(pady=15)

        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.selecionar_filme
        )

        self.listar_filmes()

    # =====================================

    def listar_filmes(self):

        conexao = conectar()

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                filme_id,
                titulo,
                duracao,
                categoria,
                classificacao
            FROM filme
            ORDER BY titulo
        """)

        registros = cursor.fetchall()

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for linha in registros:
            self.tabela.insert("",tk.END,values=linha)

        cursor.close()
        conexao.close()

    # =====================================

    def cadastrar_filme(self):

        titulo = self.entryTitulo.get()

        duracao = self.entryDuracao.get()

        categoria = self.comboCategoria.get()

        classificacao = self.comboClassificacao.get()

        if titulo == "" or duracao == "" or classificacao == "" or categoria == "":

            messagebox.showwarning(
                "Aviso",
                "Preencha todos os campos."
            )

            return

        conexao = conectar()

        cursor = conexao.cursor()

        cursor.callproc(
            "sp_cadastrar_filme",
            (
                titulo,
                int(duracao),
                categoria,
                classificacao
            )
        )

        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo(
            "Sucesso",
            "Filme cadastrado!"
        )

        self.limpar_campos()

        self.listar_filmes()

    # =====================================

    def excluir_filme(self):

        selecionado = self.tabela.focus()

        if selecionado == "":

            messagebox.showwarning(
                "Aviso",
                "Selecione um filme."
            )

            return

        resposta = messagebox.askyesno(
            "Excluir",
            "Deseja realmente excluir?"
        )

        if not resposta:
            return

        dados = self.tabela.item(selecionado)

        filme_id = dados["values"][0]

        conexao = conectar()

        cursor = conexao.cursor()

        cursor.callproc(
            "sp_deletar_filme",
            (filme_id,)
        )

        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo(
            "Sucesso",
            "Filme excluído."
        )

        self.listar_filmes()

    # =====================================

    def selecionar_filme(self,event):

        selecionado = self.tabela.focus()

        dados = self.tabela.item(selecionado)

        valores = dados["values"]

        if len(valores)==0:
            return

        self.limpar_campos()

        self.entryTitulo.insert(0,valores[1])

        self.entryDuracao.insert(0,valores[2])

        self.comboCategoria.insert(valores[3])

        self.comboClassificacao.set(valores[4])

    # =====================================

    def limpar_campos(self):

        self.entryTitulo.delete(0,tk.END)

        self.entryDuracao.delete(0,tk.END)

        self.comboCategoria.set("")

        self.comboClassificacao.set("")