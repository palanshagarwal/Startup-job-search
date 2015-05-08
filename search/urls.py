from django.conf.urls import patterns, url
from search import views
urlpatterns = patterns('',
    url(r'^formData', views.form_processing, name='form_processing'),
)