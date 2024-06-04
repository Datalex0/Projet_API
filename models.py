from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Index, Numeric, Float,MetaData

from sqlalchemy.orm import relationship

from database import Base, engine, SessionLocal

import flask
from flask import request, jsonify

# Justine - 12122022 -  V1
# classe permettant de définir les modèles de la base de données pour créer ou accéder aux tables
# hérite de la base définie dans database.py

class Client(db.Model):
    __tablename__ = "client"

    CodeCli = Column(Integer, primary_key=True)
    Nom = Column(String(40), default=None, index=True)
    Prenom = Column(String(30), default=None)
    Adresse = Column(String(50), default=None)
    IdCodePostal = Column(Integer, default=None)
    Genre = Column(String(8), default=None)
    Email = Column(String(255), default=None)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class Article(db.Model):
    __tablename__ = "article"

    CodeArticle = Column(Integer, primary_key=True)
    Designation = Column(String(50), default=None)
    Poids = Column(Numeric, default=0.0000)
    NbreDePoints = Column(Integer, default=0)


class ObjetCond(Base):
	__tablename__ = "t_rel_cond"

	idrelcond = Column(Integer, primary_key=True, index=True)
	qteobjdeb = Column(Integer, default=0)
	qteobjfin = Column(Integer, default=0)
	codobj = Column(Integer, ForeignKey('t_objet.codobj'))
	codcond = Column(Integer, ForeignKey('t_conditionnement.idcondit'))
	objets = relationship("Article",back_populates='condit')
	condit = relationship("Conditionnement",back_populates='article')

class Conditionnement(Base):
	__tablename__ = "t_conditionnement"

	idcondit = Column(Integer,primary_key=True)
	libcondit = Column(String(50), default=None)
	poidscondit = Column(Integer)
	prixcond = Column(Numeric, default=0.0000)
	ordreimp = Column(Integer)
	codobj = Column(Integer, ForeignKey('t_objet.codobj'))
	objets = relationship("ObjetCond",back_populates='condit')

class Commande(db.Model):
    __tablename__ = "commande"

    NumCde = Column(Integer, primary_key=True)
    CodeClient = Column(Integer, ForeignKey("client.CodeCli"))
    DateCde = Column(Date)
    MtTotal = Column(Float)
    CodeOperateur = Column(Integer)
    NSuivi = Column(String(50), default=None)
    DateExpedition = Column(Date)

class CommandeArticle(db.Model):
    __tablename__ = "commande_article"

    NumCde = Column(Integer, ForeignKey("commande.NumCde"), primary_key=True)
    CodeArticle = Column(Integer, ForeignKey("article.CodeArticle"), primary_key=True)
    CodeEmballage = Column(Integer)
    CodeModele = Column(Integer)
    Poids = Column(Numeric, default=0.0000)
    MontantAffranchissement = Column(Float, default=0.0000)

class Utilisateur(db.Model):
    __tablename__ = "utilisateur"

    code_utilisateur = Column(Integer, primary_key=True)
    nom_utilisateur = Column(String(50), default=None)
    prenom_utilisateur = Column(String(50), default=None)
    username = Column(String(50), default=None)
    couleur_fond_utilisateur = Column(Integer, default=0)
    date_insc_utilisateur = Column(Date)



Base.metadata.create_all(bind=engine)


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
        tailleobj=data["tailleobj"],
        puobj=data["puobj"],
        poidsobj=data["poidsobj"],
        indispobj=data["indispobj"],
        o_imp=data["o_imp"],
        o_aff=data["o_aff"],
        o_cartp=data["o_cartp"],
        points=data["points"],
        o_ordre_aff=data["o_ordre_aff"],
        condit=data["condit"]
    )

    # Ajouter le client à la session
    session.add(nouvelobjet)
    session.commit()  # Valider la transaction
    session.refresh(nouvelobjet)
    # print("{prenomcli} {nomcli} ajouté avec succès")
    return jsonify({
        "codobj": nouvelobjet.codobj,
        "libobj": nouvelobjet.libobj,
        "tailleobj": nouvelobjet.tailleobj,
        "puobj": nouvelobjet.puobj,
        "poidsobj": nouvelobjet.poidsobj,
        "indispobj": nouvelobjet.indispobj,
        "o_imp": nouvelobjet.o_imp,
        "o_aff": nouvelobjet.o_aff,
        "o_cartp": nouvelobjet.o_cartp,
        "points": nouvelobjet.points,
        "o_ordre_aff": nouvelobjet.o_ordre_aff,
        "condit": nouvelobjet.condit,
    }), 201

if __name__ == "__main__":
    app.run(debug=True)

# @app.route('/objet/suppr', methods=['GET'])
# def suppr_objet():
#     data = request.json
#     supprimer
#     return 

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





