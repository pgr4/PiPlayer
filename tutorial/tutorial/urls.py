from django.conf.urls import url, include
from rest_framework import routers
from tutorial.quickstart import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^queue', views.queue),
    url(r'^stop', views.stop),
    url(r'^next', views.next),
    url(r'^prev', views.prev),
    url(r'^pause', views.pause),
    url(r'^play', views.play)

]