from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from base.models import Team
from .serlalizers import GamesSerializer, PlayerSerializer, TeamSerializer
from base.models import Group, Player, LeagueAdmin, Coach, Game, Team
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)

@login_required()
@api_view(['GET'])
def scoreboard(request,id= None):
    games = []
    if id is None:
        games = Game.objects.all()
    else:
        games = Game.objects.filter(id=id)

    serializer = GamesSerializer(games, many=True)
    return Response(serializer.data)

@login_required()
@api_view(['GET'])
def team(request,id):
    filters = request.GET.get('filter')
    teams = Team.objects.filter(id=id)[0]
    teamserializer = TeamSerializer(teams, many=False)
    players=None
    if (filters == "90percentile"):
        team = Team.objects.filter(id=id)[0]
        players = team.player_set.all()
        avg = sum(map(lambda x:x.average, players), 0.0) / len(players)
        players = PlayerSerializer(filter(lambda x:x.average>avg, players), many=True).data
    else:
        players = Player.objects.filter(team=id)
        playerserializer = PlayerSerializer(players, many=True)
        players = playerserializer.data

    return Response({ "team": teamserializer.data, "players": players})


# def player(request):
#     pass
#@permission_required('base.view_game', raise_exception=True)


