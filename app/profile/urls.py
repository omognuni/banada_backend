from profile.views.image import ImageViewSet
from profile.views.profile import ProfileViewSet
from profile.views.simulation import SimulationViewSet
from profile.views.user import UserViewSet

from django.urls import include, path
from rest_framework.routers import SimpleRouter

app_name = "profile"

router = SimpleRouter()
router.register("profiles", ProfileViewSet, "profile")
router.register("images", ProfileViewSet, "image")
router.register("simulations", SimulationViewSet, "simulation")
router.register("users", UserViewSet, "user")

urlpatterns = [path("", include(router.urls))]
