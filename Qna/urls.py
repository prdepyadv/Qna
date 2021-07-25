from django.contrib import admin
from django.urls import path
from ask_me import views as ak_views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout', ak_views.logoutUser, name='logout'),
    path('login', ak_views.loginUser, name='login'),
    path('', ak_views.index, name='home'),
    path('search/', include('ask_me.urls')),
    path('key/', ak_views.find, name='find'),
    path('lastest-10', ak_views.lastestQuestions, name='lastedQuestions'),
    path('answer/update/', ak_views.updateAnswer, name='updateAnswer'),
    path('answer/delete/', ak_views.deleteAnswer, name='deleteAnswer'),
    path('answer/save-new/', ak_views.saveAnswer, name='saveAnswer'),
    path('answer/<int:answer_id>/add-like', ak_views.addLike, name='addLike'),
    path('answer/<int:answer_id>/add-dislike',
         ak_views.addDislike, name='addDislike')
]
