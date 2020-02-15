from django.urls import path

from . import views

urlpatterns = [
    path('makepayment/', views.HomePageView.as_view(), name='home'), #david007
    #path('listings/', views.HomePageView.as_view(), name='home'),
    path('charge/', views.charge, name='charge'), # new
]