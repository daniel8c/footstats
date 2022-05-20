from django import template
from home.models import MatchResult, League

register = template.Library()

@register.simple_tag
def display_league():
    leagues = League.objects.all()
    return leagues