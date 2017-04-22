from django.conf.urls import url

from . import views

urlpatterns = [
    # maps an empty string to  function views.index name is the name that will be used to identify the view
    url(r'', views.index, name='index'),
]
