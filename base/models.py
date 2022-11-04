# Create your models here.
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)


class Player(User):
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    height = models.FloatField(null=True)
    noOfGames = models.IntegerField(default=0)
    average = models.FloatField(default=0)


class LeagueAdmin(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_superuser = True


class Coach(User):
    team = models.OneToOneField(Team, on_delete=models.PROTECT)


class GameStatus(models.TextChoices):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    UPCOMING = "UPCOMING"


class Game(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='+')
    team2 = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='+')
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    winner = models.ForeignKey(Team, on_delete=models.PROTECT, null=True, blank=True, related_name='+')
    date = models.DateField()
    status = models.CharField(max_length=100, choices=GameStatus.choices)
    isDrawn = models.BooleanField(default=False)


class Stat(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    last_online = models.DateTimeField(null=True, blank=True)
    times_logged_in = models.PositiveIntegerField(null=True, blank=True)
