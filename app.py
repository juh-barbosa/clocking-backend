from bson import ObjectId
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

connection_string = "mongodb+srv://julia:10092019Juvi@clock.zkfozyb.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)

database_name = "clocking"
db = client[database_name]

collection_marking = db["marking"]
collection_users = db["users"]

app = Flask(__name__)
CORS(app)

@app.route('/get',methods=['GET'])
def gethello():
    return'hello'

@app.route('/users/<string:user>/<string:password>', methods=['GET'])
def validateUser(user, password):
    get = collection_users.find_one({"username": user})

    if get:
        get['_id'] = str(get['_id'])
        if get['password'] == "":
            collection_users.find_one_and_update(
                {"username": user}, {"$set": {"password": password}}
            )

        getForValidate = collection_users.find_one({"username": user})

        if getForValidate['username'] == user and getForValidate['password'] == password:
            return jsonify({"message": "Usuário validado."}), 200

        getForValidate['username'] 
        
        return jsonify(get), 200
    else:
        return jsonify({"message": "Usuário não encontrado."}), 404

@app.route('/marking/<string:username>', methods=['POST'])
def postMarking(username):
    if request.is_json:
        marking = request.get_json()

        post = {
            "dia": marking['dia'],
            "mes": marking['mes'],
            "ano": marking['ano'],
            "tipo": marking['tipo'],
            "estado": marking['estado'],
            "hora": marking['hora'],
            "colaborador": username,
            "status": marking['status']
        }

        collection_marking.insert_one(post)

        return jsonify({"message": "Hora inserida com sucesso."}), 201
    else:
        return jsonify({"message": "Corpo da requisição não é um JSON válido."}), 400

@app.route('/marking/many/<string:username>', methods=['POST'])
def postMarkingMany(username):
    if request.is_json:
        marking = request.get_json()

        for i in marking:
            post = {
                "dia": i['dia'],
                "mes": i['mes'],
                "ano":i['ano'],
                "tipo": i['tipo'],
                "estado": i['estado'],
                "hora": i['hora'],
                "colaborador": username,
                "status": i['status']
            }

            collection_marking.insert_one(post)
        
        return jsonify({"message": "Hora inserida com sucesso."}), 201
    else:
        return jsonify({"message": "Corpo da requisição não é um JSON válido."}), 400
    
@app.route('/marking/approve/<string:_id>/<string:status>', methods=['PUT'])
def approveHours(_id,status):
    object_id = ObjectId(_id)

    documento = collection_marking.find_one({"_id": object_id})
    if documento:
        collection_marking.update_one({"_id": object_id}, {"$set": {"status": status}})
        return jsonify({"message": "Hora validada com sucesso."}), 201
    else:
        return jsonify({"message": "Documento não encontrado."}), 40

@app.route('/marking/get/<string:mes>', methods=['GET'])
def getHours(mes):
    response = collection_marking.find({"mes": mes})

    documentos = list(response)

    if documentos:
        for documento in documentos:
            documento['_id'] = str(documento['_id'])

        return jsonify(documentos), 200
    else:
        return jsonify({"message": "Nenhum documento encontrado para o mês especificado."}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3050)