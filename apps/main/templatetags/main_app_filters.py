#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def static_version(path):
    """ Returns absolute URL to static file with versioning.
    """
    full_path = os.path.join(os.path.abspath(settings.STATICFILES_DIRS[0]), os.path.normpath(path))
    try:
        # Get file modification time.
        mtime = os.path.getmtime(full_path)
        return '%s%s?%s' % (settings.STATIC_URL, path, mtime)
    except OSError:
        # Returns normal url if this file was not found in filesystem.
        return '%s%s' % (settings.STATIC_URL, path)
