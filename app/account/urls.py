from account.views.profile import ProfileViewset
from account.views.simulation import SimulationViewSet
from django.urls import include, path
from rest_framework.routers import SimpleRouter

app_name = "account"

router = SimpleRouter()
router.register("profiles", ProfileViewset, "profile")
router.register("simulations", SimulationViewSet, "simulation")

urlpatterns = [path("", include(router.urls))]
