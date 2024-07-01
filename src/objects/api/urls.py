from django.urls import include, path

urlpatterns = [
    path("v1", include("objects.api.v1.urls", namespace="v1")),
    path("v2", include("objects.api.v2.urls", namespace="v2")),
]
