from flask import Flask, jsonify, request
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
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    } for cupcake in cupcakes]
    
    # import pdb; pdb.set_trace()

    return jsonify(response=serialized_cupcakes)


@app.route("/cupcakes", methods=["POST"])
def create_cupcake():
    """ create new cupcake"""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(
        flavor= flavor,
        size= size,
        rating= rating,
        image= image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized_new_cupcake= { 
        "id": new_cupcake.id,
        "flavor": new_cupcake.flavor,
        "size": new_cupcake.size,
        "rating": new_cupcake.rating,
        "image": new_cupcake.image}   

    return jsonify(response=serialized_new_cupcake)

