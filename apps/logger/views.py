#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import md5
import socket
import traceback
import re
import warnings

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext, Context
from django.views.decorators.cache import cache_control
from django.conf import settings

from apps.main.helpers import main_context_proc


# DEBUG_SERVER = 'python -m smtpd -n -c DebuggingServer localhost:1025'
MESSAGE = {
    400: 'Неправильний запит!',
    403: 'У вас немає прав доступу до цієї сторінки!',
    404: 'Сторінку не знайдено!',
    500: 'Помилка на сервері!',
}
IGNORABLE_404_URLS = (
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/browserconfig\.xml$'),
    re.compile(r'.*\.(php|cgi)$'),
    re.compile(r'^/phpmyadmin'),
)
BotNames = ['Googlebot', 'Slurp', 'Twiceler', 'msnbot', 'KaloogaBot', 'YodaoBot',
            '"Baiduspider', 'googlebot', 'Speedy Spider', 'DotBot', 'YandexBot']


def is_bot(user_agent):
    for botname in BotNames:
        if botname in user_agent:
            return True
    return False


def send_notification(context):
    subject = "{} Error page {} - {}".format(
        settings.EMAIL_SUBJECT_PREFIX, context.get('err_code'), context.get('err_message'))

    from_email = settings.DEFAULT_FROM_EMAIL
    recipients = ['pidvezy.org@gmail.com']
    cc = None  # []
    bcc = None  # []
    attachments = None
    if 'traceback' in context:
        attachments = [('traceback.txt', context['traceback'], 'text/plain')]

    t = get_template('email/error_notification.html')
    body = t.render(Context(context))

    message = EmailMessage(subject=subject, body=body, from_email=from_email,
                           to=recipients, bcc=bcc, cc=cc, attachments=attachments)
    message.content_subtype = "html"
    message.send(fail_silently=False)

    print "=====  Logger Email sent successfully! ====="


def prepare_email_context(request, exception=None, err_code=500):
    try:
        context = dict({
            'request': request,
            'datetime': datetime.now(),
            'url': request.build_absolute_uri(),
            'server_name': socket.gethostname(),
            # 'user_fb': getattr(get_fb_user(request), "uid", ''),
            'err_code': err_code,
            'user_agent': request.META.get('HTTP_USER_AGENT', None),
            'is_bot': is_bot(request.META.get('HTTP_USER_AGENT', None))
        })
        if err_code != 404:
            tb_text = traceback.format_exc()
            context['traceback'] = tb_text
            context['checksum'] = md5(tb_text).hexdigest()
            err_message_default = tb_text.rstrip('\n').split('\n')[-1]
        else:
            err_message_default = "Couldn't dispatch url."
        context['err_message'] = getattr(exception, "message",
                                         err_message_default)

        send_notification(context)
    except Exception as e:
        warnings.warn(unicode(e))


class ExceptionLoggingMiddleware(object):

    def __init__(self):
        pass

    def process_exception(self, request, exception):
        prepare_email_context(request, exception)


# #############################################################################
# Error page handlers (400, 403, 404, 500)
# #############################################################################

@cache_control(max_age=1)
def base_error_handler(request, err_code):
    if any(re.match(x, request.path) for x in IGNORABLE_404_URLS):
        print "404 Not found: %s. Present in ignorable list. " % request.path
    else:
        print "404 Not found: %s. Will send mail notification. " % request.path
        prepare_email_context(request, err_code=err_code)

    t = get_template('base_error_page.html')
    c = RequestContext(request, {
        'err_code': err_code,
        'message': MESSAGE[err_code],
        'page_name': 'Помилка на сторінці'
    }, processors=[main_context_proc])

    html = t.render(c)
    return HttpResponse(html)


def bad_request_view(request):
    return base_error_handler(request, 400)


def permission_denied_view(request):
    return base_error_handler(request, 403)


def page_not_found_view(request):
    return base_error_handler(request, 404)


def server_error_view(request):
    return base_error_handler(request, 500)


def view_main(request):
    return HttpResponse('Nothing to show')
