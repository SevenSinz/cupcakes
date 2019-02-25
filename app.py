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
    """ create new cupcake
    
    Sending the query inside the body of the post as:

    { "flavor": "strawberry",
    "size": "XXL",
    "rating": 1,
    "image": "cupcake4.com"}
    
    Expecting:
    {
        "response": {
        "flavor": "strawberry",
        "id": 2,
        "image": "cupcake4.com",
        "rating": 1.0,
        "size": "XXL"
        }
    }
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized_new_cupcake = { 
        "id": new_cupcake.id,
        "flavor": new_cupcake.flavor,
        "size": new_cupcake.size,
        "rating": new_cupcake.rating,
        "image": new_cupcake.image}   

    return jsonify(response=serialized_new_cupcake)


@app.route("/cupcakes/<int:cupcake_id>", methods=["GET", "PATCH"])
def patch_cupcake(cupcake_id):
    """ Handles cupcake patch for individual cupcake """

    patched_cupcake = Cupcake.query.get(cupcake_id)

    patched_cupcake.flavor = request.json["flavor"]
    patched_cupcake.size = request.json["size"]
    patched_cupcake.rating = request.json["rating"]
    patched_cupcake.image = request.json["image"]

    db.session.commit()

    serialized_patched_cupcake = {
        "id": patched_cupcake.id,
        "flavor": patched_cupcake.flavor,
        "size": patched_cupcake.size,
        "rating": patched_cupcake.rating,
        "image": patched_cupcake.image
        }

    return jsonify(response=serialized_patched_cupcake)


@app.route("/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """ Handles cupcake patch for individual cupcake """

    cupcake_to_delete = Cupcake.query.get(cupcake_id)
    db.session.delete(cupcake_to_delete)

    db.session.commit()

    response = {
        "message": "deleted"
        }

    return jsonify(response=response)
