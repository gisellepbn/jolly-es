from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('account/<str:search_option>', views.account, name='account'),
    path('join', views.join_quiz, name='join_quiz'),
    path('live-quiz/<int:pin>/<uuid:participant_id>',
         views.live_quiz, name='live_quiz'),
    path('create-quiz', views.create_quiz, name='create_quiz'),
    path('edit-quiz/<uuid:id>', views.edit_quiz, name='edit_quiz'),
    path('question/<uuid:id>', views.question, name='question'),
    path('delete-quiz/<uuid:id>', views.delete_quiz, name='delete_quiz'),
    path('start-quiz/<uuid:id>', views.start_quiz, name='start_quiz'),
    path('scoreboard/<uuid:id>', views.scoreboard, name='scoreboard'),


]
