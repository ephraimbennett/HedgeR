from django.db import models
from home.models import Member

# Create your models here.
class Settings(models.Model):
    user = models.OneToOneField(Member, on_delete=models.CASCADE) # The link to member
    state = models.CharField(max_length=2, null=False, default="XX")

class BonusBet(models.Model):
    title = models.TextField

    # the bonus bet
    bonus_bet = models.TextField
    bonus_odds = models.IntegerField

    hedge_bet = models.TextField
    hedge_odds = models.IntegerField

    profit_index = models.FloatField
