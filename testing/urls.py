from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('api/update-status/', views.update_bug_status, name='update_bug_status'),
    path('api/bug-list-html/', views.bug_list_partial, name='bug_list_partial'),
]

# Made with Bob
