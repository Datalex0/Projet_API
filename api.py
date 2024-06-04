from database import SessionLocal
import flask

app = flask.Flask(__name__)

app.config["DEBUG"] = True
#Affiche un message autre que bad gateway s'il y a une erreur dans l'appli


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
 
@app.route('/client', methods=['GET'])
def read_client():
    return ''' <p>test</p>'''

@app.route('/objet', methods=['GET'])
def objet():
    return

@app.route('/commande', methods=['GET'])
def commande():
    return

@app.route('/utilisateur', methods=['GET'])
def utilisateur():
    return
 


app.run()