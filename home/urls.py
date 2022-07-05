from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.match_list, name='match_list'),
    path('<name>/', views.match_list, name='filter_league'),
    path('<id>/<h_title>_<a_title>/', views.match_detail, name='match_detail'),
    path('<id>/<player>/', views.player_detail, name='player_detail')
    # path('<league>/', views.match_list, name='league'),
]
