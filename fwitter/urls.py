from django.conf.urls import url

from . import controller

urlpatterns = [
    url(r'^$', controller.index),
    url(r'^adduser$', controller.adduser),
    url(r'^verify$', controller.verify),
    url(r'^login$', controller.login),
    url(r'^logout$', controller.logout),
    url(r'^additem$', controller.additem),
    url(r'^item/(?P<tweetId>[a-z0-9]+)$', controller.getitem),
    url(r'^search$', controller.search),
]