import tkinter as tk
from tkinter import messagebox
import re
import psycopg2

class CadastroApp:
    def __init__(self, root, voltar_callback):
        self.root = root
        self.root.title("Cadastro de Usuário")
        self.root.configure(bg="orange")
        self.voltar_callback = voltar_callback

        try:
            self.conn = psycopg2.connect(host="186.226.56.84", database="proft", port="5432", user="banco", password="tsc10012000@")
            self.cursor = self.conn.cursor()
        except psycopg2.Error as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
            self.root.destroy()

        self.create_widgets()

    def create_widgets(self):
        # Labels
        label_nome = tk.Label(self.root, text="Nome Pessoa ou Empresa:", bg="orange")
        label_nome.grid(row=0, column=0, pady=5, padx=5, sticky="e")

        label_cpf_cnpj = tk.Label(self.root, text="CPF ou CNPJ:", bg="orange")
        label_cpf_cnpj.grid(row=1, column=0, pady=5, padx=5, sticky="e")

        label_tipo = tk.Label(self.root, text="Tipo:", bg="orange")
        label_tipo.grid(row=2, column=0, pady=5, padx=5, sticky="e")

        label_telefone = tk.Label(self.root, text="Telefone:", bg="orange")
        label_telefone.grid(row=3, column=0, pady=5, padx=5, sticky="e")

        label_email = tk.Label(self.root, text="Email:", bg="orange")
        label_email.grid(row=4, column=0, pady=5, padx=5, sticky="e")

        label_conf_email = tk.Label(self.root, text="Confirmar Email:", bg="orange")
        label_conf_email.grid(row=5, column=0, pady=5, padx=5, sticky="e")

        label_senha = tk.Label(self.root, text="Senha:", bg="orange")
        label_senha.grid(row=6, column=0, pady=5, padx=5, sticky="e")

        label_conf_senha = tk.Label(self.root, text="Confirmar Senha:", bg="orange")
        label_conf_senha.grid(row=7, column=0, pady=5, padx=5, sticky="e")

        self.entry_nome = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.entry_nome.grid(row=0, column=1, pady=5, padx=5)

        self.entry_cpf_cnpj = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.entry_cpf_cnpj.grid(row=1, column=1, pady=5, padx=5)

        self.var_tipo = tk.StringVar()
        self.var_tipo.set(None)

        self.radio_pf = tk.Radiobutton(self.root, text="Pessoa Física", variable=self.var_tipo, value="pessoafísica", bg="orange", font=("Arial", 12))
        self.radio_pf.grid(row=2, column=1, sticky="w")
        self.radio_pj = tk.Radiobutton(self.root, text="Pessoa Jurídica", variable=self.var_tipo, value="pessoajurídica", bg="orange", font=("Arial", 12))
        self.radio_pj.grid(row=2, column=2, sticky="e")

        self.entry_telefone = tk.Entry(self.root)
        self.entry_telefone.grid(row=3, column=1, pady=5, padx=5)

        self.entry_email = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.entry_email.grid(row=4, column=1, pady=5, padx=5)

        self.entry_conf_email = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.entry_conf_email.grid(row=5, column=1, pady=5, padx=5)

        self.entry_senha = tk.Entry(self.root, width=30, font=("Arial", 12), show="*")
        self.entry_senha.grid(row=6, column=1, pady=5, padx=5)

        self.entry_conf_senha = tk.Entry(self.root, width=30, font=("Arial", 12), show="*")
        self.entry_conf_senha.grid(row=7, column=1, pady=5, padx=5)

        self.button_cadastrar = tk.Button(self.root, text="Cadastrar", bg="yellow", command=self.cadastrar, font=("Arial", 12))
        self.button_cadastrar.grid(row=8, columnspan=2, pady=10)

        self.button_voltar = tk.Button(self.root, text="Voltar para o Login", bg="yellow", command=self.voltar_login)
        self.button_voltar.grid(row=9, columnspan=2, pady=10)

    def voltar_login(self):
        self.root.withdraw()
        self.voltar_callback()

    def cadastrar(self):
        nome = self.entry_nome.get()
        cpf_cnpj = self.entry_cpf_cnpj.get()
        tipo = self.var_tipo.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        conf_email = self.entry_conf_email.get()
        senha = self.entry_senha.get()
        conf_senha = self.entry_conf_senha.get()

        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', senha):
            messagebox.showerror("Erro",
                                 "A senha deve conter pelo menos 8 caracteres, incluindo pelo menos uma letra, um número e um caractere especial.")
            return

        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório.")
            return

        if not cpf_cnpj:
            messagebox.showerror("Erro", "CPF ou CNPJ é obrigatório.")
            return

        if tipo == 'pessoafísica':
            if not re.match(r'^\d{11}$', cpf_cnpj):
                messagebox.showerror("Erro", "CPF inválido.")
                return
        elif tipo == 'pessoajurídica':
            if not re.match(r'^\d{14}$', cpf_cnpj):
                messagebox.showerror("Erro", "CNPJ inválido.")
                return

        if not email or not conf_email or email != conf_email:
            messagebox.showerror("Erro", "Emails não coincidem ou são inválidos.")
            return

        if not senha or not conf_senha or senha != conf_senha:
            messagebox.showerror("Erro", "Senhas não coincidem ou são inválidas.")
            return

        try:
            self.cursor.execute("INSERT INTO usuarios (nomepessoaouempresa, cpfoucnpj, tipo, email, confirmaemail, senha, confirmasenha,telefone) VALUES (%s, %s, %s, %s, %s, %s, %s ,%s)",
                                (nome, cpf_cnpj, tipo, email, conf_email, senha, conf_senha,telefone))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso.")
        except psycopg2.Error as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

root = tk.Tk()
app = CadastroApp(root, lambda: root.deiconify())
root.mainloop()

