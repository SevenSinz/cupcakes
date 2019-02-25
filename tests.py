from app import app
from models import db, connect_db, Cupcake
import unittest

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes-app-test'
db.create_all()


class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client and make new cupcake."""

        Cupcake.query.delete()

        self.client = app.test_client()

        new_cupcake = Cupcake(
            flavor='testing', size='small', rating=10, id=10000)
        db.session.add(new_cupcake)
        db.session.commit()
