from flask import Flask, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/cupcakes")
def display_cupcakes():
    """ display all existing cupcakes"""
    cupcakes = Cupcake.query.all()

    serialized_cupcakes = [{
        "flavor": cupcakes.flavor,
        "size": cupcakes.size,
        "rating": cupcakes.rating,
        "image": cupcakes.image,
    } for cupcake in cupcakes]

    return jsonify(response=serialized_cupcakes)

