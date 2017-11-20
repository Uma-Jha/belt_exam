from django.conf.urls import url
from . import views

urlpatterns = [
	url(r"^$", views.index),
	url(r"^register$", views.register),
    url(r"^login$", views.login),
	url(r"^friends$", views.friends),
	url(r'^addFriend/(?P<no>\d+)/$', views.addFriend),
	url(r'^removeFriend/(?P<no>\d+)/$', views.removeFriend),
	url(r'^user/(?P<no>\d+)/$', views.viewUser),
]