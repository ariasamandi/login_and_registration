from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process/register$', views.process_register),
    url(r'^process/login$', views.process_login),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout)
]
