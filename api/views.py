import plistlib
from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Team
from .serlalizers import TeamSerializer
from base.models import Group, Player, LeagueAdmin, Coach
from django.contrib.auth.decorators import login_required
@api_view(['GET'])
@login_required()
def auth(request):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)

@api_view(['GET'])
def get(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)

    adminGroup, _ =Group.objects.update_or_create(name='admins')
    playerGroup, _= Group.objects.update_or_create(name='players')
    coachGroup, _ =Group.objects.update_or_create(name='coaches')

    team1, _= Team.objects.update_or_create(name='Manchester United')
    team2, _= Team.objects.update_or_create(name='Liverpool')


    player1 = Player.objects.create_user(username='cr57', password='test', email='cr57@manchesterufc.com',
                    first_name='Christiano', last_name='Ronaldo', team=team1)
    player2 = Player.objects.create_user(username='ddgea', password='test', email='ddgea@manchesterufc.com',
                    first_name='David', last_name='Gea', team=team2)
    player3 = Player.objects.create_user(username='abecker', password='test', email='abecker@liverpoolfc.com',
                    first_name='Alisson', last_name='Becker', team=team2)
    player4 = Player.objects.create_user(username='talcantara', password='test', email='talcantara@liverpoolfc.com',
                    first_name='Thiago', last_name='Alcantara', team=team2)

    player1.groups.add(playerGroup)
    player2.groups.add(playerGroup)
    player3.groups.add(playerGroup)
    player4.groups.add(playerGroup)

    player1.save()
    player2.save()
    player3.save()
    player4.save()

    coach1 = Coach.objects.create_user(username='jklopp', password='test', email='jklopp@manchesterufc.com',
                first_name='Jürgen', last_name='Klopp', team=team1)
    coach2 = Coach.objects.create_user(username='ehag', password='test', email='ehag@liverpoolfc.com',
                first_name='Erik', last_name='Hag', team=team2)

    coach1.groups.add(coachGroup)
    coach2.groups.add(coachGroup)
    coach1.save()
    coach2.save()

    leagueAdmin= LeagueAdmin.objects.create_user(username='gawicks', password='root',
                            email='gawicks@premierleague.com', first_name='Haritha', last_name='Wickremasinghe')
    leagueAdmin.groups.add(adminGroup)
    leagueAdmin.save()

    return Response(serializer.data)
