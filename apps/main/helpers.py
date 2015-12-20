#!/usr/bin/env python
# -*- coding: utf-8 -*-

APP_TITLE = 'Your website name'


def main_context_proc(request):
    """ A context processor for each view
    """

    return {
        "app_title": APP_TITLE,
        'server_addr': ('https://' if request.is_secure() else 'http://') + request.META['HTTP_HOST']
    }
