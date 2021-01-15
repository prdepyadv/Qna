from django.urls import path

from . import views

app_name = 'ask_me'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.getDetail, name='detail'),
    path('<int:question_id>/approve/', views.approve, name='approve'),
    path('<int:question_id>/results/', views.results, name='results'),
]
