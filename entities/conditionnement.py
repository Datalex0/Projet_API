from flask import request, jsonify, Blueprint
from database.models import Conditionnement
from database.database import SessionLocal

cond = Blueprint('conditionnement', __name__)


# Créer une session
session = SessionLocal()

# Afficher la liste des conditionnements
@cond.route("/conditionnements", methods=["GET"])
def afficher_conditionnements():
    conditionnements = session.query(Conditionnement).all()
    return jsonify([{
        "idcondit": conditionnement.idcondit,
        "libcondit": conditionnement.libcondit,
        "poidscondit": conditionnement.poidscondit,
        "qte_min": conditionnement.qte_min,
        "qte_max": conditionnement.qte_max,
        "est_actif": conditionnement.est_actif
    } for conditionnement in conditionnements])

# Afficher les infos d'un conditionnement
@cond.route("/conditionnements/<int:idcondit>", methods=["GET"])
def afficher_conditionnement(idcondit):
    conditionnement = session.query(Conditionnement).filter(Conditionnement.idcondit == idcondit).first()
    if conditionnement is None:
        return jsonify({"message": "Conditionnement non trouvé"}), 404
    else:
        return jsonify([{
            "idcondit": conditionnement.idcondit,
            "libcondit": conditionnement.libcondit,
            "poidscondit": conditionnement.poidscondit,
            "qte_min": conditionnement.qte_min,
            "qte_max": conditionnement.qte_max,
            "est_actif": conditionnement.est_actif
    }])


# Ajouter un nouveau conditionnement à la base
@cond.route("/conditionnements", methods=["POST"])
def ajouter_conditionnement():
    # Créer un nouveau conditionnement
    data = request.json
    nouveau_conditionnement = Conditionnement(
        libcondit=data["libcondit"],
        poidscondit=data["poidscondit"],
        qte_min=data["qte_min"],
        qte_max=data["qte_max"]
    )

    # Ajouter le conditionnement à la session
    session.add(nouveau_conditionnement)
    session.commit()  # Valider la transaction
    session.refresh(nouveau_conditionnement)
    return jsonify({
        "idcondit": nouveau_conditionnement.idcondit,
        "libcondit": nouveau_conditionnement.libcondit,
        "poidscondit": nouveau_conditionnement.poidscondit,
        "qte_min": nouveau_conditionnement.qte_min,
        "qte_max": nouveau_conditionnement.qte_max,
        "est_actif": nouveau_conditionnement.est_actif
    }), 201


# Mettre à jour une fiche conditionnement
@cond.route("/conditionnements/<int:idcondit>", methods=["PUT"])
def maj_conditionnement(idcondit):
    data = request.json
    # Requête pour récupérer un conditionnement par son ID
    conditionnement = session.query(Conditionnement).filter(Conditionnement.idcondit == idcondit).first()

    if conditionnement is None:
        return jsonify({"message": "Conditionnement non trouvé"}), 404
    
    else:
        if "libcondit" in data:
            conditionnement.libcondit = data["libcondit"]
        if "poidscondit" in data:
            conditionnement.poidscondit = data["poidscondit"]
        if "qte_min" in data:
            conditionnement.qte_min = data["qte_min"]
        if "qte_max" in data:
            conditionnement.qte_max = data["qte_max"]
        if "est_actif" in data:
            conditionnement.est_actif = data["est_actif"]
    
    # Valider la transaction
    session.commit()
    session.refresh(conditionnement)
    
    return jsonify({
        "idcondit": conditionnement.idcondit,
        "libcondit": conditionnement.libcondit,
        "poidscondit": conditionnement.poidscondit,
        "qte_min": conditionnement.qte_min,
        "qte_max": conditionnement.qte_max,
        "est actif": conditionnement.est_actif
    })


# Supprimer (désactiver) une fiche conditionnement
@cond.route("/conditionnements/<int:idcondit>/desactiver", methods=["PUT"])
def desactiv_conditionnement(idcondit):
    # Requête pour récupérer un conditionnement par son ID
    conditionnement = session.query(Conditionnement).filter(Conditionnement.idcondit == idcondit).first()
    
    if conditionnement is None:
            return jsonify({"error": "Conditionnement non trouvé"}), 404
        
    else:
        conditionnement.est_actif = False
        session.commit()
        session.refresh(conditionnement)
        return jsonify({
            "idcondit": conditionnement.idcondit,
            "est_actif": conditionnement.est_actif
    })
