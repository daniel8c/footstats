from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from home.models import MatchResult
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def match_list(request):
    print(request)
    print(request.path == '/home/')
    if request.method == 'GET':
        print('GET')
    leagues = ['Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1']
    object_list = MatchResult.resulttrue.all()
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    la_liga = request.GET.get('La Liga')
    print(la_liga)

    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    return render(request, 'home/match/list.html', {'matches': matches, 'page':  page, 'leagues': leagues})

def match_list_premier_league(request):
    object_list = MatchResult.premierleague.all()
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    return render(request, 'home/match/list.html', {'matches': matches, 'page':  page})

def match_list_la_liga(request):
    object_list = MatchResult.laliga.all()
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')

    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    return render(request, 'home/match/list.html', {'matches': matches, 'page':  page})

def match_list_serie_a(request):
    object_list = MatchResult.seriea.all()
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    return render(request, 'home/match/list.html', {'matches': matches, 'page':  page})

def match_list_bundesliga(request):
    object_list = MatchResult.bundesliga.all()
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    return render(request, 'home/match/list.html', {'matches': matches, 'page':  page})

def match_list_ligue_1(request):
    object_list = MatchResult.ligue1.all()
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    return render(request, 'home/match/list.html', {'matches': matches, 'page':  page})





def match_detail(request, id, h_title, a_title):
    match = get_object_or_404(MatchResult, id = id, h_title = h_title, a_title = a_title)
    return render(request, 'home/match/detail.html', {'match' : match})

# def match_list_league(request):
#     leagues = ['Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1']
#     return  render(request, 'home/base.html', {'leagues': leagues})


# def league_matches(request, legue)
#     matches =
#     return render(request, 'home/match/list.html', {'matches' : matches})
