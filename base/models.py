from django.db import models

# Create your models here.
from django.contrib.auth.models import User, Group

class Team(models.Model):
    name = models.CharField(max_length=1 - 00)


class Player(User):
    team = models.ForeignKey(Team, on_delete=models.PROTECT)


class LeagueAdmin(User):
    pass


class Coach(User):
    team = models.OneToOneField(Team, on_delete=models.PROTECT)
