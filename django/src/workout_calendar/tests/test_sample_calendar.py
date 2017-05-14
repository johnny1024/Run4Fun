from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import ResolverMatch
from workout_calendar import views
from workout_calendar import calendar_functions
from django.contrib.auth.models import User


class DisplayFormTestCase(TestCase):
    def test_get_method_with_date(self):
        rf = RequestFactory()
        get_request = rf.get(path='/calendar/display_form', data ={'date': '2017-09-08'})
        get_request.user = User.objects.create_user(username='testUser')
        response = views.display_form(get_request)
        self.assertEqual(response.status_code, 200)

    def test_get_method_no_date(self):
        rf = RequestFactory()
        get_request = rf.get(path='/calendar/display_form')
        get_request.user = User.objects.create_user(username='testUser')
        response = views.display_form(get_request)
        self.assertEqual(response.status_code, 404)

class CalendarTestCase(TestCase):
    def test_calendar_get_method(self):
        rf = RequestFactory()
        get_request = rf.get(path='/calendar/')
        get_request.user = User.objects.create_user(username='testUser')
        get_request.resolver_match = ResolverMatch(func=None, args=None, kwargs=None)
        get_request.resolver_match.url_name = 'calendar'
        response = views.calendar(get_request, '2017', '07')
        self.assertEqual(response.status_code, 200)

class CalendarFunctionsTestCase(TestCase):
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

