from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from home.models import MatchResult, League
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def match_list(request):
    object_list = MatchResult.resulttrue.all()
    all_leagues = League.objects.all()
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')

    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    return render(request, 'home/match/list.html', {'matches': matches, 'all_leagues': all_leagues, 'page': page})


def filter_league(request, name):
    all_leagues = League.objects.all()
    league = get_object_or_404(League, name=name)
    object_list = league.result_league.filter(season='2021').filter(isresult=True)

    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')

    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)

    return render(request, 'home/match/list.html', {'league': league, 'matches': matches, 'all_leagues': all_leagues, })


def match_detail(request, id, h_title, a_title):
    match = get_object_or_404(MatchResult, id=id, h_title=h_title, a_title=a_title)
    return render(request, 'home/match/detail.html', {'match': match})

# def match_list_league(request):
#     leagues = ['Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1']
#     return  render(request, 'home/base.html', {'leagues': leagues})


# def league_matches(request, legue)
#     matches =
#     return render(request, 'home/match/list.html', {'matches' : matches})
