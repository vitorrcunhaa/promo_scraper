from django.contrib.auth.decorators import login_required
from django.urls import path

from core import views

urlpatterns = [
    path('', login_required(views.index), name='index'),
]
