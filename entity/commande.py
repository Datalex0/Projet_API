from flask import Blueprint, request, jsonify, redirect
from database.database import SessionLocal
from database.models import Commande
from sqlalchemy import select, text

cde = Blueprint('commande', __name__)

def ConvertToJson(data):
    commande = []
    for cmd in data:
        cmd_list = {}
        cmd_list['codcde'] = cmd[0].codcde
        cmd_list['datcde'] = cmd[0].datcde
        cmd_list['codcli'] = cmd[0].codcli
        cmd_list['montant_total'] = cmd[0].montant_total
        cmd_list['code_utilisateur'] = cmd[0].code_utilisateur
        cmd_list['num_suivi'] = cmd[0].num_suivi
        cmd_list['datexp'] = cmd[0].datexp
        cmd_list['est_actif'] = cmd[0].est_actif
        commande.append(cmd_list)

    return commande


@cde.route('/commande', methods=["GET"])
def afficher_commande():
    if 'id_cli' in request.args:
        with SessionLocal() as session:
            data = session.execute(select(Commande).where(Commande.codcli == request.args['id_cli'])).all()

            if data:
                return jsonify(ConvertToJson(data))
            else:
                return "Error: Aucune donnée avec cette ID"

    elif 'id_cde' in request.args:
        with SessionLocal() as session:
            data = session.execute(select(Commande).where(Commande.codcde == request.args['id_cde'])).all()

            if data:
                return jsonify(ConvertToJson(data))
            else:
                return "Error: Aucune donnée avec cette ID"
    else:
        return jsonify({"Erreur": "Code client ou code commande non fournis"}), 404

@cde.route('/commande', methods=["POST"])
def ajouter_command():
    #Récuperation des donnée fourni au format JSON
    data = request.json

    #Création de la nouvelle commande
    nouvelle_commande = Commande(
        datcde=data['datcde'],
        codcli=data['codcli'],
        montant_total=data['montant_total'],
        code_utilisateur=data['code_utilisateur'],
        num_suivi=data['num_suivi'],
        datexp=data['datexp']
    )

    #Ouverture de la connexion à la base de donnée - fermeture automatique
    with SessionLocal() as session:
        session.add(nouvelle_commande)
        session.commit()

        id = session.execute(select(Commande.codcde).where(
            Commande.codcli == data['codcli'], Commande.datcde == data['datcde'])).scalar()

        #Redirection vers une page précise
        return redirect(f'/commande?id_cde={id}')

@cde.route('/commande', methods=["PUT"])
def update_command():
    #Récuperation des donnée fourni au format JSON
    data = request.json

    # Ouverture de la connexion à la base de donnée - fermeture automatique
    with SessionLocal() as session:
        commande = session.execute(select(Commande).where(Commande.codcde == request.args['id_cde'])).fetchall()

        if commande:
            if 'datexp' in data:
                commande[0][0].datexp = data['datexp']
            if 'num_suivi' in data:
                commande[0][0].num_suivi = data['num_suivi']

            session.commit()
            session.refresh(commande[0][0])

            return jsonify(ConvertToJson(commande))
        else:
            return jsonify({"Erreur": "Commande introuvable"}), 404

@cde.route('/commande', methods=["DELETE"])
def desactivate_commande():
    # Ouverture de la connexion à la base de donnée - fermeture automatique
    with SessionLocal() as session:
        commande = session.execute(select(Commande).where(Commande.codcde == request.args['id_cde'])).all()

        if commande:
            commande[0][0].est_actif = False
            session.commit()
            session.refresh(commande[0][0])

            return jsonify(ConvertToJson(commande))
        else:
            return jsonify({"Erreur": "Commande introuvable"}), 404