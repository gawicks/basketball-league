import factory
from faker import Faker

from .models import Game, Player, Team

faker = Faker()


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player


class GameFactory(factory.django.DjangoModelFactory):
    score1 = faker.random_int()
    score2 = faker.random_int()
    date = faker.date_time()

    class Meta:
        model = Game
