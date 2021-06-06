from django.contrib import admin
from django.urls import path
from ask_me import views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout', views.logoutUser, name='logout'),
    path('login', views.loginUser, name='login'),
    path('', views.index, name='home'),
    path('search/', include('ask_me.urls')),
    path('lastest-10', views.lastestQuestions, name='lastedQuestions'),
    path('answer/update/', views.updateAnswer, name='updateAnswer'),
    path('answer/delete/', views.deleteAnswer, name='deleteAnswer'),
    path('answer/save-new/', views.saveAnswer, name='saveAnswer'),
    path('answer/<int:answer_id>/add-like', views.addLike, name='addLike'),
    path('answer/<int:answer_id>/add-dislike', views.addDislike, name='addDislike')
]
