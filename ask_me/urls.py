from django.urls import path

from . import views

app_name = 'ask_me'
urlpatterns = [
    path('', views.search, name='index'),
    path('<int:question_id>/', views.getDetail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/delete/', views.deleteQuestion, name='delete'),
]
