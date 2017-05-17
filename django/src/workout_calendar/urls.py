import datetime

from django.conf.urls import url

from . import views

urlpatterns = [
    # maps an empty string to  function views.index name is the name that will be used to identify the view
    # the more detailed one should be the first argument!
    url(r'^display_form$', views.display_form, name='display_form'),
    url(r'^([0-9]{4})/([0-9]{2})/$', views.calendar),
    url(r'', views.calendar, {'year': str(datetime.datetime.now().year), 'month': str(datetime.datetime.now().month)},
        name='calendar'),
]
