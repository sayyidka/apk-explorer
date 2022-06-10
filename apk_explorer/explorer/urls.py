from django.urls import path
from explorer.views import Applications, ApplicationDetail

urlpatterns = [
    path("applications", Applications.as_view()),
    path("applications/<int:id>", ApplicationDetail.as_view()),
]
