# importações
from flask import Flask
from flask import request
from flask import jsonify
from flask_json_schema import JsonSchema, JsonValidationError
from flask_cors import CORS
import logging
import sqlite3

app = Flask(__name__)

# Logging
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("escolaapp.log")
handler.setFormatter(formatter)
logger = app.logger
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# validação
schema = JsonSchema()
schema.init_app(app)

comerciante_schema = {

}

DATABASE_NAME = "EscolaApp_versao2.db"

# listar comerciantes
@app.route("/comerciante",  methods = ["GET"])
def getProfessores():
    logger.info("Listando comerciante.")
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            select * from tb_comerciante;
        """)
        comerciante = []
        for linha in cursor.fetchall():
            comerciante = {
                "id" : linha[0],
                "nome" : linha[1],
                "id_endereco" : linha[2]
            }
            comerciante.append(comerciante)
        conn.close()
    except(sqlite3.Error):
         logger.error("Aconteceu um erro.")
    logger.info("Professores listados com sucesso.")
    return jsonify(comerciante)

# cadastrar comerciante
@app.route("/comerciante", methods = ["POST"])
@schema.validate(comerciante_schema)
def setProfessor():
    logger.info("Cadastrando comerciante.")
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        comerciante = request.get_json()
        nome = comerciante["nome"]
        id_endereco = comerciante["id_endereco"]

        cursor.execute("""
            insert into tb_comerciante(nome, id_endereco)
            values(?,?);
        """, (nome, id_endereco))
        conn.commit()
        id = cursor.lastrowid
        comerciante["id"] = id
    except(sqlite3.Error, Exception) as e:
        logger.error("Aconteceu um erro.")
        logger.error("Exceção: %s" % e)
    finally:
        if conn:
            conn.close()
    logger.info("Professor cadastrado com sucesso.")
    return jsonify(comerciante)
