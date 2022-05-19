from django.urls import path
from . import views

app_name = 'home'


urlpatterns = [
    path('', views.match_list, name='home'),
    path('<id>/<h_title>_<a_title>/', views.match_detail, name = 'match_detail'),
    path('<name>/', views.filter_league, name = 'filter_league'),
    # path('<league>/', views.match_list, name='league'),
]
