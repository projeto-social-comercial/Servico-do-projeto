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

# schema do comerciante
comerciante_schema = {

}

# schema do endereço
endereco_schema = {

}

# schema do produto
produto_schema = {

}

DATABASE_NAME ="App_Comerciante.db"

# cadastrar comerciante
@app.route("/comerciante", methods = ["POST"])
@schema.validate(comerciante_schema)
def setComerciante():

# cadastrar endereço
@app.route("/endereco", methods = ["POST"])
@schema.validate(endereco_schema)
def setEndereco():

# cadastrar produto
@app.route("/produto", methods = ["POST"])
@schema.validate(produto_schema)
def setProduto():

# listar comerciante
@app.route("/comerciantes",  methods = ["GET"])
def getComerciantes():

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
    return jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]})

cors = CORS(app, resources={r"/*": {"origins": "*"}})

if(__name__ == '__main__'):
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
