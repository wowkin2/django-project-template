#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import redirect

from apps.test_app.views import view_about, view_profile


def view_main(request):
    if request.user.is_authenticated():
        return redirect(view_profile)
    else:
        return redirect(view_about)
