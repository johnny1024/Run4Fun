from django.contrib.auth.models import User
from django.test import TestCase, Client


class TestingClass(TestCase):
    def test_user_logged(self):
        client = Client()
        User.objects.create_user(username='testUser', password='testingPassword')
        client.login(username='testUser', password='testingPassword')
        response = client.get(path='/')
        self.assertRedirects(response, '/dashboard/', status_code=302, target_status_code=302)

    def test_user_not_logged(self):
        client = Client()
        User.objects.create_user(username='testUser')
        response = client.get(path='/', follow=True)
        self.assertContains(response, 'run.jpg')
