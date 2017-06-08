from django.test import SimpleTestCase
from django.test.client import RequestFactory, Client
from django.urls import ResolverMatch
from workout_calendar import views
from workout_calendar import calendar_functions
from workout_calendar.models import Workout
import mock
from mock import patch


class TestDisplayForm(SimpleTestCase):
    def setUp(self):
        self.user = mock.Mock(username='testUser')

    def test_get_method_with_date(self):
        rf = RequestFactory()
        get_request = rf.get(path='/calendar/display_form', data={'date': '2017-09-08'})
        get_request.user = self.user
        with mock.patch.object(views, 'get_all_user_workouts') as mocked_method:
            mocked_method.return_value = []
            response = views.display_form(get_request)
            self.assertEqual(response.status_code, 200)

    def test_get_method_no_date(self):
        rf = RequestFactory()
        get_request = rf.get(path='/calendar/display_form')
        get_request.user = self.user
        with mock.patch.object(views, 'get_all_user_workouts') as mocked_method:
            mocked_method.return_value = []
            response = views.display_form(get_request)
            self.assertEqual(response.status_code, 404)


class TestCalendar(SimpleTestCase):
    def setUp(self):
        self.user = mock.Mock(username='testUser')

    def test_calendar_get_method(self):
        rf = RequestFactory()
        get_request = rf.get(path='/calendar/')
        get_request.user = self.user
        get_request.resolver_match = ResolverMatch(func=None, args=None, kwargs=None)
        get_request.resolver_match.url_name = 'calendar'
        with mock.patch.object(views, 'get_workouts_for_calendar') as calendar_mocked_method:
            calendar_mocked_method.return_value = []
            response = views.calendar(get_request, '2017', '07')
            self.assertEqual(response.status_code, 200)

    def test_calendar_post_delete_method(self):
        rf = RequestFactory()
        post_request = rf.post(path='/calendar/')
        post_request.user = self.user
        post_request.data = 'delete'
        # Mocking delete function
        with mock.patch.object(Workout, 'delete') as delete_mock:
            delete_mock.return_value = True
            response = views.calendar(post_request, '2017', '08')
            response.client = Client()
            # Check if the user has been redirected
            self.assertRedirects(response, expected_url='/calendar/', target_status_code=302)

    def test_calendar_post_update_method(self):
        rf = RequestFactory()
        post_request = rf.post(path='/calendar/')
        post_request.user = self.user
        post_request.data = 'delete'
        with mock.patch.object(Workout, 'save') as update_mock:
            update_mock.return_value = True
            response = views.calendar(post_request, '2017', '08')
            response.client = Client()
            self.assertRedirects(response, expected_url='/calendar/', target_status_code=302)


class TestCalendarFunctions(SimpleTestCase):
    def setUp(self):
        self.calendar = calendar_functions.WorkoutCalendar([])

    def test_day_cell(self):
        result = self.calendar.day_cell('class', 'id', 'body')
        self.assertEqual(result, '<td class="class" id="id">body</td>')

    def test_format_one_digit_bigger_than_nine(self):
        result = self.calendar.format_one_digit('12')
        self.assertEqual('12', result)

    def test_format_one_digit_smaller_than_nine(self):
        result = self.calendar.format_one_digit('5')
        self.assertEqual('05', result)

    def test_format_month(self):
        self.calendar.formatmonth(2015, 5)
        self.assertEqual(self.calendar.month, 5)
        self.assertEqual(self.calendar.year, 2015)

    @patch('workout_calendar.calendar_functions.WorkoutCalendar.day_cell_no_id')
    def test_format_day_no_day(self, mock):
        # Checking if another function has been called
        self.calendar.formatday(0, 0)
        self.assertTrue(mock.called)
