from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Index, Numeric, Float
from sqlalchemy.orm import relationship
from database import Base, engine

# classes des différentes tables à créer

class Client(Base):
	__tablename__ = "t_client"

	codcli = Column(Integer, primary_key=True)
	nom = Column(String(40), default=None, index=True)
	prenom = Column(String(30), default=None)
	adresse = Column(String(50), default=None)
	cp = Column(String(5), default=None)
	ville = Column(String(50), default=None)
	genre = Column(String(8), default=None)
	email = Column(String(255), default=None)
	est_actif = Column(Boolean, default=True)

class Commande(Base):
	__tablename__ = "t_commande"

	codcde = Column(Integer,primary_key=True)
	datcde = Column(Date)
	codcli = Column(Integer,ForeignKey('t_client.codcli'))
	montant_total = Column(Float, default=0.0000)
	code_utilisateur = Column(Integer, ForeignKey('t_utilisateur.code_utilisateur'))
	num_suivi = Column(String(50), default=None)
	datexp = Column(Date)
	est_actif = Column(Boolean, default=True)

	__table_args__ = (Index('commmande_index', "codcli"),)
 
class CommObjet(Base):
	__tablename__ = "rel_commande_objet"

	codcde = Column(Integer, ForeignKey("t_commande.codcde"), primary_key=True)
	codobj = Column(Integer, ForeignKey("t_objet.codobj"), primary_key=True)
	codembal = Column(Integer)
	codmodele = Column(Integer)
	poids = Column(Numeric, default=0.0000)
	montant_affranchissement = Column(Float, default=0.0000)

class Objet(Base):
	__tablename__ = "t_objet"

	codobj = Column(Integer,primary_key=True)
	libobj = Column(String(50), default=None)
	poidsobj = Column(Numeric, default=0.0000)
	nb_points = Column(Integer, default=0)
	est_actif = Column(Boolean, default=True)
	condit = relationship("ObjetCond",back_populates='objets')

class ObjetCond(Base):
	__tablename__ = "rel_objet_conditionnement"

	idrelcond = Column(Integer,primary_key=True, index=True)
	codobj = Column(Integer, ForeignKey('t_objet.codobj'))
	codcond = Column(Integer, ForeignKey('t_conditionnement.idcondit'))
	objets = relationship("Objet",back_populates='condit')
	condit = relationship("Conditionnement",back_populates='objets')
 
class Conditionnement(Base):
    __tablename__ = "t_conditionnement"

    idcondit = Column(Integer,primary_key=True)
    libcondit = Column(String(50), default=None)
    poidscondit = Column(Integer)
    qte_min = Column(Integer)
    qte_max = Column(Integer)
    objets = relationship("ObjetCond",back_populates='condit')
    est_actif = Column(Boolean, default=True)

class Utilisateur(Base):
	__tablename__ = "t_utilisateur"

	code_utilisateur = Column(Integer,primary_key=True)
	nom_utilisateur = Column(String(50), default=None)
	prenom_utilisateur = Column(String(50), default=None)
	username = Column(String(50), default=None)
	date_insc_utilisateur = Column(Date)
	est_actif = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)