from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class JWTGenerationTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_jwt_generation(self):
        # Generate JWT for the test user
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.refreshToken = refresh
        self.accessToken = access_token

        # Verify the access token is not empty
        self.assertNotEqual(access_token, '')

        # Decode the token to verify its payload
        decoded_payload = refresh.access_token.payload
        self.assertEqual(decoded_payload['user_id'], self.user.id)

    # use the token to authenticate a request
    def test_jwt_authentication(self):
        # Use the token to authenticate a request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.accessToken}')
        response = self.client.get('/geo/features/')

        # Verify the request was successful
        self.assertEqual(response.status_code, 200)



# test the filter functionality
class FilterTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Generate JWT for the test user
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.refreshToken = refresh
        self.accessToken = access_token

    def test_filter(self):
        # Use the token to authenticate a request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.accessToken}')
        response = self.client.get('/geo/features/?bbox=5.54,53.2,6.55,53.21')

        # Verify the request was successful
        self.assertEqual(response.status_code, 200)

        # Verify the response contains the expected data
        data = response.json()
        results = data['results']
        self.assertEqual(len(results), 7)
        for feature in results:
            self.assertTrue(5.54 <= feature['geometry']['coordinates'][0] <= 6.55)
            self.assertTrue(53.2 <= feature['geometry']['coordinates'][1] <= 53.21)
            # check the names in the properties
            self.assertTrue('name' in feature['properties'])
            self.assertTrue(feature['properties']['name'] in ["Groningen","Achtkarspelen","Leeuwarden","Tytsjerksteradiel","Noordenveld","Waadhoeke","Westerkwartier"])

        # Verify the response contains the expected pagination data
        self.assertTrue('count' in data)
        self.assertTrue('next' in data)
        self.assertTrue('previous' in data)

# test the CRUD functionality on the properties
class CRUDTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Generate JWT for the test user
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.refreshToken = refresh
        self.accessToken = access_token

    def test_create(self):
        # Use the token to authenticate a request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.accessToken}')
        response = self.client.post('/geo/features/', {
            'geometry': {
                'type': 'Point',
                'coordinates': [5.5, 53.2]
            },
            'properties': {
                'name': 'Test Feature'
            }
        }, content_type='application/json')

        # Verify the request was successful
        self.assertEqual(response.status_code, 201)
        # get the id of the created feature
        self.feature_id = response.json()['id']

    # test the getter
    def test_read(self):
        # Use the token to authenticate a request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.accessToken}')
        response = self.client.get(f'/geo/features/{self.feature_id}/')

        # Verify the request was successful
        self.assertEqual(response.status_code, 200)
        # Verify the response contains the expected data
        data = response.json()
        self.assertEqual(data['geometry']['coordinates'], [5.5, 53.2])
        self.assertEqual(data['properties']['name'], 'Test Feature')

    # test the updater
    def test_update(self):
        # Use the token to authenticate a request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.accessToken}')
        response = self.client.put(f'/geo/features/{self.feature_id}/', {
            'geometry': {
                'type': 'Point',
                'coordinates': [5.6, 53.3]
            },
            'properties': {
                'name': 'Updated Test Feature'
            }
        }, content_type='application/json')

        # Verify the request was successful
        self.assertEqual(response.status_code, 200)
        # Verify the response contains the expected data
        data = response.json()
        self.assertEqual(data['geometry']['coordinates'], [5.6, 53.3])
        self.assertEqual(data['properties']['name'], 'Updated Test Feature')

    # test the deleter
    def test_delete(self):
        # Use the token to authenticate a request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.accessToken}')
        response = self.client.delete(f'/geo/features/{self.feature_id}/')

        # Verify the request was successful
        self.assertEqual(response.status_code, 204)
        # Verify the feature was deleted
        response = self.client.get(f'/geo/features/{self.feature_id}/')
        self.assertEqual(response.status_code, 404)
