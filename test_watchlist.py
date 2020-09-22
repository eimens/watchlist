import unittest
from app import Cuser, Movie, app, db

class WatchListTestCase(unittest.TestCase):
    
    def setUp(self):
        app.config.update(
            TESTING = True,
            SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        )

        db.create_all()
        user = Cuser(name='Test', user_name='Test')
        user.set_password('123')
        movie = Movie(title='Test Movie Title', year='2020')
        db.session.add_all([user, movie])
        db.session.commit()

        self.client = app.test_client()
        self.runner = app.test_cli_runner()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app_exist(self):
        self.assertIsNotNone(app)

    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    def test_404_page(self):
        respone = self.client.get('/nothing')
        data = respone.get_data(as_text=True)
        self.assertIn('Page Not Found - 404', data)
        self.assertIn('Go Back', data)
        self.assertEqual(respone.status_code, 200)

    def test_index_page(self):
        respone = self.client.get('/')
        data = respone.get_data(as_text=True)
        self.assertIn('Test\'s Watchlist', data)
        self.assertIn('Test Movie Title', data)
        self.assertEqual(respone.status_code, 200)

    def login(self):
        self.client.post('/login', data=dict(
            username = 'Test',
            password = '123'
        ), follow_redirects=True)
    
    def test_create_item(self):
        self.login()

        respone = self.client.post('/', data=dict(
            title='New Movie',
            year='2019'
        ), follow_redirects=True)
        data = respone.get_data(as_text=True)
        self.assertIn('Item create.', data)
        self.assertIn('New Movie', data)

        respone = self.client.post('/', data=dict(
            title='',
            year='2019'
        ), follow_redirects=True)
        data = respone.get_data(as_text=True)
        self.assertNotIn('Item created.', data)
        self.assertIn('Invalid input.', data)

        respone = self.client.post('/', data=dict(
            title='New Movie',
            year=''
        ), follow_redirects=True)
        data = respone.get_data(as_text=True)
        self.assertNotIn('Item created.', data)
        self.assertIn('Invalid input.', data)

    def test_update_item(self):
        self.login()

        respone = self.client.get('/movie/edit/1')
        data = respone.get_data(as_text=True)
        self.assertIn("Edit item", data)
        self.assertIn('Test Movie Title', data)
        self.assertIn('2020', data)

        respone = self.client.post('/movie/edit/1', data=dict(
            title = 'New Movie Edited',
            Year = '2019'
        ), follow_redirects=True)
        data = respone.get_data(as_text=True)
        self.assertIn('Item update', data)
        self.assertIn('New Movie Edited', data)

        respone = self.client.post('/movie/edit/1', data=dict(
            title = '',
            Year = '2020'
        ), follow_redirects=True)
        data = respone.get_data(as_text=True)
        self.assertNotIn('Item update', data)
        self.assertIn('Invalid input', data)

        respone = self.client.post('/movie/edit/1', data=dict(
            title = 'New Movie Edited again',
            Year = ''
        ), follow_redirects=True)
        data = respone.get_data(as_text=True)
        self.assertNotIn('Item update', data)
        self.assertIn('Invalid input', data)

    def test_delete_item(self):
        self.login()

        respone = self.client.post('/movie/delete/1', follow_redirects=True)
        data = respone.get_data(as_text=True)

        self.assertIn('Item deleted', data)
        self.assertNotIn('Test Movie Title', data)       

    def test_login_protect(self):
        respone = self.client.get('/')
        data = respone.get_data(as_text=True)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Setting', data)
        self.assertNotIn('<form method="post">', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Edit', data)

    def test_login(self):
        respone = self.client.post('/login', data=dict(
            username = 'Test',
            password = '123'
        ), follow_redirects=True)
        data = respone.get_data(as_text=True)
        self.assertIn('Login success.', data)
        self.assertIn('Setting', data)
        self.assertIn('Logout', data)
        self.assertIn('<form method="post">', data)
        self.assertIn('Delete', data)
        self.assertIn('Edit', data)

        respone = self.client.post('/login', data=dict(
            username = 'test',
            password = '1234'
        ), follow_redirects=True)
        data = respone.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Inavlid username or password.', data) 

    def test_logout(self):
        self.login()

        respone = self.client.get('/logout', follow_redirects=True)
        data = respone.get_data(as_text=True)
        self.assertIn('Good bye.', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Setting', data)
        self.assertNotIn('<form method="post">', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Edit', data)

    def test_settings(self):
        self.login()

        respone = self.client.get('/settings')
        data = respone.get_data(as_text=True)
        self.assertIn('Settings', data)
        self.assertIn('Your name', data)

        respone = self.client.post('/settings', data=dict(
            name='Grey LI'
        ),follow_redirects=True)
        data = respone.get_data(as_text=True)
        self.assertIn('Setting update.', data)
        self.assertIn('Grey LI', data)

        respone = self.client.post('/settings', data=dict(
            name=''
        ),follow_redirects=True)
        data = respone.get_data(as_text=True)
        self.assertNotIn('Setting update.', data)
        self.assertIn('Invalid input.', data)

if __name__ == '__main__':
    unittest.main()
