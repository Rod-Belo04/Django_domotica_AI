from django.urls import path
from . import views 

app_name = 'dash'
url_patterns = [
    path('', views.home, name='home'),
    path('dash_post/', views.post, name='post')
]