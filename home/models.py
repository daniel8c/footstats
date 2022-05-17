from django.db import models
from django.urls import reverse

# Create your models here.
class MatchResultTrue(models.Manager):
    def get_queryset(self):
        return super(MatchResultTrue, self).get_queryset().filter(isresult = True).filter(league='EPL').filter(season='2021')

class MatchResult(models.Model):
    id = models.IntegerField(primary_key=True)
    isresult = models.BooleanField()
    datetime = models.DateTimeField()
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
    xg_h = models.DecimalField(max_digits=7, decimal_places=5, null=True)
    xg_a = models.DecimalField(max_digits=7, decimal_places=5, null=True)
    forecast_w = models.DecimalField(
        max_digits=7, decimal_places=5, null=True)
    forecast_d = models.DecimalField(
        max_digits=7, decimal_places=5, null=True)
    forecast_l = models.DecimalField(
        max_digits=7, decimal_places=5, null=True)

    objects = models.Manager()
    resulttrue = MatchResultTrue()

    class Meta:
        ordering = ('-datetime',)

    def __str__(self):
        return f'{self.id} - {self.h_title} {self.goals_h} : {self.a_title} {self.goals_a}'


class SituationMatch(models.Model):
    id = models.IntegerField(primary_key=True)
    minute = models.IntegerField()
    result = models.CharField(max_length=16)
    x = models.DecimalField(max_digits=7, decimal_places=5)
    y = models.DecimalField(max_digits=7, decimal_places=5)
    xg = models.DecimalField(max_digits=7, decimal_places=5)
    player = models.CharField(max_length=60)
    h_a = models.CharField(max_length=2)
    player_id = models.IntegerField()
    situation = models.CharField(max_length=16)
    season = models.IntegerField()
    shottype = models.CharField(max_length=30)
    match_id = models.ForeignKey(
        MatchResult, on_delete=models.CASCADE, related_name='situation_result')
    h_team = models.CharField(max_length=60)
    a_team = models.CharField(max_length=60)
    h_goals = models.IntegerField()
    a_goals = models.IntegerField()
    date = models.DateTimeField()
    player_assisted = models.CharField(max_length=60, null=True)
    lastaction = models.CharField(max_length=60)
    season = models.IntegerField()
    # league = models.CharField(max_length=20)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'{self.id}, {self.player} - {self.h_team} : {self.a_team}'


class Roster(models.Model):
    id = models.IntegerField(primary_key=True)
    goals = models.IntegerField()
    own_goals = models.IntegerField()
    shots = models.IntegerField()
    xg = models.DecimalField(max_digits=7, decimal_places=5)
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
    xa = models.DecimalField(max_digits=7, decimal_places=5)
    xgchain = models.DecimalField(max_digits=7, decimal_places=5)
    xgbuildup = models.DecimalField(max_digits=7, decimal_places=5)
    positionorder = models.IntegerField()
    match_id = models.ForeignKey(MatchResult, on_delete=models.CASCADE, related_name='roster_result')

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'{self.id}, {self.player}'

class TeamHistory(models.Model):
    team_id = models.IntegerField()
    title = models.CharField(max_length=60)
    season = models.IntegerField()
    league = models.CharField(max_length=20)
    kolejka = models.IntegerField()
    h_a = models.CharField(max_length=2)
    xg = models.DecimalField(max_digits=7, decimal_places=5)
    xga = models.DecimalField(max_digits=7, decimal_places=5)
    npxg = models.DecimalField(max_digits=7, decimal_places=5)
    npxga = models.DecimalField(max_digits=7, decimal_places=5)
    deep = models.IntegerField()
    deep_allowed = models.IntegerField()
    scored = models.IntegerField()
    missed = models.IntegerField()
    xpts = models.DecimalField(max_digits=7, decimal_places=5)
    result = models.CharField(max_length=2)
    date = models.DateTimeField()
    wins = models.IntegerField()
    draws = models.IntegerField()
    loses = models.IntegerField()
    pts = models.IntegerField()
    npxgd = models.DecimalField(max_digits=7, decimal_places=5)
    ppda_att = models.IntegerField()
    ppda_def = models.IntegerField()
    ppda_allowed_att = models.IntegerField()
    ppda_allowed_def = models.IntegerField()