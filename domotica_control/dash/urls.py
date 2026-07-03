from django.urls import path
from . import views 

app_name = 'dash'
urlpatterns = [
    path('', views.home, name='home'),
    path('dash_post/', views.post, name='post'),
    path('ai_calls/', views.ai_calls, name='ai_calls')
]
