from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Collection, Movie

User = get_user_model()

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        
        # Create sample data
        self.collection = Collection.objects.create(user=self.user, title="Test Collection", description="Test Description")
        self.movie = Movie.objects.create(title="Test Movie", genres="Action, Comedy")
        self.collection.movies.add(self.movie)
    

    def test_register_view(self):
        response = self.client.post('/register/', {'username': 'newuser', 'password': 'newpassword'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.json())


    def test_collection_list_get(self):
        response = self.client.get('/collection/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('collections', response.json()['data'])
        self.assertIn('favourite_genres', response.json()['data'])
        self.assertIsInstance(response.json()['data']['collections'], list)


    def test_collection_list_post(self):
        response = self.client.post('/collection/', {'title': 'New Collection', 'description': 'New Description'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('collection_uuid', response.json())


    def test_edit_collection_get(self):
        response = self.client.get(f'/collection/{self.collection.uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], self.collection.title)


    def test_edit_collection_put(self):
        response = self.client.put(f'/collection/{self.collection.uuid}/', {'title': 'Updated Title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['collection_uuid'], str(self.collection.uuid))
        self.collection.refresh_from_db()
        self.assertEqual(self.collection.title, 'Updated Title')


    def test_get_request_count(self):
        request_count = 10
        cache.set('request_count', request_count)
        response = self.client.get('/request-count/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # +1 because getting number of requests will increment number of processed requests
        self.assertEqual(response.json(), {'requests': request_count+1})


    def test_reset_request_count(self):
        request_count = 20
        cache.set('request_count', request_count)
        response = self.client.post('/request-count/reset/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'request count reset successfully'})
        self.assertEqual(cache.get('request_count'), 0)
