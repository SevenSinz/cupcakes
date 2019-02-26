"""Models for Cupcakes app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_CUPCAKE_IMG = "https://tinyurl.com/truffle-cupcake"

class Cupcake(db.Model):
    """Cupcake."""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    # do we need size? String?
    flavor = db.Column(db.Text,
                       nullable=False)
    size = db.Column(db.Text,
                     nullable=False)
    rating = db.Column(db.Float,
                       nullable=False)
    image = db.Column(db.String(600),
                      default=DEFAULT_CUPCAKE_IMG)


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)                            