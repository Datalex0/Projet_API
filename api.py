from flask import Flask, render_template

from entity.client import clients
from entity.commande import cde

app = Flask(__name__)
app.config["DEBUG"] = True

app.register_blueprint(clients)
app.register_blueprint(cde)

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")

app.run()