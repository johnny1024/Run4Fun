from unittest.mock import Mock
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, SimpleTestCase

from accounts import views


class TestDisplayProfile(SimpleTestCase):
    def test_get_profile(self):
        rf = RequestFactory()
        get_request = rf.get(path='/profile/')
        # get_request.user = User.objects.create_user(username='testUser')
        get_request.user = Mock(username='testUser')
        resolver_match_mock = Mock(url_name='/profile')
        get_request.resolver_match = resolver_match_mock
        response = views.profile(get_request)
        self.assertEqual(response.status_code, 200)


class TestUpdateProfile(SimpleTestCase):
    def test_edit_profile_with_data(self):
        rf = RequestFactory()
        post_request = rf.post(path='/profile/', data={'age': 12, 'weight': 48})
        # post_request.user = User.objects.create_user(username='testUser')
        post_request.user = Mock(username='testUser')
        resolver_match_mock = Mock(url_name='/profile')
        post_request.resolver_match = resolver_match_mock
        response = views.profile(post_request)
        self.assertEqual(response.status_code, 200)
