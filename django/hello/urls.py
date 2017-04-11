from django.conf.urls import url

from . import views

urlpatterns = [
    # maps an empty string to  function views.index name is the name that will be used to identify the view
    url(r'^$', views.index, name='index'),
    url(r'^calendar/([0-9]{4})/([0-9]{2})/$', views.calendar),
    url(r'^(?P<user_id>[0-9]+)/$', views.display_user, name='display_user'),
]