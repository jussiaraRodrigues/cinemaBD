import tkinter as tk
from tkinter import ttk, messagebox

from conexao import conectar
from componentes.frame_scroll import FrameScroll


class TelaHistoricos:

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

        self.vendaSelecionada = None

        # ===========================
        # Título
        # ===========================

        titulo = tk.Label(

            self.frame,

            text="HISTÓRICO DE VENDAS",

            font=("Arial",20,"bold"),

            fg="#FFD700",

            bg="#1F1F1F"

        )

        titulo.pack(pady=15)

        # ===========================
        # Pesquisa
        # ===========================

        framePesquisa = tk.Frame(

            self.frame,

            bg="#1F1F1F"

        )

        framePesquisa.pack(pady=10)

        tk.Label(

            framePesquisa,

            text="Filme",

            fg="white",

            bg="#1F1F1F"

        ).grid(row=0,column=0,padx=5)

        self.entryPesquisa = tk.Entry(

            framePesquisa,

            width=35

        )

        self.entryPesquisa.grid(
            row=0,
            column=1,
            padx=10
        )

        tk.Button(

            framePesquisa,

            text="Pesquisar",

            width=15,

            command=self.pesquisar

        ).grid(
            row=0,
            column=2,
            padx=5
        )

        tk.Button(

            framePesquisa,

            text="Atualizar",

            width=15,

            command=self.listar_historico

        ).grid(
            row=0,
            column=3,
            padx=5
        )

        # ===========================
        # Tabela
        # ===========================

        colunas=(
            "Venda",
            "Filme",
            "Sessão",
            "Sala",
            "Assento",
            "Valor",
            "Data Venda"
        )

        self.tabela = ttk.Treeview(

            self.frame,

            columns=colunas,

            show="headings",

            height=14

        )

        for coluna in colunas:

            self.tabela.heading(
                coluna,
                text=coluna
            )

        self.tabela.column(
            "Venda",
            width=60
        )

        self.tabela.column(
            "Filme",
            width=230
        )

        self.tabela.column(
            "Sessão",
            width=150
        )

        self.tabela.column(
            "Sala",
            width=100
        )

        self.tabela.column(
            "Assento",
            width=80
        )

        self.tabela.column(
            "Valor",
            width=90
        )

        self.tabela.column(
            "Data Venda",
            width=90
        )

        self.tabela.pack(
            pady=15,
            fill="x"
        )

        self.tabela.bind(

            "<<TreeviewSelect>>",

            self.selecionar_venda

        )

        # ===========================
        # Informações
        # ===========================

        frameInfo = tk.Frame(

            self.frame,

            bg="#1F1F1F"

        )

        frameInfo.pack(pady=10)

        tk.Label(

            frameInfo,

            text="Venda Selecionada:",

            fg="white",

            bg="#1F1F1F",

            font=("Arial",11,"bold")

        ).pack(side="left")

        self.lblVenda = tk.Label(

            frameInfo,

            text="Nenhuma",

            fg="#FFD700",

            bg="#1F1F1F"

        )

        self.lblVenda.pack(
            side="left",
            padx=10
        )

        # ===========================
        # Botão
        # ===========================

        tk.Button(

            self.frame,

            text="Cancelar Venda",

            width=20,

            command=self.cancelar_venda

        ).pack(pady=15)

        self.listar_historico()
    
    # =====================================
    # Listar Histórico
    # =====================================

    def listar_historico(self):

        conexao = conectar()

        if conexao is None:
            return

        cursor = conexao.cursor()

        cursor.execute("""

            SELECT
                venda_id,
                filme,
                data_hora_sessao,
                sala,
                CONCAT(fila, numero_assento) AS assento,
                valor_ingresso,
                data_venda
            FROM vw_historico_vendas
            ORDER BY data_venda DESC

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

        self.vendaSelecionada = None

        self.lblVenda.config(text="Nenhuma")

    # =====================================
    # Pesquisar
    # =====================================

    def pesquisar(self):

        filme = self.entryPesquisa.get()

        conexao = conectar()

        if conexao is None:
            return

        cursor = conexao.cursor()

        cursor.execute("""

            SELECT
                venda_id,
                filme,
                data_hora_sessao,
                sala,
                CONCAT(fila, numero_assento),
                valor_ingresso,
                data_venda
            FROM vw_historico_vendas
            WHERE filme LIKE %s
            ORDER BY data_venda DESC

        """,("%"+filme+"%",))

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
    # Selecionar Venda
    # =====================================

    def selecionar_venda(self, event):

        selecionado = self.tabela.focus()

        if selecionado == "":
            return

        dados = self.tabela.item(selecionado)

        valores = dados["values"]

        if len(valores) == 0:
            return

        self.vendaSelecionada = valores[0]

        self.lblVenda.config(

            text=f"Venda Nº {self.vendaSelecionada}"

        )

    # =====================================
    # Cancelar Venda
    # =====================================

    def cancelar_venda(self):

        if self.vendaSelecionada is None:

            messagebox.showwarning(

                "Aviso",

                "Selecione uma venda."

            )

            return

        resposta = messagebox.askyesno(

            "Cancelar Venda",

            f"Deseja cancelar a venda Nº {self.vendaSelecionada} ?"

        )

        if not resposta:
            return

        conexao = conectar()

        if conexao is None:
            return

        cursor = conexao.cursor()

        cursor.callproc(

            "sp_cancelar_venda",

            (self.vendaSelecionada,)

        )

        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo(

            "Sucesso",

            "Venda cancelada com sucesso."

        )

        self.entryPesquisa.delete(0, tk.END)

        self.listar_historico()
    
    