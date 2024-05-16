import tkinter as tk
from tkinter import messagebox
from profit import dllStart

class TelaCredenciais:
    def __init__(self, root):
        self.root = root
        self.root.title("Credenciais")
        self.root.geometry("300x250")
        self.root.configure(bg="orange")

        self.create_widgets()

    def create_widgets(self):

        self.label_chave_acesso = tk.Label(self.root, text="Chave de Acesso:", bg="orange")
        self.label_chave_acesso.pack()

        self.entry_chave_acesso = tk.Entry(self.root)
        self.entry_chave_acesso.pack()

        self.label_usuario = tk.Label(self.root, text="Usuário:", bg="orange")
        self.label_usuario.pack()

        self.entry_usuario = tk.Entry(self.root)
        self.entry_usuario.pack()

        self.label_senha = tk.Label(self.root, text="Senha:", bg="orange")
        self.label_senha.pack()

        self.entry_senha = tk.Entry(self.root, show="*")
        self.entry_senha.pack()

        self.button_conectar = tk.Button(self.root, text="Conectar", bg="yellow", command=self.conectar)
        self.button_conectar.pack()

        self.label_status = tk.Label(self.root, text="", bg="orange", fg="green")
        self.label_status.pack(pady=10)

        self.button_desconectar = tk.Button(self.root, text="Desconectar", bg="yellow", command=self.desconectar)
        self.button_desconectar.pack()

    def conectar(self):
        chave_acesso = self.entry_chave_acesso.get()
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        try:
            dllStart(chave_acesso, usuario, senha)
            self.label_status.config(text="DLL conectada com sucesso!")
            messagebox.showinfo("Conexão", "DLL conectada com sucesso!")
        except Exception as e:
            self.label_status.config(text="Erro ao conectar DLL")
            messagebox.showerror("Erro", str(e))

    def desconectar(self):
             self.label_status.config(text="DLL desconectada")



