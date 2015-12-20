#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib import admin

from . import views


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^about', views.view_about, name='about'),
    url(r'^profile', views.view_profile, name='profile'),
)
