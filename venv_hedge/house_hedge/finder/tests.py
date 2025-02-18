from django.test import TestCase
from .services import update_bonus_bets

# Create your tests here.

class CalculateTestCase(TestCase):
    def from_services(self):
        update_bonus_bets()