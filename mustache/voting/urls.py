from django.conf.urls import patterns, include, url

import voting.views

urlpatterns = patterns('',
    url(r'^test$', voting.views.test, name='test'),
)
