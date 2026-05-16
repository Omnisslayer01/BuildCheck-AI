from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('api/update-status/', views.update_bug_status, name='update_bug_status'),
]

# Made with Bob
