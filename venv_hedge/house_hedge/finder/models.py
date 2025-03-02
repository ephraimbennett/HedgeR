from django.db import models
from home.models import Member

# Create your models here.
class Settings(models.Model):
    user = models.OneToOneField(Member, on_delete=models.CASCADE) # The link to member
    state = models.CharField(max_length=2, null=False, default="XX")

class BonusBet(models.Model):
    title = models.TextField(null=True)
    market = models.TextField(null=True)

    # the bonus bet
    bonus_bet = models.TextField(null=True)
    bonus_odds = models.IntegerField(null=True)
    bonus_name = models.TextField(null=True)

    hedge_bet = models.TextField(null=True)
    hedge_odds = models.IntegerField(null=True)
    hedge_index = models.FloatField(null=True)
    hedge_name = models.TextField(null=True)

    profit_index = models.FloatField(null=True)

class SecondBet(models.Model):
    title = models.TextField(null=True)

    # the bonus bet
    bonus_bet = models.TextField(null=True)
    bonus_odds = models.IntegerField(null=True)

    hedge_bet = models.TextField(null=True)
    hedge_odds = models.IntegerField(null=True)

    hedge_index = models.FloatField(null=True)

    profit_index = models.FloatField(null=True)

class BookMaker(models.Model):
    title = models.TextField()
