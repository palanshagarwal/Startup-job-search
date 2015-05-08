from django.conf.urls import patterns, include, url
from django.contrib import admin
from search import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', 'search.views.index'),
    # Examples:
    # url(r'^$', 'angelapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
     url(r'^search/', include('search.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
