from django.conf.urls import patterns, url

from cc_app import views as ccviews

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^upload/', ccviews.upload, name='upload'),
    url(r'^detail/(?P<slug>[-\w]+)/', ccviews.detail, name='detail'),
)
