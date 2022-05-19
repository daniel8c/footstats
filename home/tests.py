from django.test import TestCase
import home

# Create your tests here.
def link_league(apps, schema_editor):
    MatchResult = apps.get_model('home', 'MatchResult')
    Legue = apps.get_model('home', 'League')
    for match in MatchResult.objects.all():
        league, created = League.objects.get_or_create(name=match.league)
        match.match_link = match
        match.save()
link_league(home, 'public')