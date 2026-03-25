from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('start/', views.start_game, name='start_game'),
    path('game/<int:session_id>/round/<int:round_num>/', views.game_round, name='game_round'),
    path('game/<int:session_id>/round/<int:round_num>/submit/', views.submit_guess, name='submit_guess'),
    path('game/<int:session_id>/result/', views.game_result, name='game_result'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('how-to-play/', views.how_to_play, name='how_to_play'),
]
