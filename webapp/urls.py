from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'img/favicon.ico', permanent=True)),
    url(r'^admin/', include(admin.site.urls)),

    # AUTH
    url(r'^security/', include('apps.security.urls')),
    # url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^', include('apps.main.urls')),
    url(r'^', include('apps.test_app.urls')),
)

# IGNORABLE_404_URLS has been moved to logger

handler400 = 'apps.logger.views.bad_request_view'
handler403 = 'apps.logger.views.permission_denied_view'
handler404 = 'apps.logger.views.page_not_found_view'
handler500 = 'apps.logger.views.server_error_view'
