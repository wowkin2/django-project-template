#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings


def debug(context):
    return {'DEBUG': settings.DEBUG}
