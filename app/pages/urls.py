from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('testconnect', views.testIBconnect, name='testconnect'),
    path('profile', views.memberProfile, name='memberProfile'),
    path('faq', views.faq, name='faq'),
    path('services', views.services, name='services'),
    path('ibgatewayconfig', views.ibgatewayconfig, name='ibgatewayconfig'),
    path('hostnameconfig', views.hostnameconfig, name='hostnameconfig'),
]
