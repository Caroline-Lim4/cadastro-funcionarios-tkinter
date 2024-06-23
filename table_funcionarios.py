# import psycopg2
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime

# classe de funcionarios
class FuncionarioDB:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self._criar_tabela()

    # criar tabela caso nao exista
    def _criar_tabela(self):
        try:
            create_table_query = """
                CREATE TABLE IF NOT EXISTS cad_funcionarios (
                    user_id serial PRIMARY KEY,
                    nome VARCHAR(50) NOT NULL,
                    data_contratação TIMESTAMP NOT NULL,
                    idade INTEGER CHECK (idade >= 18),
                    salario INTEGER NOT NULL
                );
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()

        except sqlite3.DatabaseError as error:
            # printa o erro caso a tabela já exista
            print(error)

    # inserir novos dados
    def _inserir_dados(self, dados_para_inserir):
        insert_data_query = """
            INSERT INTO cad_funcionarios (user_id, nome, data_contratação, idade, salario)
            VALUES (?, ?, ?, ?, ?);
        """
        self.cursor.execute(insert_data_query, dados_para_inserir)
        self.connection.commit()

    # consultando dados 
    def _consultar_dados(self):
        consulta_query = "SELECT * FROM cad_funcionarios;"
        self.cursor.execute(consulta_query)
        dados = self.cursor.fetchall()
        return dados

    # Atualizar dados
    def _atualizar_dados(self, user_id, salario):
        atualizacao_query = "UPDATE cad_funcionarios SET salario = ? WHERE user_id = ?;"
        self.cursor.execute(atualizacao_query, (salario, user_id))
        self.connection.commit()

    # Excluir dados
    def _excluir_dados(self, user_id_para_excluir):
        exclusao_query = "DELETE FROM cad_funcionarios WHERE user_id = ?;"
        self.cursor.execute(exclusao_query, (user_id_para_excluir,))
        self.connection.commit()

    # fechar conexao
    def _fechar_conexao(self):
        self.cursor.close()
        self.connection.close()
        print('Operação concluída com sucesso!')
        
class FuncionarioGUI:
    def __init__(self, root, funcionario_db):
        self.funcionario_db = funcionario_db
        
        self.root = root
        self.root.title("Cadastro de Funcionários")
        self.root.geometry('400x200')

        # Configura a interface gráfica
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Criar widgets
        self.label_id = ttk.Label(self.frame, text="Id:")
        self.entry_id = ttk.Entry(self.frame, width=10)
        
        self.label_nome = ttk.Label(self.frame, text="Nome:")
        self.entry_nome = ttk.Entry(self.frame, width=30)

        self.label_idade = ttk.Label(self.frame, text="Idade:")
        self.entry_idade = ttk.Entry(self.frame, width=10)

        self.label_salario = ttk.Label(self.frame, text="Salário:")
        self.entry_salario = ttk.Entry(self.frame, width=10)

        self.btn_criar = ttk.Button(self.frame, text="Criar", command=self.criar_funcionario)
        self.btn_consultar = ttk.Button(self.frame, text="Consultar Dados", command=self.consultar_dados)
        self.btn_atualizar = ttk.Button(self.frame, text="Atualizar", command=self.atualizar_funcionario)
        self.btn_excluir = ttk.Button(self.frame, text="Excluir", command=self.excluir_funcionario)

        # Layout dos widgets
        self.label_id.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.entry_id.grid(column=1, row=0, padx=5, pady=5)
        
        self.label_nome.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.entry_nome.grid(column=1, row=1, columnspan=2, padx=5, pady=5)

        self.label_idade.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.entry_idade.grid(column=1, row=2, padx=5, pady=5)

        self.label_salario.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.entry_salario.grid(column=1, row=3, padx=5, pady=5)

        self.btn_criar.grid(column=0, row=4, pady=10)
        self.btn_atualizar.grid(column=1, row=4, pady=10)
        self.btn_consultar.grid(column=2, row=4, pady=10)
        self.btn_excluir.grid(column=3, row=4, pady=10)

    def criar_funcionario(self):
        user_id = int(self.entry_id.get())
        nome = self.entry_nome.get()
        idade = int(self.entry_idade.get())
        salario = int(self.entry_salario.get())

        data_contratacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        dados_para_inserir = [user_id, nome, data_contratacao, idade, salario]

        self.funcionario_db._inserir_dados(dados_para_inserir)
        messagebox.showinfo("Sucesso","Funcionário criado com sucesso!")
        
    def consultar_dados(self):
        # Chama a função _consultar_dados do FuncionarioDB
        dados_consultados = self.funcionario_db._consultar_dados()

        # Cria uma janela para mostrar os dados consultados
        consulta_window = tk.Toplevel(self.root)
        consulta_window.title("Consulta de Funcionários")

        tree = ttk.Treeview(consulta_window)
        tree["columns"] = ("ID", "Nome", "Data de Contratação", "Idade", "Salário")
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Data de Contratação", text="Data de Contratação")
        tree.heading("Idade", text="Idade")
        tree.heading("Salário", text="Salário")

        for dado in dados_consultados:
            tree.insert("", "end", values=dado)

        tree.pack(expand=True, fill="both")

    def atualizar_funcionario(self):
        # Janela de diálogo para obter o ID e o novo salário
        user_id = simpledialog.askinteger("Atualizar Funcionário", "Digite o ID do funcionário:")
        novo_salario = simpledialog.askinteger("Atualizar Funcionário", "Digite o novo salário do funcionário:")

        if user_id is not None and novo_salario is not None:
            # Chamar a função de atualizar dados do banco de dados
            self.funcionario_db._atualizar_dados(user_id, novo_salario)
            messagebox.showinfo("Sucesso", f"Funcionário {user_id} atualizado com sucesso!")

    def excluir_funcionario(self):
        # Janela de diálogo para obter o ID do funcionário a ser excluído
        user_id_para_excluir = simpledialog.askinteger("Excluir Funcionário", "Digite o ID do funcionário a ser excluído:")

        if user_id_para_excluir is not None:
            # Chamar a função de excluir dados do banco de dados
            self.funcionario_db._excluir_dados(user_id_para_excluir)
            messagebox.showinfo("Sucesso", f"Funcionário {user_id_para_excluir} excluído com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    # Exemplo de utilização da classe
    funcionario_db = FuncionarioDB('funcionarios.db')
    
    app = FuncionarioGUI(root, funcionario_db)
    root.mainloop()
    
funcionario_db._fechar_conexao()

    