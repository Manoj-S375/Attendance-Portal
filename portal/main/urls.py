from django.urls import path
from . import views

urlpatterns = [
    path('',views.login, name = "login"),
    path('detail/', views.details, name = "detail"),
    path('attend/', views.attend, name="attend"),
    path('seeatt/',views.seeatt, name ="seeatt"),
    path('sumy/',views.sumy, name="sumy"),
]