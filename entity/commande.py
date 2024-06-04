from flask import Blueprint, request, jsonify, redirect
from database.database import SessionLocal
from database.models import Commande
from sqlalchemy import select, text

cmd = Blueprint('commande', __name__)

def ConvertToJson(data):
    commande = []
    for cmd in data:
        cmd_list = {}
        cmd_list['codcde'] = cmd[0]
        cmd_list['datcde'] = cmd[1]
        cmd_list['codcli'] = cmd[2]
        cmd_list['montant_total'] = cmd[3]
        cmd_list['code_utilisateur'] = cmd[4]
        cmd_list['num_suivi'] = cmd[5]
        cmd_list['datexp'] = cmd[6]
        commande.append(cmd_list)

    return commande


@cmd.route('/commande', methods=["GET"])
def afficher_commande():
    if 'id_cli' in request.args:
        with SessionLocal() as session:
            data = session.execute(text('SELECT * FROM t_commande WHERE codcli = '+request.args['id_cli'])).all()
            print(data)

            if data:
                return jsonify(ConvertToJson(data))
            else:
                return "Error: Aucune donnée avec cette ID"

    elif 'id_cde' in request.args:
        with SessionLocal() as session:
            data = session.execute(text('SELECT * FROM t_commande WHERE codcde = '+request.args['id_cde'])).all()

            if data:
                return jsonify(ConvertToJson(data))
            else:
                return "Error: Aucune donnée avec cette ID"
    else:
        return 'ok'

@cmd.route('/commande', methods=["POST"])
def ajouter_command():
    if request.method == 'POST':
        data = request.json

        nouvelle_commande = Commande(
            datcde=data['datcde'],
            codcli=data['codcli'],
            montant_total=data['montant_total'],
            code_utilisateur=data['code_utilisateur'],
            num_suivi=data['num_suivi'],
            datexp=data['datexp']
        )

        with SessionLocal() as session:
            session.add(nouvelle_commande)
            session.commit()

            id = session.execute(select(Commande.codcde).where(
                Commande.codcli == data['codcli'], Commande.datcde == data['datcde'])).scalar()

            return redirect(f'/commande?id_cde={id}')