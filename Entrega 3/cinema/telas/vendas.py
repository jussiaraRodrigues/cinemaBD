import tkinter as tk
from tkinter import ttk, messagebox

from conexao import conectar
from componentes.frame_scroll import FrameScroll


class TelaVendas:

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

        # ============================
        # Variáveis
        # ============================

        self.sessoes = {}

        self.botoes = {}

        self.assentosSelecionados = []

        self.valorIngresso = 0

        # ============================
        # Título
        # ============================

        titulo = tk.Label(
            self.frame,
            text="VENDA DE INGRESSOS",
            font=("Arial",20,"bold"),
            fg="#FFD700",
            bg="#1F1F1F"
        )

        titulo.pack(pady=10)

        # ============================
        # Escolha da sessão
        # ============================

        frameSessao = tk.Frame(
            self.frame,
            bg="#1F1F1F"
        )

        frameSessao.pack(pady=10)

        tk.Label(
            frameSessao,
            text="Sessão",
            bg="#1F1F1F",
            fg="white",
            font=("Arial",11,"bold")
        ).grid(row=0,column=0,padx=5)

        self.comboSessao = ttk.Combobox(
            frameSessao,
            width=65,
            state="readonly"
        )

        self.comboSessao.grid(
            row=0,
            column=1,
            padx=10
        )

        self.comboSessao.bind(
            "<<ComboboxSelected>>",
            self.carregar_assentos
        )

        # ============================
        # Tela
        # ============================

        tela = tk.Label(

            self.frame,

            text="TELA",

            bg="#DDDDDD",

            fg="black",

            width=55,

            font=("Arial",12,"bold")

        )

        tela.pack(pady=10)

        # ============================
        # Frame dos assentos
        # ============================

        self.frameMapa = tk.Frame(

            self.frame,

            bg="#1F1F1F"

        )

        self.frameMapa.pack()

        # ============================
        # Informações da compra
        # ============================

        frameCompra = tk.Frame(

            self.frame,

            bg="#1F1F1F"

        )

        frameCompra.pack(pady=20)

        tk.Label(

            frameCompra,

            text="Assentos:",

            fg="white",

            bg="#1F1F1F",

            font=("Arial",11,"bold")

        ).grid(row=0,column=0)

        self.lblAssentos = tk.Label(

            frameCompra,

            text="Nenhum",

            fg="#FFD700",

            bg="#1F1F1F",

            width=30,

            anchor="w"

        )

        self.lblAssentos.grid(
            row=0,
            column=1,
            padx=10
        )

        tk.Label(

            frameCompra,

            text="Quantidade:",

            fg="white",

            bg="#1F1F1F",

            font=("Arial",11,"bold")

        ).grid(row=1,column=0)

        self.lblQuantidade = tk.Label(

            frameCompra,

            text="0",

            fg="#FFD700",

            bg="#1F1F1F"

        )

        self.lblQuantidade.grid(
            row=1,
            column=1,
            sticky="w",
            padx=10
        )

        tk.Label(

            frameCompra,

            text="Valor Total:",

            fg="white",

            bg="#1F1F1F",

            font=("Arial",11,"bold")

        ).grid(row=2,column=0)

        self.lblValor = tk.Label(

            frameCompra,

            text="R$ 0,00",

            fg="#00FF66",

            bg="#1F1F1F"

        )

        self.lblValor.grid(
            row=2,
            column=1,
            sticky="w",
            padx=10
        )

        # ============================
        # Botão
        # ============================

        tk.Button(

            self.frame,

            text="Finalizar Venda",

            width=25,

            command=self.finalizar_venda

        ).pack(pady=10)

        # ============================
        # Legenda
        # ============================

        legenda = tk.Frame(
            self.frame,
            bg="#1F1F1F"
        )

        legenda.pack(pady=5)

        # Livre
        tk.Label(
            legenda,
            bg="green",
            width=2,
            height=1
        ).pack(side="left", padx=(10,2))

        tk.Label(
            legenda,
            text="Livre",
            bg="#1F1F1F",
            fg="white"
        ).pack(side="left", padx=(0,15))

        # Selecionado
        tk.Label(
            legenda,
            bg="blue",
            width=2,
            height=1
        ).pack(side="left", padx=(10,2))

        tk.Label(
            legenda,
            text="Selecionado",
            bg="#1F1F1F",
            fg="white"
        ).pack(side="left", padx=(0,15))

        # Ocupado
        tk.Label(
            legenda,
            bg="red",
            width=2,
            height=1
        ).pack(side="left", padx=(10,2))

        tk.Label(
            legenda,
            text="Ocupado",
            bg="#1F1F1F",
            fg="white"
        ).pack(side="left", padx=(0,15))
        # ============================

        self.carregar_sessoes()
    
    # ==========================================
    # Carregar Sessões
    # ==========================================

    def carregar_sessoes(self):

        conexao = conectar()

        if conexao is None:
            return

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                sessao_id,
                filme,
                data_hora,
                vagas_disponiveis
            FROM vw_sessoes_e_vagas
            ORDER BY data_hora
        """)

        self.sessoes.clear()

        lista = []

        for sessao_id, filme, data_hora, vagas in cursor.fetchall():

            texto = f"{filme} | {data_hora} | Vagas: {vagas}"

            self.sessoes[texto] = sessao_id

            lista.append(texto)

        self.comboSessao["values"] = lista

        cursor.close()
        conexao.close()

    # ==========================================
    # Carregar Assentos
    # ==========================================

    def carregar_assentos(self, event=None):

        for widget in self.frameMapa.winfo_children():
            widget.destroy()

        self.botoes.clear()

        self.assentosSelecionados.clear()

        self.lblAssentos.config(text="Nenhum")
        self.lblQuantidade.config(text="0")
        self.lblValor.config(text="R$ 0,00")

        sessao = self.comboSessao.get()

        if sessao == "":
            return

        sessao_id = self.sessoes[sessao]

        conexao = conectar()

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                ingresso_id,
                fila,
                numero,
                situacao,
                valor
            FROM vw_mapa_assentos_sessao
            WHERE sessao_id=%s
            ORDER BY fila,numero
        """, (sessao_id,))

        assentos = cursor.fetchall()
        print(assentos)

        cursor.close()
        conexao.close()

        # Cabeçalho das colunas

        tk.Label(
            self.frameMapa,
            text="",
            bg="#1F1F1F",
            width=3
        ).grid(row=0,column=0)

        numeros = sorted(set(a[2] for a in assentos))

        for coluna, numero in enumerate(numeros, start=1):

            tk.Label(
                self.frameMapa,
                text=numero,
                fg="white",
                bg="#1F1F1F",
                width=4
            ).grid(row=0,column=coluna)

        # Letras das filas

        filas = sorted(set(a[1] for a in assentos))

        for fila in filas:

            linha = ord(fila)-64

            tk.Label(
                self.frameMapa,
                text=fila,
                fg="white",
                bg="#1F1F1F",
                width=3
            ).grid(row=linha,column=0)

        # Botões

        for ingresso_id, fila, numero, situacao, valor in assentos:

            linha = ord(fila)-64
            coluna = numero

            if situacao == "Livre":

                cor = "green"

                estado = "normal"

            else:

                cor = "red"

                estado = "disabled"

            botao = tk.Button(

                self.frameMapa,

                text=f"{fila}{numero}",

                bg=cor,

                fg="white",

                width=4,

                state=estado,

                command=lambda i=ingresso_id,
                               a=f"{fila}{numero}",
                               v=valor:
                    self.selecionar_assento(
                        i,
                        a,
                        v
                    )

            )

            botao.grid(
                row=linha,
                column=coluna,
                padx=2,
                pady=2
            )

            self.botoes[ingresso_id] = botao

    # ==========================================
    # Selecionar Assento
    # ==========================================

    def selecionar_assento(
        self,
        ingresso_id,
        assento,
        valor
    ):

        botao = self.botoes[ingresso_id]

        # Remove se já estiver selecionado

        for item in self.assentosSelecionados:

            if item["id"] == ingresso_id:

                self.assentosSelecionados.remove(item)

                botao.config(bg="green")

                self.atualizar_compra()

                return

        # Adiciona na compra

        self.assentosSelecionados.append({

            "id": ingresso_id,

            "assento": assento,

            "valor": valor

        })

        botao.config(bg="blue")

        self.atualizar_compra()

    # ==========================================
    # Atualizar Informações
    # ==========================================

    def atualizar_compra(self):

        if len(self.assentosSelecionados) == 0:

            self.lblAssentos.config(text="Nenhum")

            self.lblQuantidade.config(text="0")

            self.lblValor.config(text="R$ 0,00")

            return

        nomes = []

        total = 0

        for item in self.assentosSelecionados:

            nomes.append(item["assento"])

            total += float(item["valor"])

        self.lblAssentos.config(

            text=", ".join(nomes)

        )

        self.lblQuantidade.config(

            text=str(len(self.assentosSelecionados))

        )

        self.lblValor.config(

            text=f"R$ {total:.2f}"

        )
    
    # ==========================================
    # Finalizar Venda
    # ==========================================

    def finalizar_venda(self):

        if len(self.assentosSelecionados) == 0:
            messagebox.showwarning(
                "Aviso",
                "Selecione pelo menos um assento."
            )
            return

        total = sum(float(item["valor"]) for item in self.assentosSelecionados)

        resposta = messagebox.askyesno(
            "Confirmar Venda",
            f"Quantidade de ingressos: {len(self.assentosSelecionados)}\n\n"
            f"Valor Total: R$ {total:.2f}\n\n"
            f"Deseja concluir a venda?"
        )

        if not resposta:
            return

        conexao = conectar()

        if conexao is None:
            return

        cursor = conexao.cursor()

        # -----------------------------------------------------------------
        # INÍCIO DA PROTEÇÃO CONTRA ERROS / TRIGGER
        # -----------------------------------------------------------------
        try:

            cursor.execute("""
                INSERT INTO venda
                (
                    data_venda,
                    valor_total
                )
                VALUES
                (
                    NOW(),
                    %s
                )
            """, (total,))

            venda_id = cursor.lastrowid

            for item in self.assentosSelecionados:
                cursor.execute("""
                    UPDATE ingresso
                    SET venda_id=%s
                    WHERE ingresso_id=%s
                """, (venda_id, item["id"]))

            conexao.commit()

            messagebox.showinfo(
                "Sucesso",
                "Venda realizada com sucesso!"
            )

        except Exception as erro:
            conexao.rollback()

            messagebox.showerror(
                "Venda Bloqueada",
                f"Não foi possível concluir a venda:\n{erro}"
            )

        finally:
            cursor.close()
            conexao.close()

        self.carregar_assentos()

        self.carregar_sessoes()