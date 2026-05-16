# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('api/bug-list-html/', views.bug_list_partial, name='bug_list_partial'),
]