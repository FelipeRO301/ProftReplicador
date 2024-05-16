import tkinter as tk
from tkinter import messagebox
import psycopg2

class TeladoInvestidor:
    def __init__(self, root, usuario_id):
        self.root = root
        self.root.title("Tela do Investidor")
        self.root.configure(bg="orange")
        self.usuario_id = usuario_id

        print("ID do usuário logado:", self.usuario_id)

        try:
            self.conn = psycopg2.connect(host="186.226.56.84", database="proft", port="5432", user="banco", password="tsc10012000@")
            self.cursor = self.conn.cursor()
        except psycopg2.Error as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
            self.root.destroy()

        self.create_widgets()
        self.carregar_empresas()

    def create_widgets(self):
        label_empresas = tk.Label(self.root, text="Empresas Disponíveis:", bg="orange")
        label_empresas.grid(row=0, column=0, pady=5, padx=5, sticky="w")

        self.listbox_empresas = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.listbox_empresas.grid(row=1, column=0, pady=5, padx=5, sticky="w")

        self.button_associar = tk.Button(self.root, text="Associar", bg="yellow", command=self.associar_empresas)
        self.button_associar.grid(row=2, column=0, pady=5, padx=5)

        self.button_sair = tk.Button(self.root, text="Sair", bg="yellow", command=self.sair)
        self.button_sair.grid(row=3, column=0, pady=5, padx=5)

    def carregar_empresas(self):
        try:
            self.cursor.execute("SELECT id, nomepessoaouempresa FROM usuarios WHERE tipo = 'pessoajurídica'")
            empresas = self.cursor.fetchall()
            for id_empresa, nome_empresa in empresas:
                self.listbox_empresas.insert(tk.END, f"{id_empresa} - {nome_empresa}")
        except psycopg2.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar empresas: {e}")

    def associar_empresas(self):
        empresas_selecionadas = self.listbox_empresas.curselection()
        if not empresas_selecionadas:
            messagebox.showerror("Erro", "Selecione pelo menos uma empresa para associar.")
            return

        for index in empresas_selecionadas:
            id_empresa = int(self.listbox_empresas.get(index).split(" - ")[0])
            print("ID da empresa selecionada:", id_empresa)

            try:

                self.cursor.execute("SELECT COUNT(*) FROM usuarios WHERE id = %s AND tipo = 'pessoafísica'", (self.usuario_id,))
                count_usuario = self.cursor.fetchone()[0]
                if count_usuario == 0:
                    messagebox.showerror("Erro", "Apenas usuários do tipo 'pessoafísica' podem associar-se a empresas.")
                    continue

                self.cursor.execute("SELECT COUNT(*) FROM usuarios WHERE id = %s AND tipo = 'pessoajurídica'", (id_empresa,))
                count_empresa = self.cursor.fetchone()[0]
                if count_empresa == 0:
                    messagebox.showerror("Erro", f"ID de empresa inválido: {id_empresa}")
                    continue

                self.cursor.execute("SELECT COUNT(*) FROM associacoes WHERE usuario_pf_id = %s AND usuario_pj_id = %s", (self.usuario_id, id_empresa))
                count_associacao = self.cursor.fetchone()[0]
                if count_associacao == 0:
                    self.cursor.execute("INSERT INTO associacoes (usuario_pf_id, usuario_pj_id) VALUES (%s, %s)", (self.usuario_id, id_empresa))
                    self.conn.commit()
                else:
                    messagebox.showinfo("Aviso", "Esta empresa já está associada.")
            except psycopg2.Error as e:
                messagebox.showerror("Erro", f"Erro ao associar empresa: {e}")

        messagebox.showinfo("Sucesso", "Empresas associadas com sucesso.")

    def sair(self):
        self.root.destroy()

















