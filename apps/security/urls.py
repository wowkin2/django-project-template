from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.view_login_page, name='login'),
    url(r'^login/', views.handle_login, name='login_act'),
    url(r'^logout/', views.handle_logout, name='logout_act'),
)