from django.conf.urls import url, include
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='TODO API')


urlpatterns = [
    url(r'^', include('custom_user.urls')),
    url(r'^todos/', include('todo.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^auth/', include('rest_framework.urls')),
        url(r'^docs/$', schema_view),
    ]