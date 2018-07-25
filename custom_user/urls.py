from django.conf.urls import url
from custom_user.views import (
    CreateUserView, LoginUserView, LogoutUserView, UserView
)

urlpatterns = [
    url(r'^sign_up/$', CreateUserView.as_view(), name='sign_up'),
    url(r'^login/$', LoginUserView.as_view(), name='login'),
    url(r'^logout/$', LogoutUserView.as_view(), name='logout'),
    url(r'^profile/$', UserView.as_view(), name='profile'),
]
