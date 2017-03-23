from django.conf.urls import url

from . import controller

urlpatterns = [
    url(r'^adduser$', controller.adduser),
    url(r'^verify$', controller.verify),
    url(r'^login$', controller.login),
    url(r'^logout$', controller.logout),
]