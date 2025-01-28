from django.db import models

# Create your models here.

class Member(models.Model) :
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    joined_date = models.DateField(null=True)
    phone = models.IntegerField(null=True)
    status = models.BooleanField()

    def __str__(self):
        return f"{self.email}"