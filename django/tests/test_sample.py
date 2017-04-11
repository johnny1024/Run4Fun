from django.test import TestCase

class TestingClass(TestCase):
    def test_passing(self):
        self.assertEqual(1, 1)

    def test_notPassing(self):
        self.assertEqual(1, 0)