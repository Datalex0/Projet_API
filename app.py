from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Index, Numeric, Float,MetaData

from sqlalchemy.orm import relationship

from database import Base, engine, SessionLocal
import flask
from flask import request, jsonify

from models import *
# Flask

app = flask.Flask(__name__)

app.config["DEBUG"] = True
#Affiche un message autre que bad gateway s'il y a une erreur dans l'appli

session = SessionLocal()

@app.route('/', methods=['GET'])
def home():
	return '''<h1>Bienvenue sur notre projet d'API</h1>
	<p><strong>Avec la participation de :</strong> </br></br>Alexis MURAIL</br>Kévin Perquy</br>Luis-Miguel Borderon</br>Florence Bouchart</p>
	<h2>Entités : </h2>
 	<a href = '/client'><h3>Client</h3></a>
	<a href = '/objet'><h3>Objet</h3></a>
	<a href = '/commande'><h3>Commande</h3></a>
	<a href = '/utilisateur'><h3>Utilisateur</h3></a>
 '''

@app.route("/clients", methods=["POST"])
def ajouterclient():
    # Créer un nouveau client
    data = request.json
    nouveau_client = Client(
        genrecli=data["genrecli"],
        nomcli=data["nomcli"],
        prenomcli=data["prenomcli"],
        adresse1cli=data["adresse1cli"],
        villecliid=data["villecliid"],
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


@app.route('/client/suppr', methods=['GET'])
def suppr():
    return ''' <h1>Supprimer un client : </h1>'''

@app.route('/client/modifier', methods=['GET'])
def modifier():
    return ''' <h1>Modifier un client : </h1>'''

@app.route('/client/consulter', methods=['GET'])
def consulter():
    return ''' <h1>Consulter un client : </h1>'''

# OBJET
@app.route('/objet', methods=['POST'])
def ajout_objet():
    # Créer un nouveau client
    data = request.json
    nouvelobjet = Objet(
        codobj=data["genrecli"],
        libobj=data["libobj"],
        poidsobj=data["poidsobj"],
        nb_points=data["nb_points"]
    )

    # Ajouter le client à la session
    session.add(nouvelobjet)
    session.commit()  # Valider la transaction
    session.refresh(nouvelobjet)
    # print("{prenomcli} {nomcli} ajouté avec succès")
    return jsonify({
        "codobj": nouvelobjet.codobj,
        "libobj": nouvelobjet.libobj,
        "poidsobj": nouvelobjet.poidsobj,
        "nb_points": nouvelobjet.nb_points,
    }), 201


@app.route('/objet/suppr', methods=['GET'])
def suppr_objet(codobj):
    codobj = request.args.get('codobj')
    if codobj is None:
        return jsonify({'Alerte': 'Code de l\'objet non fourni'}), 400
    obj = Objet.query.get(codobj)
    if obj is None : 
        return jsonify({'Alerte' : 'Objet introuvable'}), 404
    obj.est_actif = False
    session.commit()
    return 

# @app.route('/objet/modifier', methods=['GET'])
# def modifier():
#     return ''' <h1>Modifier un objet : </h1>'''

# @app.route('/objet/consulter', methods=['GET'])
# def suppr():
#     return ''' <h1>Consulter un objet : </h1>'''

# # COMMANDE
# @app.route('/commande', methods=['GET'])
# def commande():
#     return

# @app.route('/commande/ajout', methods=['GET'])
# def ajout():
#     return ''' <h1>Ajouter une commande : </h1>'''

# @app.route('/commande/suppr', methods=['GET'])
# def suppr():
#     return ''' <h1>Supprimer une commande : </h1>'''

# @app.route('/commande/modifier', methods=['GET'])
# def modifier():
#     return ''' <h1>Modifier une commande : </h1>'''

# @app.route('/commande/consulter', methods=['GET'])
# def suppr():
#     return ''' <h1>Consulter une commande : </h1>'''

# # UTILISATEUR
# @app.route('/utilisateur', methods=['GET'])
# def utilisateur():
#     return

# @app.route('/utilisateur/ajout', methods=['GET'])
# def ajout():
#     return ''' <h1>Ajouter un utilisateur : </h1>'''

# @app.route('/utilisateur/suppr', methods=['GET'])
# def suppr():
#     return ''' <h1>Supprimer un utilisateur : </h1>'''

# @app.route('/utilisateur/modifier', methods=['GET'])
# def modifier():
#     return ''' <h1>Modifier un utilisateur : </h1>'''

# @app.route('/utilisateur/consulter', methods=['GET'])
# def suppr():
#     return ''' <h1>Consulter un utilisateur : </h1>'''


if __name__ == "__main__":
    app.run(debug=True)
