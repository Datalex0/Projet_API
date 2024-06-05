import flask
from flask import request, jsonify
from database import Base, engine
from sqlalchemy.orm import Session
from models import Utilisateur
from database import SessionLocal 

app = flask.Flask(__name__)
app.config["DEBUG"] = True

session = SessionLocal()

# Ajouter Utilisateur :

@app.route('/utilisateurs', methods=['POST'])
def ajout_utilisateur():
    data = request.json
    nouveau_utilisateur = Utilisateur(
        code_utilisateur=data["code_utilisateur"],
        nom_utilisateur=data["nom_utilisateur"],
        prenom_utilisateur=data["prenom_utilisateur"],
        username=data["username"],
        date_insc_utilisateur=data["date_insc_utilisateur"]
    )

    session.add(nouveau_utilisateur)
    session.commit()  
    session.refresh(nouveau_utilisateur)
    return jsonify({
        "code_utilisateur": nouveau_utilisateur.code_utilisateur,
        "nom_utilisateur": nouveau_utilisateur.nom_utilisateur,
        "prenom_utilisateur": nouveau_utilisateur.prenom_utilisateur,
        "username": nouveau_utilisateur.username,
        "date_insc_utilisateur": nouveau_utilisateur.date_insc_utilisateur,
        "est_actif": nouveau_utilisateur.est_actif
    }), 201


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

if __name__ == "__main__":
    app.run(debug=True)