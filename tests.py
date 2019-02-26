from app import app
from models import db, connect_db, Cupcake, DEFAULT_CUPCAKE_IMG
import unittest

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes-app-test'
db.create_all()


class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client and make new cupcake."""

        Cupcake.query.delete()

        self.client = app.test_client()

        new_cupcake = Cupcake(
            flavor='testing', size='small', rating=10, image='image.com', id=10000)
        db.session.add(new_cupcake)
        db.session.commit()

    def test_all_cupcakes(self):
        """/cupcakes should show all cupcakes"""
        response = self.client.get("/cupcakes")
        response_data = response.json['response']
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['flavor'], 'testing')
        self.assertEqual(response_data[0]['size'], 'small')
        self.assertEqual(response_data[0]['rating'], 10)
        self.assertEqual(response_data[0]['image'], 'image.com')
        self.assertEqual(response.status_code, 200)
        # end test_all
    

    # def test_get_single_cupcake(self):
    #     """/cupcake/[cupcake-id] returns info about cupcakeid = 10000"""
    #     response = self.client.get("/cupcakes/10000")
    #     self.assertEqual(response.json['response']['flavor'], 'testing')
    #     self.assertEqual(response.json['response']['size'], 'small')
    #     self.assertEqual(response.json['response']['rating'], 10)
    #     self.assertEqual(response.status_code, 200)


    def test_post_cupcake(self):
        """add new cupcake on /cupcakes """        
        response = self.client.post(
            "/cupcakes",
            json={ 'flavor': 'newFlavor',
                    'size': 'sizable',
                    'rating': 7,
                    'image': 'cupcake.com'
                  })

        self.assertEqual(response.json['response']['flavor'], 'newFlavor')
        self.assertEqual(response.json['response']['size'], 'sizable')
        self.assertEqual(response.json['response']['rating'], 7)
        self.assertEqual(response.json['response']['image'], 'cupcake.com')
        self.assertEqual(response.status_code, 200)   


    def test_patch_cupcake(self):
        """/cupcakes/1000 patch cupcakeid=10000"""
        # route is copied from the @app.route, 
        # except id is updated to the testid
        # below is json answer, copy from the body on insomnia
        response = self.client.patch(
            "/cupcakes/10000",
            json={'flavor': 'patching',
                  'size': 'smallpatch',
                  'rating': 6,
                  })
        # check and make sure your json[response] is accurate

        self.assertEqual(response.json['response'], { 'id': 10000,
                                                     'flavor': 'patching',
                                                     'size': 'smallpatch',
                                                     'rating': 6,
                                                     'image': DEFAULT_CUPCAKE_IMG})

        self.assertEqual(response.status_code, 200)
        # below is replaced with above, cause python can compare dicts directly,
        # and if a new argument is added to the {} test will fail, so we know to 
        # # test for it
        # self.assertEqual(response.json['response']['flavor'], 'patching')
        # self.assertEqual(response.json['response']['size'], 'smallpatch')
        # self.assertEqual(response.json['response']['rating'], 6)
        # self.assertEqual(response.json['response']['image'], DEFAULT_CUPCAKE_IMG)

    def delete_cupcake(self):
        """/cupcakes/10000 delete cupcakeid=10000"""
        response = self.client.delete("/cupcakes/10000")

        self.assertEqual(response.json['response']['message'], 'deleted')
        self.assertEqual(response.status_code, 200)
