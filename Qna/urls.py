from django.contrib import admin
from django.urls import path
from ask_me import views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.save, name='save'),
    path('search/', include('ask_me.urls')),
    path('lastest-questions', views.lastestQuestions, name='lastedQuestions')
]
