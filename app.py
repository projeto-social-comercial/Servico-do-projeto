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
handler = logging.FileHandler("appComerciante.log")
handler.setFormatter(formatter)
logger = app.logger
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# validação
schema = JsonSchema()
schema.init_app(app)

# schema do empresa
empresa_schema = {
    "required": ["nome", "id_endereco", "email", "telefone", "instagram", "facebook"],
    "properties": {
        "nome" : {"type" : "string"},
        "id_endereco" : {"type" : "integer"},
        "email" : {"type" : "string"},
        "telefone" : {"type" : "string"},
        "instagram" : {"type" : "string"},
        "facebook" : {"type" : "string"}
    }
}

# schema do endereço
endereco_schema = {
    "required": ["logradouro","numero", "cidade", "estado", "cep"],
    "properties": {
        "logradouro" : {"type" : "string"},
        "numero" : {"type" : "string"},
        "complemento" : {"type" : "string"},
        "cidade" : {"type" : "string"},
        "estado" : {"type" : "string"},
        "cep" : {"type" : "string"},
        "ponto_referencia" : {"type" : "string"}
    }
}

# schema do produto
produto_schema = {
    "required": ["nome", "descricao", "preco"],
    "properties": {
        "nome" : {"type" : "string"},
        "descricao" : {"type" : "string"},
        "preco" : {"type" : "string"}
    }
}

DATABASE_NAME ="App_Comerciante.db"

# cadastrar empresa
@app.route("/empresa", methods = ["POST"])
@schema.validate(empresa_schema)
def setEmpresa():
    logger.info("Cadastrando empresa.")
    empresa = request.get_json()
    nome = empresa["nome"]
    id_endereco = empresa["id_endereco"]
    email = empresa["email"]
    telefone = empresa["telefone"]
    instagram = empresa["instagram"]
    facebook = empresa["facebook"]

    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            insert into tb_empresa(nome, id_endereco, email, telefone, instagram, facebook)
            values(?, ?, ?, ?, ?, ?);
        """, (nome, id_endereco, email, telefone, instagram, facebook))
        conn.commit()
        id = cursor.lastrowid
        empresa["id"] = id
    except(sqlite3.Error, Exception) as e:
        logger.error("Aconteceu um erro.")
        logger.error("Exceção: %s" % e)
    finally:
        if conn:
            conn.close()
    logger.info("Empresa cadastrada com sucesso.")
    return jsonify(empresa)

# cadastrar endereço
@app.route("/endereco", methods = ["POST"])
@schema.validate(endereco_schema)
def setEndereco():
    logger.info("Cadastrando endereço.")
    endereco = request.get_json()
    logradouro = endereco["logradouro"]
    numero = endereco["numero"]
    complemento = endereco["complemento"]
    cidade = endereco["cidade"]
    estado = endereco["estado"]
    cep = endereco["cep"]
    ponto_referencia = endereco["ponto_referencia"]

    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            insert into tb_endereco(logradouro, numero, complemento, cidade, estado, cep, ponto_referencia)
            values(?, ?, ?, ?, ?, ?, ?);
        """, (logradouro, numero, complemento, cidade, estado, cep, ponto_referencia))
        conn.commit()
        id = cursor.lastrowid
        endereco["id"] = id
    except(sqlite3.Error, Exception) as e:
        logger.error("Aconteceu um erro.")
        logger.error("Exceção: %s" % e)
    finally:
        if conn:
            conn.close()
    logger.info("Endereço cadastrado com sucesso.")
    return jsonify(endereco)

# cadastrar produto
@app.route("/produto", methods = ["POST"])
@schema.validate(produto_schema)
def setProduto():
    logger.info("Cadastrando produto.")
    produto = request.get_json()
    nome = produto["nome"]
    descricao = produto["descricao"]
    preco = produto["preco"]

    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            insert into tb_produto(nome, descricao, preco)
            values(?, ?, ?);
        """, (nome, descricao, preco))
        conn.commit()
        id = cursor.lastrowid
        produto["id"] = id
    except(sqlite3.Error, Exception) as e:
        logger.error("Aconteceu um erro.")
        logger.error("Exceção: %s" % e)
    finally:
        if conn:
            conn.close()
    logger.info("Produto cadastrado com sucesso.")
    return jsonify(produto)

# listar empresas
@app.route("/empresas",  methods = ["GET"])
def getEmpresas():
    logger.info("Listando empresas.")
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            select id_empresa, empresa.nome,
            endereco.logradouro, endereco.numero, endereco.complemento, endereco.cidade,
            endereco.estado, endereco.cep, endereco.ponto_referencia,
            empresa.email, empresa.telefone, empresa.instagram, empresa.facebook
            from tb_empresa empresa
            inner join tb_endereco endereco on(empresa.id_endereco = endereco.id_endereco);
        """)
        empresas = []
        for linha in cursor.fetchall():
            empresa = {
                "id" : linha[0],
                "nome" : linha[1],
                "logradouro" : linha[2],
                "numero" : linha[3],
                "complemento" : linha[4],
                "cidade" : linha[5],
                "estado" : linha[6],
                "cep" : linha[7],
                "ponto_referencia" : linha[8],
                "email" : linha[9],
                "telefone" : linha[10],
                "instagram" : linha[11],
                "facebook" : linha[12]
            }
            empresas.append(empresa)
        conn.close()
    except(sqlite3.Error):
         logger.error("Aconteceu um erro.")
    logger.info("Empresas listadas com sucesso.")
    return jsonify(empresas)

# Mensagem de erro para recurso não encontrado.
@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]}), 400

cors = CORS(app, resources={r"/*": {"origins": "*"}})

if(__name__ == '__main__'):
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
