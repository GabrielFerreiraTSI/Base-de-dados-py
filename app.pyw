import tkinter as tk
from tkinter import ttk
import re
import mysql.connector

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema")

        self.varResultado = tk.StringVar(self)
        self.labelResultado = ttk.Label(self, textvariable=self.varResultado, font=("Arial", 18, "bold"))
        self.labelResultado.grid(column=0, row=0, columnspan=3, padx=20, pady=10, sticky="ewns")
        
        
        self.labelNome = ttk.Label(self, text="Nome", font=("Arial", 18))
        self.labelNome.grid(column=0, row=1, sticky="w", padx=20, pady=5)
        
        self.varNome = tk.StringVar(self)
        self.entryNome = ttk.Entry(self, textvariable=self.varNome, font=("Arial", 18)) 
        self.entryNome.grid(column=1, row=1, sticky="we", padx=20, pady=5)
        
        
        self.labelEmail = ttk.Label(self, text="Email", font=("Arial", 18))
        self.labelEmail.grid(column=0, row=2, sticky="w", padx=20, pady=5)
        
        self.varEmail = tk.StringVar(self)
        self.entryEmail = ttk.Entry(self, textvariable=self.varEmail, font=("Arial", 18)) 
        self.entryEmail.grid(column=1, row=2, sticky="we", padx=20, pady=5)
        
        
        self.frameLista = ttk.Label(self)
        self.frameLista.grid(row=3, column=0, columnspan=2, rowspan=4, sticky="nwes", padx=20, pady=10)
        
        self.txtLista = ttk.Treeview(self.frameLista, columns=("nome", "email"), show="headings", height=7)
        self.txtLista.heading("nome", text="Nome")
        self.txtLista.heading("email", text="Email")
        
        def selectItem(event):
            for selectedItem in self.txtLista.selection():
                item = self.txtLista.item(selectedItem)
                record = item["values"]
                self.varNome.set(record[0])
                self.varEmail.set(record[1])
                
        self.txtLista.bind("<<TreeviewSelect>>", selectItem)
        self.txtLista.grid(column=0, row=0, sticky="nwes")
        
        scrollbar = tk.Scrollbar(self.frameLista, orient=tk.VERTICAL, command=self.txtLista.yview)
        self.txtLista.configure(yscroll=scrollbar.set)
        scrollbar.grid(column=1, row=0, sticky="ns")
        
        
        self.buttonConectar = ttk.Button(self, text="Conectar", command=self.conectar)
        self.buttonConectar.grid(column=2, row=1, sticky="nwes", padx=20, pady=5, ipadx=20)
        
        self.buttonCriarTabela = ttk.Button(self, text="Criar Tabela", command=self.criarTabela)
        self.buttonCriarTabela.grid(column=2, row=2, sticky="nwes", padx=20, pady=5, ipadx=20)
        
        self.buttonInserir = ttk.Button(self, text="Inserir", command=self.inserirValores)
        self.buttonInserir.grid(column=2, row=3, sticky="nwes", padx=20, pady=5, ipadx=20)
        
        self.buttonConsultar = ttk.Button(self, text="Consultar", command=self.consultar)
        self.buttonInserir.grid(column=2, row=4, sticky="nwes", padx=20, pady=5, ipadx=20)
        
        self.buttonExcluir = ttk.Button(self, text="Excluir", command=self.excluir)
        self.buttonExcluir.grid(column=2, row=5, sticky="nwes", padx=20, pady=5, ipadx=20)
        
        self.buttonEditar = ttk.Button(self, text="Editar", command=self.editar)
        self.buttonEditar.grid(column=2, row=6, sticky="nwes", padx=20, pady=5, ipadx=20)
        
    def conectar(self):
        try:
            conexao = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "")
            
            mycursor = conexao.cursor()
            query = "CREATE DATABASE IF NOT EXISTS base_de_dados;"
            mycursor.execute(query)
            self.varResultado.set("Conectado com sucesso!")
            self.labelResultado.configure(background="#99FF99")
        except:
            self.varResultado.set("Não foi possível se conectar.")
            self.labelResultado.configure(background="#FF9999")
            
    def criarTabela(self):
        try:
            conexao = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "base_de_dados")
            
            mycursor = conexao.cursor()
            query = """CREATE TABLE IF NOT EXISTS pessoas(
                nome VARCHAR(50),
                email VARRCHAR(50),
                PRIMARY KEY(email));"""
            mycursor.execute(query)
            self.varResultado.set("Tabela criada com sucesso!")
            self.labelResultado.configure(background="#99FF99")
        except:
            self.varResultado.set("Não foi possível criar a tabela.")
            self.labelResultado.configure(background="#FF9999")
            
    def inserirValores(self):
        nome = self.varNome.get().strip()
        email = self.varEmail.get().strip()
        
        reNome = re.fullmatch(r"\b[A-Za-z ]+\b", nome)
        reEmail = re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email)
        
        if reNome == None:
            self.varResultado.set("O campo é obrigatório.")
            self.labelResultado.configure(background="#FF9999")
            self.entryNome.focus()
        elif reEmail == None:
            self.varResultado.set("Digite um email váliido.")
            self.labelResultado.configure(background="#FF9999")
            self.entryEmail.focus()
        else:
            try:
                conexao = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "base_de_dados")
                
                mycursor = conexao.cursor()
                query = "INSERT INTO pessoas(nome, email) VALUES (%s, %s);"
                valores = (nome, email)
                mycursor.execute(query, valores)
                conexao.commit()
                
                self.varResultado.set(str(mycursor.rowcount) + " cadastro(s) concluído(s).")
                self.labelResultado.configure(background="#99FF99")
                
                self.varNome.set("")
                self.varEmail.set("")
                
                self.entryNome.focus()
                self.consultar()
            except:
                self.varResultado.set("Não foi possível cadastrar as informações.")
                self.labelResultado.configure(background="#FF9999")
                
    def consultar(self):
        self.txtLista.delete(*self.txtLista.get_children())
        
        try:
            conexao = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "base_de_dados")
            
            mycursor = conexao.cursor()
            query = "SELECT * FROM pessoas ORDER BY nome ASC;"
            if self.varNome.get() != "":
                query = "SELECT * FROM pessoas WHERE nome LIKE %s;"
                valores = (self.varNome.get(),)
                mycursor.execute(query, valores)
            elif self.varEmail.get() != "":
                query = "SELECT * FROM pessoas WHERE email LIKE %s;"
                valores = (self.varEmail.get(),)
                mycursor.execute(query, valores)
            else:
                mycursor.execute(query)
            myresult = mycursor.fetchall()
            
            for contato in myresult:
                self.txtLista.insert("", tk.END, values=contato)
                
            self.varResultado.set("")
            self.labelResultado.configure(background="#99FF99")
            self.entryNome.focus()
        except:
            self.varResultado.set("Não foi possível consultar as informações.")
            self.labelResultado.configure(background="#FF9999")
            
    def excluir(self):
        nome = self.varNome.get().strip()
        email = self.varEmail.get().strip()
       
        if nome == "" or email == "":
            self.varResultado.set("Escolha um registro para excluir.")
            self.labelResultado.configure(background="#FF9999")
            self.entryNome.focus()
        else:
            try:
                conexao = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "base_de_dados")
                
                mycursor = conexao.cursor()
                query = "DELETE * FROM pessoas WHERE nome = %s AND email = %s);"
                valores = (nome, email)
                mycursor.execute(query, valores)
                conexao.commit()
                
                self.varNome.set("")
                self.varEmail.set("")
                
                self.consultar()
                
                if mycursor.rowcount > 0:
                    self.varResultado.set("Registro excluido com sucesso.")
                    self.labelResultado.configure(background="#99FF99")
                    self.entryNome.focus()
                else:
                    self.varResultado.set("Registro não excluido.")
                    self.labelResultado.configure(background="#99FF99")
                    self.entryNome.focus()
            except:
                self.varResultado.set("Não foi possível excluir o registro.")
                self.labelResultado.configure(background="#FF9999")
                
    def editar(self):
        nome = self.varNome.get().strip()
        email = self.varEmail.get().strip()
        
        if len(self.txtLista.selection()) < 1:
            self.varResultado.set("Escolha um registro para atualizar.")
            self.labelResultado.configure(background="#FF9999")
            self.entryNome.focus()
            return
        
        reNome = re.fullmatch(r"\b[A-Za-z ]+\b", nome)
        reEmail = re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email)
        
        if reNome == None:
            self.varResultado.set("O campo é obrigatório.")
            self.labelResultado.configure(background="#FF9999")
            self.entryNome.focus()
        elif reEmail == None:
            self.varResultado.set("Digite um email válido.")
            self.labelResultado.configure(background="#FF9999")
            self.entryEmail.focus()
        else:
            try:
                registro = self.txtLista.selection()[0]
                dadosRegistro = self.txtLista.item(registro)
                nomeRegistro = dadosRegistro["values"][0]
                emailRegistro = dadosRegistro["values"][1]
                
                conexao = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "base_de_dados")
                
                mycursor = conexao.cursor()
                query = "UPDATE pessoas SET nome = %s, email = %s WHERE nome = %s AND email = %s);"
                valores = (nome, email, nomeRegistro, emailRegistro)
                mycursor.execute(query, valores)
                conexao.commit()
                
                self.varNome.set("")
                self.varEmail.set("")
                
                self.consultar()
                
                self.varResultado.set("Registro atualizado.")
                self.labelResultado.configure(background="#99FF99")
                self.entryNome.focus()
            except:
                self.varResultado.set("Não foi possível atualizar as informações.")
                self.labelResultado.configure(background="#FF9999")
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
