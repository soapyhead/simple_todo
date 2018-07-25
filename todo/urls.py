from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import TodoModelViewSet

router = DefaultRouter()
router.register(r'', TodoModelViewSet, base_name='todos')

urlpatterns = [
    url(r'^', include(router.urls), name='todos'),
]