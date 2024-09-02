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

        # Verify the access token is not empty
        self.assertNotEqual(access_token, '')

        # Decode the token to verify its payload
        decoded_payload = refresh.access_token.payload
        self.assertEqual(decoded_payload['user_id'], self.user.id)