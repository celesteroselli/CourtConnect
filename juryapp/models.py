from django.db import models
from django.contrib.auth.models import User
from django_random_id_model import RandomIDModel

class Number(models.Model):
    number = models.IntegerField()
    def __str__(self):
         return str(self.number)

class Jury(RandomIDModel):
    judge = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
         return str(self.pk)

class Panel(RandomIDModel):
    jury = models.ForeignKey(Jury, on_delete=models.CASCADE)
    number = models.IntegerField()
    members = models.ManyToManyField(Number)
    def __str__(self):
         return str(self.number)

class Message(models.Model):
    judge = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=100, default="Message")
    panel = models.ManyToManyField(Panel)
    def __str__(self):
         return str(self.message)

