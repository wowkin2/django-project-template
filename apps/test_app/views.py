#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext

from apps.main.helpers import main_context_proc


def view_about(request):
    t = get_template('index.html')
    c = RequestContext(request, {
        "items": []
    }, processors=[main_context_proc])

    html = t.render(c)
    return HttpResponse(html)


@login_required
def view_profile(request):
    t = get_template('profile.html')
    c = RequestContext(request, {
        "items": []
    }, processors=[main_context_proc])

    html = t.render(c)
    return HttpResponse(html)
