from django.conf.urls import url

from . import views

urlpatterns = [
    # maps an empty string to  function views.index name is the name that will be used to identify the view
    # the more detailed one should be the first argument!
    url(r'^([0-9]{4})/([0-9]{2})/$', views.calendar),
    url(r'', views.calendar, {'year': '2017', 'month': '04'}, name='index'),
]
