from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, DetailView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='home'),

	url(r'^admin/', include(admin.site.urls))
)

if settings.DEBUG:
	urlpatterns += staticfiles_urlpatterns()