from django.urls import path
from .views import hook

urlpatterns = [
    path('hook', hook),
]
