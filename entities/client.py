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
 

# Afficher la liste des clients
@app.route("/clients", methods=["GET"])
def afficher_clients():
    clients = session.query(Client).all()
    return jsonify([{
        "codcli": client.codcli,
        "genre": client.genre,
        "nom": client.nom,
        "prenom": client.prenom,
        "adresse": client.adresse,
        "cp": client.cp,
        "ville": client.ville,
        "email": client.email,
        "est_actif": client.est_actif
    } for client in clients])

# Afficher les infos d'un client
@app.route("/clients/<int:codcli>", methods=["GET"])
def afficher_client(codcli):
    client = session.query(Client).filter(Client.codcli == codcli).first()
    if client is None:
        return jsonify({"message": "Client non trouvé"}), 404
    else:
        return jsonify([{
            "codcli": client.codcli,
            "genre": client.genre,
            "nom": client.nom,
            "prenom": client.prenom,
            "adresse": client.adresse,
            "cp": client.cp,
            "ville": client.ville,
            "email": client.email,
            "est_actif": client.est_actif
    }])


# Ajouter un nouveau client à la base
@app.route("/clients", methods=["POST"])
def ajouter_client():
    # Créer un nouveau client
    data = request.json
    nouveau_client = Client(
        genre=data["genre"],
        nom=data["nom"],
        prenom=data["prenom"],
        adresse=data["adresse"],
        cp=data["cp"],
        ville=data["ville"],
        email=data["email"]
    )

    # Ajouter le client à la session
    session.add(nouveau_client)
    session.commit()  # Valider la transaction
    session.refresh(nouveau_client)
    return jsonify({
        "codcli": nouveau_client.codcli,
        "genre": nouveau_client.genre,
        "nom": nouveau_client.nom,
        "prenom": nouveau_client.prenom,
        "adresse": nouveau_client.adresse,
        "cp": nouveau_client.cp,
        "ville": nouveau_client.ville,
        "email": nouveau_client.email,
        "est_actif": nouveau_client.est_actif
    }), 201


# Mettre à jour une fiche client
@app.route("/clients/<int:codcli>", methods=["PUT"])
def maj_client(codcli):
    data = request.json
    # Requête pour récupérer un client par son ID
    client = session.query(Client).filter(Client.codcli == codcli).first()

    if client is None:
        return jsonify({"message": "Client non trouvé"}), 404
    
    else:
        if "genre" in data:
            client.genre = data["genre"]
        if "nom" in data:
            client.nom = data["nom"]
        if "prenom" in data:
            client.prenom = data["prenom"]
        if "adresse" in data:
            client.adresse = data["adresse"]
        if "cp" in data:
            client.cp = data["cp"]
        if "ville" in data:
            client.ville = data["ville"]
        if "email" in data:
            client.email = data["email"]
        if "est_actif" in data:
            client.est_actif = data["est_actif"]
    
    # Valider la transaction
    session.commit()
    session.refresh(client)
    
    return jsonify({
        "codcli": client.codcli,
        "genre": client.genre,
        "nom": client.nom,
        "prenom": client.prenom,
        "adresse": client.adresse,
        "ville": client.ville,
        "email": client.email,
        "est actif": client.est_actif
    })


# Supprimer (désactiver) une fiche client
@app.route("/clients/<int:codcli>/desactiver", methods=["PUT"])
def desactiv_client(codcli):
    # Requête pour récupérer un client par son ID
    client = session.query(Client).filter(Client.codcli == codcli).first()
    
    if client is None:
            return jsonify({"error": "Client non trouvé"}), 404
        
    else:
        client.est_actif = False
        session.commit()
        session.refresh(client)
        return jsonify({
            "codcli": client.codcli,
            "est_actif": client.est_actif
    })

if __name__ == "__main__":
    app.run(debug=True)