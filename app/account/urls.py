from account.views.profile import ProfileViewSet
from account.views.simulation import SimulationViewSet
from account.views.user import UserViewSet
from django.urls import include, path
from rest_framework.routers import SimpleRouter

app_name = "account"

router = SimpleRouter()
router.register("profiles", ProfileViewSet, "profile")
router.register("simulations", SimulationViewSet, "simulation")
router.register("users", UserViewSet, "user")

urlpatterns = [path("", include(router.urls))]
