from django import template
from home.models import MatchResult, League

register = template.Library()

@register.simple_tag
def total_matches():
    return MatchResult.premierleague.count()

@register.simple_tag
def display_league():
    leagues = League.objects.all()
    return leagues

@register.filter
def repl(value):
    """Removes all values of arg from the given string"""
    return value.replace(' ', '_')