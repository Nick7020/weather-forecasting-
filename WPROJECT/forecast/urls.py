from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # This points the home page to your weather logic
]