
from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path('', views.main, name = "main"),
    path('<int:page>', views.main, name = "root_paginate"),
    path('add_author/', views.author, name='author'),
    path('add_quote/', views.quote, name='quote'),
    path('author/<str:author_id>/', views.author_info, name='author_info')
]   
