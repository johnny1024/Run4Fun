from django.test import TestCase
# from django.contrib.auth.models import User
# import mock
# from django.test.client import RequestFactory
# from unittest.mock import Mock
from dashboard import views


class TestDashboard(TestCase):
    def test_get_temperature(self):
        self.assertTrue(-50 <= views.get_temperature() <= 50)
