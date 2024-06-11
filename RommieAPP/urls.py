from django.urls import path
from . import views

urlpatterns = [
    path('UserInsert',views.UserInsert_f),
]