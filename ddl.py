import sqlite3

conn = sqlite3.connect('App_Comerciante.db')

cursor = conn.cursor()

cursor.execute("""
	CREATE TABLE tb_comerciante(
	id_comerciante INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	nome VARCHAR(45) NOT NULL,
	id_endereco INTEGER NOT NULL,
	id_produto INTEGER NOT NULL,
	email VARCHAR(255) NOT NULL,
	telefone INTEGER NOT NULL,
	instagram VARCHAR(255) NOT NULL
	);
""")

cursor.execute("""
	CREATE TABLE tb_endereco(
	id_endereco INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	logradouro VARCHAR(65) NOT NULL,
	numero INTEGER NOT NULL,
	complemento VARCHAR(45) NOT NULL,
	cidade VARCHAR(45) NOT NULL,
	estado VARCHAR(45) NOT NULL,
	cep VARCHAR(8) NOT NULL,
	ponto_referencia VARCHAR(65) NOT NULL
	);
""")

cursor.execute("""
	CREATE TABLE tb_produto(
	id_endereco INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	nome VARCHAR(45) NOT NULL,
	descricao VARCHAR(45) NOT NULL,
	preco NUMERIC(12,2) NOT NULL
	);
""")

print ("Tabelas criadas com sucesso!")
conn.close()
