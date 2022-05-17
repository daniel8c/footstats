from django.db import models
from django.urls import reverse


# Create your models here.
class MatchResult(models.Model):
    id_match = models.IntegerField(primary_key=True)
    isResult = models.CharField(max_length=7)
    date = models.DateTimeField()
    season = models.IntegerField()
    league = models.CharField(max_length=20)
    h_id = models.IntegerField()
    h_title = models.CharField(max_length=60)
    h_short_title = models.CharField(max_length=10)
    a_id = models.IntegerField()
    a_title = models.CharField(max_length=60)
    a_short_title = models.CharField(max_length=10)
    goals_h = models.IntegerField(null=True)
    goals_a = models.IntegerField(null=True)
    xG_h = models.DecimalField(max_digits=7, decimal_places=5, blank=True)
    xG_a = models.DecimalField(max_digits=7, decimal_places=5, blank=True)
    forecast_w = models.DecimalField(
        max_digits=7, decimal_places=5, blank=True)
    forecast_d = models.DecimalField(
        max_digits=7, decimal_places=5, blank=True)
    forecast_l = models.DecimalField(
        max_digits=7, decimal_places=5, blank=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'{self.id_match} - {self.h_title} {self.goals_h} : {self.a_title} {self.goals_a}'


class Situation(models.Model):
    id_situation = models.IntegerField(primary_key=True)
    minute = models.IntegerField()
    result = models.CharField(max_length=16)
    x = models.DecimalField(max_digits=7, decimal_places=5)
    y = models.DecimalField(max_digits=7, decimal_places=5)
    xG = models.DecimalField(max_digits=7, decimal_places=5)
    player = models.CharField(max_length=60)
    h_a = models.CharField(max_length=2)
    player_id = models.IntegerField()
    situation = models.CharField(max_length=16)
    season = models.IntegerField()
    shotType = models.CharField(max_length=30)
    match_id = models.ForeignKey(
        MatchResult, on_delete=models.CASCADE, related_name='match_situation')
    h_team = models.CharField(max_length=60)
    a_team = models.CharField(max_length=60)
    h_goals = models.IntegerField()
    a_goals = models.IntegerField()
    date = models.DateTimeField()
    player_assisted = models.CharField(max_length=60)
    last_action = models.CharField(max_length=60)
    season = models.IntegerField()
    league = models.CharField(max_length=20)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'{self.id_situation}, {self.player} - {self.h_team} : {self.a_team}'

class PlayerStatisticInMatch(models.Model):
    id_player_statistic_in_match = models.IntegerField(primary_key=True)
    goals = models.IntegerField()
    own_goals = models.IntegerField()
    shots = models.IntegerField()
    xG = models.DecimalField(max_digits=7, decimal_places=5)
    time = models.IntegerField()
    player_id = models.IntegerField()
    team_id = models.IntegerField()
    position = models.CharField(max_length=6)
    player = models.CharField(max_length=60)
    h_a = models.CharField(max_length=2)
    yellow_card = models.IntegerField()
    red_card = models.IntegerField()
    roster_in = models.IntegerField()
    roster_out = models.IntegerField()
    key_passes = models.IntegerField()
    assists = models.IntegerField()
    xA = models.DecimalField(max_digits=7, decimal_places=5)
    xGChain = models.DecimalField(max_digits=7, decimal_places=5)
    xGBuildup = models.DecimalField(max_digits=7, decimal_places=5)
    positionOrder = models.IntegerField()
    match_id = models.ForeignKey(MatchResult, on_delete=models.CASCADE, related_name='player_situation_in_match')
    season = models.IntegerField()
    league = models.CharField(max_length=20)
