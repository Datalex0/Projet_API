
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# connexion a la base de donnée et déclaration de la base avec sql alchemy

# url de connexion de la base
SQLALCHEMY_DATABASE_URL = "mysql://root:Motdepasse001!!@localhost/digicheese"


# permet de définir les paramètre de connexion à la base
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# déclaration d'une base qui permet après de créer un modele et de mapper avec sql alchemy
Base = declarative_base()

# creation d'une session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

with SessionLocal() as session:
    print("connexion reussie")
    # session.close()
    # print("connexion fermée")