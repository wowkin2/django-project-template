#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib import admin

from . import views


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', views.view_main, name='logs_main'),
)
