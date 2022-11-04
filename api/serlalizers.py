from dataclasses import field
from rest_framework import serializers
from base.models import Game, Player, Team

class TeamSerializer(serializers.ModelSerializer):
    team_average = serializers.SerializerMethodField('get_team_average')
    def get_team_average(self, obj):
        players = obj.player_set.all();
        print(obj.__dict__)
        avg = sum(map(lambda x:x.average, players), 0.0) / len(players)
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
        fields = '__all__'
