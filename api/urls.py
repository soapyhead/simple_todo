from django.conf.urls import url, include
from django.conf import settings


urlpatterns = [
    url(r'^/', include('custom_user.urls')),
    url(r'^todos/', include('todo.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^auth/', include('rest_framework.urls')),
    ]