import tkinter as tk

from telas.filmes import TelaFilmes
from telas.salas import TelaSalas
from telas.sessoes import TelaSessoes
from telas.vendas import TelaVendas
from telas.historicos import TelaHistoricos

# ==================================
# Funções
# ==================================

def limpar_frame():
    """Remove tudo que estiver no frame principal."""
    for widget in frame_principal.winfo_children():
        widget.destroy()


def abrir_filmes():
    limpar_frame()
    TelaFilmes(frame_principal)


def abrir_salas():
    limpar_frame()
    TelaSalas(frame_principal)


def abrir_sessoes():
    limpar_frame()
    TelaSessoes(frame_principal)


def abrir_vendas():
    limpar_frame()
    TelaVendas(frame_principal)


def abrir_historico():
    limpar_frame()
    TelaHistoricos(frame_principal)

# ==================================
# Janela Principal
# ==================================

janela = tk.Tk()

janela.title("Cine Pajeú")
janela.geometry("1100x800")
janela.configure(bg="#1F1F1F")
janela.resizable(False, False)

# ==================================
# Cabeçalho
# ==================================

titulo = tk.Label(
    janela,
    text="🎬 CINE PAJEÚ",
    font=("Arial", 24, "bold"),
    fg="#FFD700",
    bg="#1F1F1F"
)

titulo.pack(pady=(20, 5))

subtitulo = tk.Label(
    janela,
    text="Sistema de Gerenciamento",
    font=("Arial", 12),
    fg="white",
    bg="#1F1F1F"
)

subtitulo.pack(pady=(0, 15))

# ==================================
# Menu
# ==================================

menu = tk.Frame(janela, bg="#1F1F1F")
menu.pack()

cor_botao = "#B22222"

tk.Button(
    menu,
    text="Filmes",
    width=20,
    bg=cor_botao,
    fg="white",
    command=abrir_filmes
).grid(row=0, column=0, padx=5)

tk.Button(
    menu,
    text="Salas",
    width=20,
    bg=cor_botao,
    fg="white",
    command=abrir_salas
).grid(row=0, column=1, padx=5)

tk.Button(
    menu,
    text="Sessões",
    width=20,
    bg=cor_botao,
    fg="white",
    command=abrir_sessoes
).grid(row=0, column=2, padx=5)

tk.Button(
    menu,
    text="Vendas",
    width=20,
    bg=cor_botao,
    fg="white",
    command=abrir_vendas
).grid(row=0, column=3, padx=5)

tk.Button(
    menu,
    text="Históricos",
    width=20,
    bg=cor_botao,
    fg="white",
    command=abrir_historico
).grid(row=0, column=4, padx=5)

tk.Button(
    menu,
    text="Sair",
    width=10,
    bg="#555555",
    fg="white",
    command=janela.destroy
).grid(row=0, column=5, padx=5)

# ==================================
# Área onde as telas serão exibidas
# ==================================

frame_principal = tk.Frame(
    janela,
    bg="#1F1F1F"
)

frame_principal.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=15
)

# Tela inicial

tk.Label(
    frame_principal,
    text="Bem-vindo ao Sistema Cine Pajeú",
    font=("Arial", 18),
    bg="#1F1F1F",
    fg="white"
).pack(pady=80)

# ==================================
# Executar
# ==================================

janela.mainloop()