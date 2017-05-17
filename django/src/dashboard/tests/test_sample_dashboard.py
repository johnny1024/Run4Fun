from django.test import TestCase
# from django.contrib.auth.models import User
# import mock
# from django.test.client import RequestFactory
# from unittest.mock import Mock
# from dashboard import views


class TestDashboard(TestCase):
    def test_passing(self):
        self.assertEqual(1, 1)

    # def test_whole_ran_distance(self):
    #     user = User.objects.create_user(username='testUser', password='testPassword')
    #     user.save()
    #     user.workouts = [Mock(user=user, distance=1, done=True), Mock(user=user,distance=2, done=False),
        # Mock(user=user,distance=3, done=True)]
    #     user.save()
    #     self.assertEqual(views.whole_ran_distance(user), 4)
