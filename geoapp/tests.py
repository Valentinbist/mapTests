from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.management import call_command
import json
from geoapp.models import FeatureCollection

class JWTGenerationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
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



# test the filter functionality (currently only bbox)
class FilterTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Generate JWT for the test user
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.refreshToken = refresh
        self.accessToken = access_token
        call_command('load_geojson')

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
        self.client = APIClient()
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Generate JWT for the test user
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.refreshToken = refresh
        self.accessToken = access_token

        # Use the token to authenticate a request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.accessToken}')
        feature_collection = FeatureCollection.objects.create(name='Test Collection', crs='EPSG:4326')

        json_to_add = {
            "feature_collection": feature_collection.id,
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [5.5, 53.2],
                            [5.6, 53.2],
                            [5.6, 53.3],
                            [5.5, 53.3],
                            [5.5, 53.2]
                        ]
                    ]
                ]
            },
            "properties": {
                "name": "Test Feature"
            },
            "type": "Feature",
        }

        json_to_add = json.dumps(json_to_add)
        response = self.client.post("/geo/features/", json_to_add, content_type="application/json")

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
        self.assertEqual(data['geometry']['coordinates'], [
                    [
                        [
                            [5.5, 53.2],
                            [5.6, 53.2],
                            [5.6, 53.3],
                            [5.5, 53.3],
                            [5.5, 53.2]
                        ]
                    ]
                ])
        self.assertEqual(data['properties']['name'], 'Test Feature')

    # test the updater
    def test_update(self):
        # Use the token to authenticate a request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.accessToken}')
        response = self.client.patch(f'/geo/features/{self.feature_id}/', json.dumps({
            'properties': {
                'name': 'Updated Test Feature'
            }
        }), content_type='application/json')

        # Verify the request was successful
        self.assertEqual(response.status_code, 200)
        # Verify the response contains the expected data
        data = response.json()
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


# this is more some kind of prove of concept of testing then atually testing... But I would do it like this