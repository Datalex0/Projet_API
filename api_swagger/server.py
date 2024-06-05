from flask import Flask, render_template, request, jsonify
import connexion
from database import SessionLocal,init_db
from models import Client, Commande, CommObjet, Objet, Conditionnement, Utilisateur
import yaml


# Connexion à l'API Swagger : http://localhost:5000/api/ui/

# Initialize the database
init_db()

# Create the application instance
app = connexion.App(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('config.yml')

# Initialize database session
db = SessionLocal()

# CRUD operations for Client
def create_client():
    client_data = request.get_json()
    client = Client(**client_data)
    db.add(client)
    db.commit()
    return jsonify(client_data), 201

def get_clients():
    clients = db.query(Client).all()
    return jsonify([client.__dict__ for client in clients])

def update_client(codcli):
    client_data = request.get_json()
    client = db.query(Client).filter(Client.codcli == codcli).first()
    if client:
        for key, value in client_data.items():
            setattr(client, key, value)
        db.commit()
    return jsonify(client_data)

def delete_client(codcli):
    client = db.query(Client).filter(Client.codcli == codcli).first()
    if client:
        client.est_actif = False
        db.commit()
    return '', 204

# CRUD operations for Commande
def create_order():
    order_data = request.get_json()
    order = Commande(**order_data)
    db.add(order)
    db.commit()
    return jsonify(order_data), 201

def get_orders():
    orders = db.query(Commande).all()
    return jsonify([order.__dict__ for order in orders])

def update_order(codcde):
    order_data = request.get_json()
    order = db.query(Commande).filter(Commande.codcde == codcde).first()
    if order:
        for key, value in order_data.items():
            setattr(order, key, value)
        db.commit()
    return jsonify(order_data)

def delete_order(codcde):
    order = db.query(Commande).filter(Commande.codcde == codcde).first()
    if order:
        order.est_actif = False
        db.commit()
    return '', 204

# CRUD operations for Objet
def create_object():
    object_data = request.get_json()
    obj = Objet(**object_data)
    db.add(obj)
    db.commit()
    return jsonify(object_data), 201

def get_objects():
    objects = db.query(Objet).all()
    return jsonify([obj.__dict__ for obj in objects])

def update_object(codobj):
    object_data = request.get_json()
    obj = db.query(Objet).filter(Objet.codobj == codobj).first()
    if obj:
        for key, value in object_data.items():
            setattr(obj, key, value)
        db.commit()
    return jsonify(object_data)

def delete_object(codobj):
    obj = db.query(Objet).filter(Objet.codobj == codobj).first()
    if obj:
        obj.est_actif = False
        db.commit()
    return '', 204

# CRUD operations for Utilisateur
def create_user():
    user_data = request.get_json()
    user = Utilisateur(**user_data)
    db.add(user)
    db.commit()
    return jsonify(user_data), 201

def get_users():
    users = db.query(Utilisateur).all()
    return jsonify([user.__dict__ for user in users])

def update_user(code_utilisateur):
    user_data = request.get_json()
    user = db.query(Utilisateur).filter(Utilisateur.code_utilisateur == code_utilisateur).first()
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        db.commit()
    return jsonify(user_data)

def delete_user(code_utilisateur):
    user = db.query(Utilisateur).filter(Utilisateur.code_utilisateur == code_utilisateur).first()
    if user:
        user.est_actif = False
        db.commit()
    return '', 204

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)