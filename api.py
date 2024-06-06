from flask import Flask, render_template

from entities.client import client
from entities.commande import cde
from entities.conditionnement import cond
from entities.utilisateur import user
from entities.objet import objet

app = Flask(__name__)
app.config["DEBUG"] = True

app.register_blueprint(client)
app.register_blueprint(cde)
app.register_blueprint(cond)
app.register_blueprint(user)
app.register_blueprint(objet)

app.run()