from django.urls import path, include

from . import views
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'openstack', views.ChurmHubViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('index/', views.index, name='index'),
    path('api-openstack/', include('rest_framework.urls', namespace='rest_framework')),
]