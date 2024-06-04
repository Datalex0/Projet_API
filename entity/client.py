from flask import Blueprint, render_template, jsonify, request, redirect
from database.database import SessionLocal
from database.models import Client
from sqlalchemy import select, text

clients = Blueprint('client', __name__)

def ClientDict(data):
    list_clients = []
    for cli in data:
        clients = {}
        clients['codcli'] = cli[0]
        clients['genrecli'] = cli[1]
        clients['nomcli'] = cli[2]
        clients['prenomcli'] = cli[3]
        clients['adresse1cli'] = cli[4]
        clients['villecli_id'] = cli[7]
        clients['telcli'] = cli[8]
        clients['mailcli'] = cli[9]
        clients['portcli'] = cli[10]
        clients['newsletter'] = cli[11]
        list_clients.append(clients)

    return list_clients

@clients.route('/client', methods=['GET'])
def client():
    if 'id' in request.args:
        with SessionLocal() as session:
            cli = session.execute(text('SELECT * FROM t_client WHERE codcli = ' + request.args['id'])).all()

            print(client)
            """if client:
                return jsonify(ClientDict(client))
            else:
                return "Error: Aucune donnée avec cette ID"""
            return "id"
    else:
        with SessionLocal() as session:
            data = session.execute(select(Client.__table__)).all()
            #return jsonify(ClientDict(data))
            print(data)
            return "no_id"

@clients.route('/client/new', methods=['POST'])
def ajouter_client():
    if request.method == 'POST':
        data = request.json

        nouveau_client = Client(
            nom=data['nom'],
            prenom=data['prenom'],
            genre=data['genre'],
            adresse = data['adresse'],
            cp = data['cp'],
            ville = data['ville'],
            email = data['email'],
        )

        with SessionLocal() as session:
            session.add(nouveau_client)
            session.commit()

            id = session.execute(select(Client.codcli).where(Client.emailcli == data['mailcli'])).scalar()

        return redirect(f'/client?id={id}')

    return "ok"
