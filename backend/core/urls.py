from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("tasks", views.TaskViewSet, basename="task")
router.register("events", views.EventViewSet, basename="event")
router.register("routines", views.RoutineViewSet, basename="routine")

urlpatterns = [
    path("health/", views.health_check, name="health-check"),
    path("", include(router.urls)),
]
