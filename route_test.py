from app import app
from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId

inventory_test = {'_id': ObjectId('5d55cffc4a3d4031f42827a4'), 'user_id': ObjectId('5d55cffc4a3d4031f42827a2')}

user_test = {
    '_id': ObjectId('5d55cffc4a3d4031f42827a2'),
    'user_email': 'test@test.com',
    'user_name': 'Ted',
    'user_password': 'Password',
    'user_is_admin': True,
    'inventory': ObjectId(inventory_test['_id'])
}


item_test = {
    '_id': ObjectId('5d55cffc4a3d4031f42827a3'),
    'name': 'Eggs',
    'description': 'Goose eggs',
    'image': 'noimage',
    'inventory': ObjectId(inventory_test['_id']),
    'price': '5.00',
    'seller': user_test['user_name']
}
cart_item_test = {
    '_id': ObjectId('5d55cffc4a3d4031f42827a1'),
    'name': item_test['name'],
    'description': item_test['description'],
    'amount': 1,
    'image': item_test['image'],
    'price': item_test['price'],
    'seller': item_test['seller'],
    'item_id': ObjectId(item_test['_id']),
    'user_id': ObjectId(user_test['_id'])
}
sample_login = {
    'user_name': user_test['user_name'],
    'user_password': user_test['user_password']

}


class AppTests(TestCase):
    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    # This runs implicitly before any tests are run
    # We use this to set up our app before we test on it
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 302)

    def test_login(self):
        one = self.app.get('/user_login')
        self.assertEqual(one.status_code, 200)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_playlist(self, mock_insert):
        """Test submitting a new playlist."""
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        result = self.client.post('/', data=sample_login)

        # After submitting, should redirect to that playlist's page
        self.assertEqual(result.status, '302 FOUND')
