from unittest.mock import Mock
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client

# from accounts import views
from workout_calendar import views as wc_views

from accounts import views


class TestDisplayProfile(TestCase):
    def test_get_profile(self):
        rf = RequestFactory()
        get_request = rf.get(path='/profile/')
        get_request.user = User.objects.create_user(username='testUser')
        resolver_match_mock = Mock(url_name='/profile')
        get_request.resolver_match = resolver_match_mock
        response = views.profile(get_request)
        self.assertEqual(response.status_code, 200)


class TestUpdateProfile(TestCase):
    def test_edit_profile_with_data(self):
        rf = RequestFactory()
        post_request = rf.post(path='/profile/', data={'age': 12, 'weight': 48})
        post_request.user = User.objects.create_user(username='testUser')
        resolver_match_mock = Mock(url_name='/profile')
        post_request.resolver_match = resolver_match_mock
        response = views.profile(post_request)
        self.assertEqual(response.status_code, 200)


class TestRedirect(TestCase):
    def test_no_data_entered_trying_to_go_to_calendar(self):
        rf = RequestFactory()
        get_request = rf.get(path='/calendar/')
        user = User.objects.create_user(username='testUser', password='testingPassword')
        get_request.user = user
        resolver_match_mock = Mock(url_name='calendar')
        get_request.resolver_match = resolver_match_mock
        response = wc_views.calendar(get_request)
        response.client = Client()
        self.assertRedirects(response, '/profile/?next=/calendar/', target_status_code=302)

    def test_data_entered_trying_to_go_to_calendar(self):
        rf = RequestFactory()
        get_request = rf.get(path='/calendar/')
        user = User.objects.create_user(username='testUser', password='testingPassword')
        user.profile.age = 12
        user.profile.weight = 40
        get_request.user = user
        resolver_match_mock = Mock(url_name='calendar')
        get_request.resolver_match = resolver_match_mock
        response = wc_views.calendar(get_request, year='2017', month='11')
        response.client = Client()
        self.assertEquals(response.status_code, 200)

    def test_no_data_entered_trying_to_go_to_dashboard(self):
        rf = RequestFactory()
        get_request = rf.get(path='/dashboard/')
        user = User.objects.create_user(username='testUser', password='testingPassword')
        get_request.user = user
        resolver_match_mock = Mock(url_name='dashboard')
        get_request.resolver_match = resolver_match_mock
        response = wc_views.calendar(get_request)
        response.client = Client()
        self.assertRedirects(response, '/profile/?next=/dashboard/', target_status_code=302)

    def test_data_entered_trying_to_go_to_dashboard(self):
        rf = RequestFactory()
        get_request = rf.get(path='/dashboard/')
        user = User.objects.create_user(username='testUser', password='testingPassword')
        user.profile.age = 12
        user.profile.weight = 40
        get_request.user = user
        resolver_match_mock = Mock(url_name='dashboard')
        get_request.resolver_match = resolver_match_mock
        response = wc_views.calendar(get_request, year='2017', month='11')
        response.client = Client()
        self.assertEquals(response.status_code, 200)
