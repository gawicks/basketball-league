from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from base.factories import TeamFactory, GameFactory
from base.models import Player, Coach, LeagueAdmin, Group, Permission, ContentType

faker = Faker()


def create_user(role, username=None, password=None, email=None, **kwargs):
    user = None
    if username is None:
        username = faker.name()
    if email is None:
        email = faker.email()
    if password is None:
        password = faker.text()
    if role == Player:
        user = Player.objects.create_user(username, email, password, **kwargs)
        group, _ = Group.objects.get_or_create(name="players")
        content_type_player, _ = ContentType.objects.get_or_create(
            app_label='base', model='player')
        permission_view_player, _ = Permission.objects.get_or_create(
            content_type_id=content_type_player.id, codename="view_player")
        group.permissions.add(permission_view_player)
        user.groups.add(group)
    elif role == Coach:
        user = Coach.objects.create_user(username, email, password, **kwargs)
        group = Group.objects.create(name="coaches")
        if group is None:
            group = Group.objects.create(name="coaches")
        content_type_team, _ = ContentType.objects.get_or_create(
            app_label='base', model='team')
        content_type_player, _ = ContentType.objects.get_or_create(
            app_label='base', model='player')
        permission_view_team, _ = Permission.objects.get_or_create(
            content_type_id=content_type_team.id, codename="view_team")
        permission_view_player, _ = Permission.objects.get_or_create(
            content_type_id=content_type_player.id, codename="view_player")
        group.permissions.add(permission_view_team)
        group.permissions.add(permission_view_player)
        user.groups.add(group)
    elif role == LeagueAdmin:
        # LeagueAdmin is a super user, there's no need to assign permissions explictly
        user = LeagueAdmin.objects.create_user(
            username, email, password, **kwargs)
        group = Group.objects.create(name="admins")
        user.groups.add(group)
    return username, password, user.id


class Scoreboard(APITestCase):
    def test_user_should_redirect_to_scoreboard(self):
        team = TeamFactory(name='foo')
        username, password, _ = create_user(Player, team_id=team.id)
        self.client.login(username=username, password=password)
        response = self.client.get('/')
        self.assertEqual(response.status_code,
                         status.HTTP_301_MOVED_PERMANENTLY)
        self.assertEqual(response.url, '/scoreboard')

    def test_logged_in_user_can_view_scoreboard(self):
        team1 = TeamFactory(name='foo')
        team2 = TeamFactory(name='bar')
        username, password, _ = create_user(Player, team_id=team1.id)
        GameFactory(team1=team1, team2=team2).save()
        self.client.login(username=username, password=password)
        response = self.client.get('/scoreboard')
        response_json = response.json()[0]
        self.assertEqual(response_json['team1name'], 'foo')
        self.assertEqual(response_json['team2name'], 'bar')

    def test_anonymous_user_cannot_view_scoreboard(self):
        team1 = TeamFactory(name='foo')
        team2 = TeamFactory(name='bar')
        username, password, _ = create_user(Player, team_id=team1.id)
        GameFactory(team1=team1, team2=team2)
        # self.client.login(username=username, password=password)
        response = self.client.get('/scoreboard')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/accounts/login/?next=/scoreboard')


class Teams(APITestCase):
    def test_coach_can_view_own_team_stats(self):
        team1 = TeamFactory(name='foo')
        username, password, _ = create_user(Coach, team_id=team1.id)
        create_user(Player, username="jonah", team_id=team1.id)
        self.client.login(username=username, password=password)
        response = self.client.get(f'/team/{team1.id}')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['players'][0]['username'], "jonah")

    def test_coach_can_filter_players_having_avg_score_in_90th_percentile(self):
        team1 = TeamFactory(name='foo')
        username, password, _ = create_user(Coach, team_id=team1.id)
        create_user(Player, username="jonah", team_id=team1.id, average=10)
        create_user(Player, username="jessie", team_id=team1.id, average=15)
        create_user(Player, username="james", team_id=team1.id, average=21)
        create_user(Player, username="jacob", team_id=team1.id, average=22)
        self.client.login(username=username, password=password)
        response = self.client.get(f'/team/{team1.id}?filter=90percentile')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['players'][0]['username'], "jacob")

    def test_coach_can_view_own_team_player_stats(self):
        team1 = TeamFactory(name='foo')
        username, password, _ = create_user(Coach, team_id=team1.id)
        _, _, player_id = create_user(
            Player, username="russel", team_id=team1.id)
        self.client.login(username=username, password=password)
        response = self.client.get(f'/player/{player_id}', follow=True)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['username'], "russel")

    def test_player_can_view_own_stats(self):
        team1 = TeamFactory(name='foo')
        create_user(Coach, team_id=team1.id)
        username, password, player_id = create_user(
            Player, username="arnold", team_id=team1.id)
        self.client.login(username=username, password=password)
        response = self.client.get(f'/player/{player_id}', follow=True)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['username'], "arnold")

    def test_league_admin_can_view_team_stats(self):
        team1 = TeamFactory(name='foo')
        create_user(Coach, team_id=team1.id)
        create_user(Player, username="timothy", team_id=team1.id)
        username, password, _ = create_user(LeagueAdmin)
        self.client.login(username=username, password=password)
        response = self.client.get(f'/team/{team1.id}')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['players'][0]['username'], "timothy")

    def test_league_admon_can_view_player_stats(self):
        team1 = TeamFactory(name='foo')
        create_user(Coach, team_id=team1.id)
        _, _, player_id = create_user(Player, username="john", team_id=team1.id)
        username, password, _ = create_user(LeagueAdmin)
        self.client.login(username=username, password=password)
        response = self.client.get(f'/player/{player_id}', follow=True)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['username'], "john")


class Stats(APITestCase):
    def test_admin_can_view_stats(self):
        username, password, _ = create_user(LeagueAdmin)
        self.client.login(username=username, password=password)
        response = self.client.get('/stats')
        response_json = response.json()[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['username'], username)
        self.assertEqual(response_json['times_logged_in'], 1)
