import numpy
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Player, Game, Team
from .serlalizers import GamesSerializer, PlayerSerializer, StatSerializer, TeamSerializer
from .signals import Stat  # Needs to reference signals


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


@login_required()
@api_view(['GET'])
def scoreboard(_request, game_id=None):
    if game_id is None:
        games = Game.objects.all()
    else:
        games = Game.objects.filter(id=game_id)

    serializer = GamesSerializer(games, many=True)
    return Response(serializer.data)


@login_required()
@api_view(['GET'])
@permission_required('base.view_team', raise_exception=True)
def team(request, team_id):
    this_team = Team.objects.filter(id=team_id)[0]
    authorized = request.user.id == this_team.coach.id or request.user.is_superuser
    if not authorized:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    filters = request.GET.get('filter')
    teamserializer = TeamSerializer(this_team, many=False)
    if filters == "90percentile":
        this_team = Team.objects.filter(id=team_id)[0]
        players = this_team.player_set.all()
        averages = map(lambda x: x.average, players)
        _90p = numpy.percentile(list(averages), 90)  # It's idiomatic to use numpy than implementing this from scratch
        players = PlayerSerializer(
            filter(lambda x: x.average > _90p, players), many=True).data
    else:
        players = Player.objects.filter(team=team_id)
        playerserializer = PlayerSerializer(players, many=True)
        players = playerserializer.data

    return Response({"team": teamserializer.data, "players": players})


@api_view(['GET'])
@permission_required('base.view_player', raise_exception=True)
def player(request, player_id):
    this_player = Player.objects.filter(id=player_id)[0]
    this_team = this_player.team
    authorized = request.user.id == this_team.coach.id or request.user.id == this_player.id or request.user.is_superuser
    if not authorized:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    playerserializer = PlayerSerializer(this_player)
    player_data = playerserializer.data
    return Response(player_data)


@api_view(['GET'])
@permission_required('base.view_stat', raise_exception=True)
def stats(request):
    this_stats = Stat.objects.all()
    statserializer = StatSerializer(this_stats, many=True)
    stat_data = statserializer.data
    return Response(stat_data)
