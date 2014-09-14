from django.conf.urls import patterns, include, url

from basketball import views

urlpatterns = patterns('',
                       # root '/'
                       url(r'^$', views.leagues, name='index'),
                       # include basketball app's urls
                       url(r'^basketball/', include('basketball.urls', namespace='basketball'))
                       )
