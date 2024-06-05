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

# OBJET
@app.route('/objet', methods=['POST'])
def ajout_objet():
    # Créer un nouveau client
    data = request.json
    nouvelobjet = Objet(
        codobj=data["codobj"],
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

@app.route('/objet/suppr', methods=['PUT'])
# Fonction de suppression (en réalité de désactivation) d'un objet:
def suppr_objet():
    
    # On récupère l'objet à supprimer par son codobj
    data = request.get_json()
    
    codobj = data.get('codobj')
    
    # Si le codobj est mal rentré, on retourne un code HTTP ERROR 400
    if codobj is None:
        return jsonify({'Alerte': 'Code de l\'objet incorrect'}), 400
    
    obj = Objet.query.get(codobj)
    
    # Si le codobj est introuvable dans la base, on retourne un code HTTP ERROR 404
    if obj is None : 
        return jsonify({'Alerte' : 'Objet introuvable'}), 404
    
    # Objet trouvé : on le désaactive puis on valide l'opération avec le commit pour mettre à jour la base et on retourne un code HTTP 200 de succès.
    obj.est_actif = False
    session.commit()
    
    return jsonify({'message': 'Objet désactivé avec succès'}), 200

@app.route('/objet/modifier', methods=['PUT'])
def modifier_objet():
    # On récupère les paramètres
    data = request.get_json()
    
    codobj = data.get('codobj')
    parametre = data.get('parametre')
    value = data.get('value')
    
    # Si le codobj est mal rentré, on retourne un code HTTP ERROR 400
    if codobj is None:
        return jsonify({'Alerte': 'Code de l\'objet incorrect'}), 400
    
    # Si le parametre ou value est manquant, on retourne un code HTTP ERROR 400
    if parametre is None or value is None:
        return jsonify({'Alerte': 'Paramètre ou valeur non fourni'}), 400
    
    obj = Objet.query.get(codobj)
    
    # Si le codobj est introuvable dans la base, on retourne un code HTTP ERROR 404
    if obj is None : 
        return jsonify({'Alerte' : 'Objet introuvable'}), 404
    
    # Objet trouvé : On sélectionne le paramètre à modifier et on attribue la valeur donnée
    if hasattr(obj, parametre):
        setattr(obj, parametre, value)
    # Si le paramètre n'est pas valide on retourne une erreur 400 : 
    else:
        return jsonify({'Alerte': 'Paramètre invalide'}), 400
    
    # On valide l'opération avec le commit pour mettre à jour la base et on retourne un code HTTP 200 de succès.
    session.commit()
    return jsonify({'message': 'Objet modifié avec succès'}), 200

@app.route('/objet/consulter', methods=['GET'])
def afficher_objet(codobjet):
    obj = session.query(Objet).filter(Objet.codobj == codobjet).first()
    if obj is None:
        return jsonify({"message": "Objet non trouvé"}), 404
    else:
        return jsonify([{
        "codobj": obj.codobj,
        "libobj": obj.libobj,
        "poidsobj": obj.poidsobj,
        "nb_points": obj.nb_points,
        "est_actif": obj.est_actif
    }])
