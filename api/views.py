from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from base.models import Team
from .serlalizers import GamesSerializer, PlayerSerializer, TeamSerializer
from base.models import Group, Player, LeagueAdmin, Coach, Game, Team
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
import numpy


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


@login_required()
@api_view(['GET'])
def scoreboard(request, id=None):
    games = []
    if id is None:
        games = Game.objects.all()
    else:
        games = Game.objects.filter(id=id)

    serializer = GamesSerializer(games, many=True)
    return Response(serializer.data)


@login_required()
@api_view(['GET'])
@permission_required('base.view_team', raise_exception=True)
def team(request, id):
    team = Team.objects.filter(id=id)[0]
    authorized = request.user.id == team.coach.id or request.user.is_superuser
    if (not authorized):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    filters = request.GET.get('filter')
    teamserializer = TeamSerializer(team, many=False)
    players = None
    if (filters == "90percentile"):
        team = Team.objects.filter(id=id)[0]
        players = team.player_set.all()
        averages = map(lambda x:x.average, players)
        _90p = numpy.percentile(list(averages), 90) #It's idiomatic to use numpy than implementing this from scratch
        players = PlayerSerializer(
            filter(lambda x: x.average > _90p, players), many=True).data
    else:
        players = Player.objects.filter(team=id)
        playerserializer = PlayerSerializer(players, many=True)
        players = playerserializer.data

    return Response({"team": teamserializer.data, "players": players})

@api_view(['GET'])
@permission_required('base.view_player', raise_exception=True)
def player(request, id):
    player = Player.objects.filter(id=id)[0]
    team = player.team
    print(team.__dict__)
    authorized = request.user.id == team.coach.id or request.user.id == player.id or request.user.is_superuser
    if (not authorized):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    playerserializer = PlayerSerializer(player)
    player_data = playerserializer.data
    return Response(player_data)
# @permission_required('base.view_game', raise_exception=True)
