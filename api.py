import flask
from flask import request, jsonify
from database import Base, engine
from sqlalchemy.orm import Session
from models import Client
from database import SessionLocal

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Créer une session
session = SessionLocal()
 

# 
@app.route("/clients", methods=["GET"])
def read_clients():
    clients = session.query(Client).all()
    return jsonify([{
        "codcli": client.codcli,
        "genrecli": client.genrecli,
        "nomcli": client.nomcli,
        "prenomcli": client.prenomcli,
        "adresse1cli": client.adresse1cli,
        "villecli_id": client.villecli_id,
        "telcli": client.telcli,
        "emailcli": client.emailcli,
        "portcli": client.portcli,
        "newsletter": client.newsletter
    } for client in clients])

@app.route("/clients", methods=["POST"])
def ajouter_client():
    # Créer un nouveau client
    data = request.json
    nouveau_client = Client(
        genrecli=data["genrecli"],
        nomcli=data["nomcli"],
        prenomcli=data["prenomcli"],
        adresse1cli=data["adresse1cli"],
        villecli_id=data["villecli_id"],
        telcli=data["telcli"],
        emailcli=data["emailcli"],
        portcli=data["portcli"],
        newsletter=data["newsletter"]
    )

    # Ajouter le client à la session
    session.add(nouveau_client)
    session.commit()  # Valider la transaction
    session.refresh(nouveau_client)
    # print("{prenomcli} {nomcli} ajouté avec succès")
    return jsonify({
        "codcli": nouveau_client.codcli,
        "genrecli": nouveau_client.genrecli,
        "nomcli": nouveau_client.nomcli,
        "prenomcli": nouveau_client.prenomcli,
        "adresse1cli": nouveau_client.adresse1cli,
        "villecli_id": nouveau_client.villecli_id,
        "telcli": nouveau_client.telcli,
        "emailcli": nouveau_client.emailcli,
        "portcli": nouveau_client.portcli,
        "newsletter": nouveau_client.newsletter
    }), 201

    # Fermer la session
    session.close()

if __name__ == "__main__":
    app.run(debug=True)
    
def update_client(id_client):
    # Requête pour récupérer un client par son ID
    client_id = 1
    client = session.query(Client).filter(Client.codcli == client_id).first()

    if client:
        client.telcli = "0987654321"  # Mettre à jour le numéro de téléphone
        session.commit()  # Valider la transaction

    else:
        print("Client non trouvé")

    # Fermer la session
    session.close()

def supprimer_client(id_client):
    # Requête pour récupérer un client par son ID
    client_id = 1
    client = session.query(Client).filter(Client.codcli == client_id).first()

    if client:
        session.delete(client)  # Supprimer le client
        session.commit()  # Valider la transaction
    else:
        print("Client non trouvé")

    # Fermer la session
    session.close()



@app.route('/client', methods=['POST'])
def client():
    if request.method == 'GET':
        afficher_client(id_client)
    if request.method == 'POST':
        ajouter_client()
    return jsonify({'client': 'client'})