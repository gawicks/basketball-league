import json
import random
from unicodedata import name
from urllib import response
from rest_framework.test import APITestCase
from rest_framework import status

from base.factories import PlayerFactory, TeamFactory, GameFactory
from base.models import Team, User, Player, Coach, LeagueAdmin
import factory
from faker import Faker
faker = Faker()

def create_user(role, username=None, password=None, team_id=None):
    user=None
    if team_id is None:
        team=TeamFactory()
        team_id=team.id
    if username is None:
        username=faker.name()
    if password is None:
        password=faker.text()
    if role == Player:
        user = Player.objects.create_user(username=username, password=password, team_id=team_id)
    elif role == Coach:
        user = Coach.objects.create_user(username=username, password=password, team_id=team_id)
    elif role == LeagueAdmin:
        user = LeagueAdmin.objects.create_user(username=username, password=password, team_id=team_id)
    return username,password,user.id;
class Scoreboard(APITestCase):
    def test_player_redirect_to_scoreboard(self):
        username,password,_=create_user(Player)
        self.client.login(username=username, password=password)
        response = self.client.get('/')
        self.assertEqual(response.status_code,301)
        self.assertEqual(response.url,'/scoreboard')
    def test_scoreboard_visible_to_player(self):
        username,password,_=create_user(Player)
        team1=TeamFactory(name='foo')
        team2=TeamFactory(name='bar')
        GameFactory(team1=team1, team2=team2).save()
        self.client.login(username=username, password=password)
        response = self.client.get('/scoreboard')
        responseJson=response.json()[0]
        self.assertEqual(responseJson['team1name'],'foo')
        self.assertEqual(responseJson['team2name'],'bar')

class Scoreboard(APITestCase):
    def test_player_redirect_to_scoreboard(self):
        username,password,_=create_user(Player)
        self.client.login(username=username, password=password)
        response = self.client.get('/')
        self.assertEqual(response.status_code,301)
        self.assertEqual(response.url,'/scoreboard')
    def test_scoreboard_visible_to_player(self):
        username,password,_=create_user(Player)
        team1=TeamFactory(name='foo')
        team2=TeamFactory(name='bar')
        GameFactory(team1=team1, team2=team2).save()
        self.client.login(username=username, password=password)
        response = self.client.get('/scoreboard')
        responseJson=response.json()[0]
        self.assertEqual(responseJson['team1name'],'foo')
        self.assertEqual(responseJson['team2name'],'bar')


