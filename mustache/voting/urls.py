from django.conf.urls import patterns, include, url

import voting.views

urlpatterns = patterns('',
    url(r'^test$', voting.views.test, name='test'),
    url(r'^signup$', voting.views.signup, name='signup'),
    url(r'^profile$', voting.views.profile, name='profile'),
    url(r'^login$', voting.views.login, name='login'),
    url(r'^logout$', voting.views.logout, name='logout'),
)
