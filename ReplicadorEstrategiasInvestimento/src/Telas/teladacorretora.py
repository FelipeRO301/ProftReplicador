import tkinter as tk
from telacredenciais import TelaCredenciais

class TeladaCorretora:
    def __init__(self, root, nome_empresa=""):
        self.root = root
        self.root.title("Tela da Corretora")
        self.root.configure(bg="orange")

        self.create_widgets()
        self.mostrar_tela_inicial(nome_empresa)

    def mostrar_tela_inicial(self, nome_empresa):
        self.label_nome_empresa.config(text=nome_empresa)

    def create_widgets(self):
        self.label_bem_vindo = tk.Label(self.root, text="Bem-vindo", font=("Helvetica", 16), bg="orange")
        self.label_bem_vindo.pack(pady=20)

        self.label_nome_empresa = tk.Label(self.root, text="", font=("Helvetica", 14), bg="orange")
        self.label_nome_empresa.pack(pady=10)

        button_frame = tk.Frame(self.root, bg="orange")
        button_frame.pack()

        self.button_conectar_dll = tk.Button(button_frame, text="Conectar DLL", bg="yellow", command=self.abrir_janela_credenciais)
        self.button_conectar_dll.pack(pady=20)

        self.button_sair = tk.Button(button_frame, text="Sair", bg="yellow", command=self.sair)
        self.button_sair.pack(pady=20)

    def abrir_janela_credenciais(self):
        credenciais_window = tk.Toplevel(self.root)
        tela_credenciais = TelaCredenciais(credenciais_window)

    def sair(self):
        self.root.quit()






















