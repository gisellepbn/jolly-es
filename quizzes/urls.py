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

]
