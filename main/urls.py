from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.view_main, name='main'),
)
