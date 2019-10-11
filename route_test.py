from app import app
from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId

user_id_test = '5d55cffc4a3d4031f42827a2'
user_test = {'_id': ObjectId('5d55cffc4a3d4031f42827a2'), 'user_email': 'test@test.com', 'user_name': 'Ted', 'user_password': 'Password', 'user_is_admin': True, 'inventory': None}
inventory_test = {'_id': ObjectId('5d55cffc4a3d4031f42827a4'), 'user_id': ObjectId('5d55cffc4a3d4031f42827a2')}


item_test = {
    '_id': ObjectId('5d55cffc4a3d4031f42827a3'),
    'name': 'Eggs',
    'description': 'Goose eggs',
    'image': 'noimage',
    'inventory': ObjectId('5d55cffc4a3d4031f42827a4'),
    'price': '5.00',
    'seller': 'Ted'
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
    'user_id': ObjectId('5d55cffc4a3d4031f42827a2')
}
sample_create = {
    'user_email': 'test@test.com',
    'user_name': 'Ted',
    'user_password': 'Password'

}
sample_login = {
    'user_name': 'Ted',
    'user_password': 'Password'

}
sample_search = {
    'user_id': ObjectId('5d55cffc4a3d4031f42827a2'),
    'search': 'Eggs'

}
sample_account = {
    'user_id': ObjectId('5d55cffc4a3d4031f42827a2')


}
sample_create_item = {
    'user_id': ObjectId('5d55cffc4a3d4031f42827a2'),
    'add': True,
    'name': 'Eggs',
    'description': 'Goose eggs',
    'image': 'noimage',
    'inventory': ObjectId('5d55cffc4a3d4031f42827a4'),
    'price': '5.00',
    'seller': 'Ted'
}


class AppTests(TestCase):
    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home_status_code(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 302)

    def test_login(self):
        one = self.client.get('/user_login')
        self.assertEqual(one.status_code, 200)

    def test_user_new(self):
        result = self.client.get('/user_login/create')
        self.assertEqual(result.status_code, 200)
        '''
    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_user_create(self, mock_insert):
        result = self.client.post('/user_login/create', data=sample_create)
        self.assertEqual(result.status_code, 302)
        mock_insert.assert_called_with(user_test)
        '''
        '''
    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_admin_item_create(self, mock_insert):
        result = self.client.post('/admin/inventory', data=sample_create_item)
        self.assertEqual(result.status_code, 302)
        '''
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_user_home_page_login(self, mock_find):
        """Test showing a single playlist."""
        mock_find.return_value = user_test

        result = self.client.post('/', data=sample_login)
        self.assertEqual(result.status, '302 FOUND')

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_admin_add_item(self, mock_find):
        """Test showing a single playlist."""
        mock_find.return_value = user_test

        result = self.client.post('/admin/add/item', data=sample_account)
        self.assertEqual(result.status, '200 OK')

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_user_account(self, mock_find):
        """Test showing a single playlist."""
        mock_find.return_value = user_test

        result = self.client.post('/user/account', data=sample_account)
        self.assertEqual(result.status, '200 OK')

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_admin_edit_item(self, mock_find):
        """Test showing a single playlist."""
        mock_find.return_value = user_test

        result = self.client.post('/admin/edit/item', data=sample_account)
        self.assertEqual(result.status, '200 OK')
        '''
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_admin_accounts(self, mock_find):
        """Test showing a single playlist."""
        mock_find.return_value = user_test

        result = self.client.post('/admin/accounts', data=sample_account)
        self.assertEqual(result.status, '200 OK')


    @mock.patch('pymongo.collection.Collection.find_one')
    def test_user_cart(self, mock_find):
        """Test showing a single playlist."""
        mock_find.return_value = cart_item_test

        result = self.client.post('/user/cart', data=sample_account)
        self.assertEqual(result.status, '200 OK')
        '''
        '''
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_admin_accounts(self, mock_find):
        """Test showing a single playlist."""
        mock_find.return_value = user_test

        result = self.client.post('/admin/accounts', data=sample_account)
        self.assertEqual(result.status, '200 OK')

    def test_search(self):
        """Test showing a single playlist."""

        result = self.client.post('/search', data=sample_search)
        self.assertEqual(result.status, '302 FOUND')


    @mock.patch('pymongo.collection.Collection.find_one')
    def test_user_home_page(self, mock_find):
        """Test showing a single playlist."""
        mock_find.return_value = user_test

        result = self.client.post('/', data=sample_account)
        self.assertEqual(result.status, '302 FOUND')
        '''
        '''
    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_user_account_delete(self, mock_delete):
        """Test showing a single playlist."""

        result = self.client.get(f'/{user_id_test}/delete')
        self.assertEqual(result.status, '200 OK')
        mock_delete.assert_called_with({'_id': user_id_test})
        '''


if __name__ == '__main__':
    unittest_main()
