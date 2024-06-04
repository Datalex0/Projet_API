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

# @app.route('/client', methods=['GET'])
# def read_client():
#     return ''' <p>test</p>'''

# @app.route('/client', methods=['POST'])
# def ajout_client():
#     # Créer un nouveau client
#     data = request.json
#     nouveau_client = Client(
#         genrecli=data["genrecli"],
#         nomcli=data["nomcli"],
#         prenomcli=data["prenomcli"],
#         adresse1cli=data["adresse1cli"],
#         villecliid=data["villecliid"],
#         telcli=data["telcli"],
#         emailcli=data["emailcli"],
#         portcli=data["portcli"],
#         newsletter=data["newsletter"]
#     )

#     session.add(nouveau_client)
#     session.commit()  
#     session.refresh(nouveau_client)
#     return jsonify({
#         "codcli": nouveau_client.codcli,
#         "genrecli": nouveau_client.genrecli,
#         "nomcli": nouveau_client.nomcli,
#         "prenomcli": nouveau_client.prenomcli,
#         "adresse1cli": nouveau_client.adresse1cli,
#         "villecli_id": nouveau_client.villecli_id,
#         "telcli": nouveau_client.telcli,
#         "emailcli": nouveau_client.emailcli,
#         "portcli": nouveau_client.portcli,
#         "newsletter": nouveau_client.newsletter
#     }), 201

#     if __name == "__main":
#         app.run(debug=True)

# @app.route('/client', methods=['DELETE'])
# def supprimer_client():
#     return ''' <p>test</p>'''

# @app.route('/client', methods=['PUT'])
# def modifier_client():
#     return ''' <p>test</p>'''


# @app.route('/objet', methods=['GET'])
# def article():
#     return

# @app.route('/commande', methods=['POST'])
# def commande():
#     return

# Ajouter Utilisateur :

@app.route('/utilisateurs', methods=['POST'])
def ajout_utilisateur():
    data = request.json
    nouveau_utilisateur = Utilisateur(
        code_utilisateur=data["code_utilisateur"],
        nom_utilisateur=data["nom_utilisateur"],
        prenom_utilisateur=data["prenom_utilisateur"],
        username=data["username"],
        date_insc_utilisateur=data["date_insc_utilisateur"],
    )

    session.add(nouveau_utilisateur)
    session.commit()  
    session.refresh(nouveau_utilisateur)
    return jsonify({
        "code_utilisateur": nouveau_utilisateur.code_utilisateur,
        "nom_utilisateur": nouveau_utilisateur.nom_utilisateur,
        "prenom_utilisateur": nouveau_utilisateur.prenom_utilisateur,
        "username": nouveau_utilisateur.username,
        " date_insc_utilisateur": nouveau_utilisateur.date_insc_utilisateur,
        "est_actif": nouveau_utilisateur.est_actif
    }), 201

    if __name == "__main":
        app.run(debug=True)

# Afficher liste utilisateur

@app.route("/utilisateurs", methods=["GET"])
def read_liste_utilisateurs():
    utilisateurs = session.query(Utilisateur).all()
    return jsonify([{
            "code_utilisateur": utilisateur.code_utilisateur,
            "nom_utilisateur": utilisateur.nom_utilisateur,
            "prenom_utilisateur": utilisateur.prenom_utilisateur,
            "username": utilisateur.username,
            "date_insc_utilisateur": utilisateur.date_insc_utilisateur,
            "est_actif": utilisateur.est_actif
    } for utilisateur in utilisateurs])

# Afficher infos utilisateur

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
            "date_insc_utilisateur": utilisateur.date_insc_utilisateur,
            "est_actif": utilisateur.est_actif
    }])
 
# Mettre à jour les infos Utilisateur 

@app.route("/utilisateurs/<int:code_utilisateur>", methods=["PUT"])
def maj_utilisateur(code_utilisateur):
    data = request.json
    utilisateur = session.query(Utilisateur).filter(Utilisateur.code_utilisateur == code_utilisateur).first()

    if utilisateur is None:
        return jsonify({"message": "Utilisateur non trouvé"}), 404

    else:
        if "code_utilisateur" in data:
            utilisateur.code_utilisateur = data["code_utilisateur"]
        if "nom_utilisateur" in data:
            utilisateur.nom_utilisateur = data["nom_utilisateur"]
        if "prenom_utilisateur" in data:
            utilisateur.prenom_utilisateur = data["prenom_utilisateur"]
        if "username" in data:
            utilisateur.username = data["username"]
        if "date_insc_utilisateur" in data:
            utilisateur.date_insc_utilisateur = data["date_insc_utilisateur"]
        if "est_actif" in data:
            utilisateur.est_actif = data["est_actif"]

    session.commit()
    session.refresh(utilisateur)

    return jsonify({
        "code_utilisateur":  utilisateur.code_utilisateur,
        "nom_utilisateur":  utilisateur.nom_utilisateur,
        "prenom_utilisateur":  utilisateur.prenom_utilisateur,
        "username":  utilisateur.username,
        "date_insc_utilisateur":  utilisateur.date_insc_utilisateur,
        "est_actif": utilisateur.est_actif
    }) 



# Supprimer ( désactiver ) Utilisateur

@app.route("/utilisateurs/<int:code_utilisateur>/desactiver", methods=["PUT"])
def desactiv_utilisateur(code_utilisateur):
    utilisateur = session.query(Utilisateur).filter(Utilisateur.code_utilisateur == code_utilisateur).first()
    
    if utilisateur is None:
            return jsonify({"error": "Utilisateur non trouvé"}), 404     
    else:
        utilisateur.est_actif = False
        session.commit()
        session.refresh(utilisateur)
        return jsonify({
            "code_utilisateur": utilisateur.code_utilisateur,
            "est_actif": utilisateur.est_actif
        })

app.run()