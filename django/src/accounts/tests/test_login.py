from django.contrib.auth.models import User
from django.test import TestCase, Client


class TestLoginDisplay(TestCase):
    def test_get_login_not_logged(self):
        response = self.client.get(path='/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_get_login_logged_no_profile_info(self):
        client = Client()
        User.objects.create_user(username='testUser', password='testingPassword')
        client.login(username='testUser', password='testingPassword')
        response = client.get(path='/accounts/login/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Please fill your profile information before accessing the site.' in
                        response.content.decode("utf-8"))

    def test_get_login_logged_with_profile_info(self):
        client = Client()
        user = User.objects.create_user(username='testUser', password='testingPassword')
        user.profile.age = 25
        user.profile.sex = 'K'
        user.profile.weight = 60
        user.save()
        client.login(username='testUser', password='testingPassword')
        response = client.get(path='/accounts/login/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Please fill your profile information before accessing the site.' not in
                        response.content.decode("utf-8"))


class TestLoginFunctionality(TestCase):
    def test_post_login_wrong_credentials(self):
        response = self.client.post(path='/accounts/login/', data={
            'username': 'test',
            'password': 'test',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Please enter a correct username and password." in response.content.decode("utf-8"))

    def test_post_login_right_credentials(self):
        User.objects.create_user(username='testUser', password='testingPassword')
        response = self.client.post(path='/accounts/signup/', data={
            'username': 'testingUser',
            'password': 'testingPassword',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Please enter a correct username and password." not in response.content.decode("utf-8"))
