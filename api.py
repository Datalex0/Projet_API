import flask
from flask import request, jsonify
from database import Base, engine
from sqlalchemy.orm import Session
from models import Client,Utilisateur
from database import SessionLocal 

app = flask.Flask(__name__)
app.config["DEBUG"] = True

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
 
# @app.route('/client', methods=['GET'])
# def read_liste_clients():
#     pass

@app.route('/client', methods=['GET'])
def read_client():
    return ''' <p>test</p>'''

@app.route('/client', methods=['POST'])
def ajout_client():
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

    session.add(nouveau_client)
    session.commit()  
    session.refresh(nouveau_client)
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

    if __name == "__main":
        app.run(debug=True)

@app.route('/client', methods=['DELETE'])
def supprimer_client():
    return ''' <p>test</p>'''

@app.route('/client', methods=['PUT'])
def modifier_client():
    return ''' <p>test</p>'''





@app.route('/objet', methods=['GET'])
def article():
    return

@app.route('/commande', methods=['GET'])
def commande():
    return

# AFFICHER INFOS GENERALES UTILISATEUR ( PAS ID ET ROLE )

@app.route('/utilisateurs/<int:code_utilisateur>', methods=['GET'])
def read_utilisateur(code_utilisateur):
    utilisateur = session.query(Utilisateur).filter(Utilisateur.code_utilisateur == code_utilisateur).first()
    if utilisateur is None:
        return jsonify({"message": "Utilisateur non trouvé"}), 404
    else:
        return jsonify([{
            "code_utilisateur": utilisateur.code_utilisateur,
            "nom_utilisateur": utilisateur.nom_utilisateur,
            "prenom_utilisateur": utilisateur.prenom_utilisateur,
            "username": utilisateur.username,
            "couleur_fond_utilisateur": utilisateur.couleur_fond_utilisateur,
            "date_insc_utilisateur": utilisateur.date_insc_utilisateur
    }])
 


app.run()