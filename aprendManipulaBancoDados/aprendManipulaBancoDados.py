# Importa bibliotecas
import os
import sqlite3
import pandas as pd



# funcao para imprimir na tela
def imprimeDadosTela(con): 
	# Seleciona todos registros na tabela e guarda em cursor
	cur = con.execute('select * from cidade_imposto')
	regs = cur.fetchall()

	# Carregando DataFrame de biblioteca pandas
	fr = pd.DataFrame (regs, columns= [x[0] for x in cur.description])
	print(fr)
	print('\nfeito...\n')



print("\n ----- Criacao Banco ------------------------")

# Reemove o arquivo com o banco de dados SQLite (caso exista)
os.remove("imposto.db") if os.path.exists("imposto.db") else None

# Cria conexao e banco se nao existir
con = sqlite3.connect("imposto.db")

# Cria tabela
qrCriaTabela = """ 
			CREATE TABLE cidade_imposto
			(cidade varchar(20),
			estado varchar(20),
			taxa real,
			imposto integer);"""

con.execute(qrCriaTabela)
con.commit()

print('\nfeito...\n')



print("\n ----- Insercao em tabela -------------------")

# Popula tabela com registros
dados = [('Natal','Rio Grande do Norte',1.25,6),
		('Recife', 'Pernambuco', 2.6, 3),
		('Londrina', 'Paraná', 1.7, 5),
		('Rio de Janeiro', 'Rio de Janeiro', 1.6, 6),
		('Sao Paulo', 'São Paulo', 1.2, 2)]

qrInsert = "INSERT INTO cidade_imposto VALUES(?,?,?,?)"
con.executemany(qrInsert,dados)
con.commit()

# Imprime dados na Tela
imprimeDadosTela(con)



print("\n ----- Alteracao de Imposto de 3 Registro -")

# Cria novo cursor
cur2 = con.cursor()

# Alterar registro
cur2.execute(""" UPDATE cidade_imposto SET imposto = 100 WHERE cidade = 'Natal' """)

cid = 'Recife'
cur2.execute(""" UPDATE cidade_imposto SET imposto = 50 WHERE cidade = ? """, (cid,) )

cid = 'Londrina'
imp = 80

cur2.execute(""" UPDATE cidade_imposto SET imposto = ? WHERE cidade = ? """, (imp, cid) )
con.commit()

# Imprime dados na Tela
imprimeDadosTela(con)



print("\n ----- Apagar 1 Registro da tabela -")

# Apagar registro de tabela
cid = 'Rio de Janeiro'

cur2.execute(""" DELETE FROM cidade_imposto WHERE cidade = ? """, (cid,))
con.commit()

# Imprime dados na Tela
imprimeDadosTela(con)