from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from home.models import MatchResult, League, Roster
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from home.pitch import draw_pitch, get_info_situations, add_situations_to_pitch
from plotly.offline import plot


# Create your views here.


def match_list(request):
    object_list = MatchResult.resulttrue.all().order_by('-league', '-datetime')
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
    object_list = league.result_league.filter(season='2021').filter(isresult=True).order_by('-datetime')

    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')

    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)

    return render(request, 'home/match/list.html',
                  {'a_league': league, 'matches': matches, 'all_leagues': all_leagues, })


def match_detail(request, id, h_title, a_title):
    match = get_object_or_404(MatchResult, id=id, h_title=h_title, a_title=a_title)
    home_s, away_s = get_info_situations(match)
    fig = draw_pitch()
    add_situations_to_pitch(fig, home_s, away_s, match = match)
    config = {'displayModeBar': False, }
    plot_div = plot({'data': fig, }, output_type='div', config=config)

    # Rosters
    rosters_home, rosters_away = match.roster_result.filter(h_a='h'), match.roster_result.filter(h_a='a')

    # TODO display rosters
    return render(request, 'home/match/detail.html',
                  {'match': match, 'plot_div': plot_div, 'rosters_home': rosters_home, 'rosters_away': rosters_away})
