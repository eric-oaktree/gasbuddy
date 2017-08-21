from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

urlpatterns = [
    url(r'^site_an/$', views.site_an, name='site_an'),
    url(r'^sites/$', views.sites, name='sites'),
    url(r'^setup_site/$', views.setup_site, name='setup_site'),
    url(r'^pull_prices/$', views.pull_prices, name='pull_prices'),
    url(r'^wipe_db/$', views.wipe_db, name='wipe_db'),
    url(r'^about/$', views.about, name='about'),
    url(r'^$', views.home, name='home'),
]
