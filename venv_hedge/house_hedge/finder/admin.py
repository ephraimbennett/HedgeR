from django.contrib import admin
from .models import Settings, BonusBet, SecondBet

# Register your models here.
admin.site.register(BonusBet)
admin.site.register(Settings)
admin.site.register(SecondBet)