from django.urls import path
from explorer.views import (
    Applications,
    ApplicationDetail,
    Users,
    UsersRegister,
    UserDetail,
)

urlpatterns = [
    path("applications", Applications.as_view()),
    path("applications/<int:id>", ApplicationDetail.as_view()),
    path("creators", Users.as_view()),
    path("register", UsersRegister.as_view()),
    path("creators/<int:userid>", UserDetail.as_view()),
]
