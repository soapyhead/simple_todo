from django.conf.urls import url
from custom_user.views import (
    CreateUserView, LoginUserView, LogoutUserView, UserView
)

urlpatterns = [
    url(r'^sign_up/$', CreateUserView.as_view()),
    url(r'^login/$', LoginUserView.as_view()),
    url(r'^logout/$', LogoutUserView.as_view()),
    url(r'^profile/$', UserView.as_view()),
]
