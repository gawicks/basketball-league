from rest_framework import serializers

from base.models import Game, Player, Stat, Team


class TeamSerializer(serializers.ModelSerializer):
    team_average = serializers.SerializerMethodField('get_team_average')

    @staticmethod
    def get_team_average(obj):
        players = obj.player_set.all()
        avg = sum(map(lambda x: x.average, players), 0.0) / len(players) #TODO: use mean or numpy.average
        return avg

    class Meta:
        model = Team
        fields = '__all__'


class GamesSerializer(serializers.ModelSerializer):
    team1name = serializers.CharField(source='team1.name')
    team2name = serializers.CharField(source='team2.name')

    class Meta:
        model = Game
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        exclude = (['groups','user_permissions','is_staff','is_active','is_superuser', 'last_login','password'])



class StatSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Stat
        fields = '__all__'
