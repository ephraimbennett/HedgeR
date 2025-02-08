from django.db import models
from home.models import Member

# Create your models here.
class Settings(models.Model):
    user = models.OneToOneField(Member, on_delete=models.CASCADE) # The link to member
    state = models.CharField(max_length=2, null=False, default="XX")
