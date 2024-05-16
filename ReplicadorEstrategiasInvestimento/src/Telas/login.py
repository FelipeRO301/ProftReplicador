import tkinter as tk
from tkinter import messagebox
import psycopg2
from ReplicadorEstrategiasInvestimento.src.Telas.cadastro import CadastroApp
from teladoinvestidor import TeladoInvestidor
from teladacorretora import TeladaCorretora

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.configure(bg="orange")

        try:
            self.conn = psycopg2.connect(host="186.226.56.84", database="proft", port="5432", user="banco", password="tsc10012000@")
            self.cursor = self.conn.cursor()
        except psycopg2.Error as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
            self.root.destroy()

        self.create_widgets()

    def create_widgets(self):
        label_cpf_cnpj = tk.Label(self.root, text="CPF ou CNPJ:", bg="orange")
        label_cpf_cnpj.grid(row=0, column=0, pady=5, padx=5, sticky="e")

        label_senha = tk.Label(self.root, text="Senha:", bg="orange")
        label_senha.grid(row=1, column=0, pady=5, padx=5, sticky="e")

        self.entry_cpf_cnpj = tk.Entry(self.root, width=30)
        self.entry_cpf_cnpj.grid(row=0, column=1, pady=5, padx=5)

        self.entry_senha = tk.Entry(self.root, width=30, show="*")
        self.entry_senha.grid(row=1, column=1, pady=5, padx=5)

        self.button_login = tk.Button(self.root, text="Login", bg="yellow", command=self.login)
        self.button_login.grid(row=2, columnspan=2, pady=10)

        self.button_esqueci_senha = tk.Button(self.root, text="Esqueci a Senha", bg="yellow", command=self.esqueci_senha)
        self.button_esqueci_senha.grid(row=3, columnspan=2, pady=5)

        self.button_cadastrar = tk.Button(self.root, text="Cadastre-se", bg="yellow", command=self.abrir_cadastro)
        self.button_cadastrar.grid(row=4, columnspan=2, pady=10)

    def abrir_cadastro(self):
        self.root.withdraw()
        cadastro_window = tk.Toplevel(self.root)
        cadastro_app = CadastroApp(cadastro_window, self.voltar_login)
        cadastro_window.protocol("WM_DELETE_WINDOW", lambda: self.fechar_cadastro(cadastro_window))

    def fechar_cadastro(self, cadastro_window):
        cadastro_window.destroy()
        self.root.deiconify()

    def voltar_login(self):
        self.root.deiconify()

    def login(self):
        cpf_cnpj = self.entry_cpf_cnpj.get()
        senha = self.entry_senha.get()

        try:
            self.cursor.execute("SELECT id, nomepessoaouempresa, tipo FROM usuarios WHERE cpfoucnpj = %s AND senha = %s", (cpf_cnpj, senha))
            usuario = self.cursor.fetchone()

            if usuario:
                usuario_id, nome_usuario, tipo_usuario = usuario
                if tipo_usuario == 'pessoafísica':
                    self.abrir_tela_investidor(usuario_id, nome_usuario)
                elif tipo_usuario == 'pessoajurídica':
                    self.abrir_tela_corretora(usuario_id, nome_usuario)
            else:
                messagebox.showerror("Erro", "Credenciais inválidas.")
        except psycopg2.Error as e:
            messagebox.showerror("Erro", f"Erro ao realizar login: {e}")

    def abrir_tela_investidor(self, usuario_id, nome_usuario):
        self.root.withdraw()
        investidor_window = tk.Toplevel(self.root)

        investidor_app = TeladoInvestidor(investidor_window, usuario_id)
        investidor_window.protocol("WM_DELETE_WINDOW", self.voltar_login)

        print("ID do usuário logado:", usuario_id)
        print("Nome do usuário logado:", nome_usuario)

    def abrir_tela_corretora(self, empresa_id, nome_empresa):
        self.root.withdraw()
        corretora_window = tk.Toplevel(self.root)

        corretora_app = TeladaCorretora(corretora_window, nome_empresa)
        corretora_window.protocol("WM_DELETE_WINDOW", self.voltar_login)

        print("ID da empresa logada:", empresa_id)
        print("Nome da empresa logada:", nome_empresa)

    def esqueci_senha(self):
        messagebox.showinfo("Esqueci a Senha", "Por favor, entre em contato com o suporte para redefinir sua senha.")

root = tk.Tk()
app = LoginApp(root)
root.mainloop()




