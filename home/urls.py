from django.urls import path
from . import views

app_name = 'home'


urlpatterns = [
    path('', views.match_list, name='home'),
    path('Premier_League', views.match_list_premier_league, name='premier_league'),
    path('La_Liga', views.match_list_la_liga, name='premier_league'),
    path('Serie_A', views.match_list_serie_a, name='premier_league'),
    path('Bundesliga', views.match_list_bundesliga, name='premier_league'),
    path('Ligue_1', views.match_list_ligue_1, name='premier_league'),
    path('<id>/<h_title>_<a_title>/', views.match_detail, name = 'match_detail'),
    # path('<league>/', views.match_list, name='league'),
]
