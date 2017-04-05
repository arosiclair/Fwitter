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
    url(r'^follow$', controller.follow),
    url(r'^user/(?P<username>[a-zA-Z0-9]+)', controller.getUserInfo),
    url(r'^user/(?P<username>[a-zA-Z0-9]+)/followers', controller.getUserFollowers),
    url(r'^user/(?P<username>[a-zA-Z0-9]+)/following', controller.getUserFollowing),
]
