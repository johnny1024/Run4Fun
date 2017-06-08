from unittest.mock import Mock
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client

from accounts import views


class TestDisplaySignup(TestCase):
    def test_get_signup(self):
        rf = RequestFactory()
        get_request = rf.get(path='/accountss/signup/')
        get_request.user = User.objects.create_user(username='testUser')
        get_request.resolver_match = Mock(url_name='signup')
        response = views.signup(get_request)
        self.assertEqual(response.status_code, 200)

    def test_post_signup(self):
        response = self.client.post(path='/accounts/signup/', data={
            'username': 'test',
            'password1': '99test99',
            'password2': '99test99',
        })

        self.assertEqual(response.status_code, 302)
        response.client = Client()
        self.assertRedirects(response, '/profile/', target_status_code=302)

    def test_post_signup_inconsistent_password(self):
        response = self.client.post(path='/accounts/signup/', data={
            'username': 'test',
            'password1': '99test99',
            'password2': '99test98',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue("The two password fields didn&#39;t match" in response.content.decode("utf-8"))

    def test_post_signup_too_similar_password(self):
        response = self.client.post(path='/accounts/signup/', data={
            'username': 'test',
            'password1': 'test',
            'password2': 'test',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue("The password is too similar to the username" in response.content.decode("utf-8"))
