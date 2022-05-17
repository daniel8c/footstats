from django.shortcuts import render
from .models import MatchResult

# Create your views here.
def match_list(request):
    matches = MatchResult.resulttrue.all()
    return render(request, 'home/list.html', {'matches': matches})
