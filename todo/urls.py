from django.conf import settings
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view
from .views import TodoModelViewSet


schema_view = get_swagger_view(title='TODO API')

router = DefaultRouter()
router.register(r'', TodoModelViewSet, base_name='todos')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include('custom_user.urls')),
    url(r'^todos/', include('todo.urls')),

]

if settings.DEBUG:
    urlpatterns += [
        url(r'^auth/', include('rest_framework.urls')),
        url(r'^docs/$', schema_view),
    ]