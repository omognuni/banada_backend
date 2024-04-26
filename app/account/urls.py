from account.views.profile import ProfileViewset
from django.urls import include, path
from rest_framework.routers import SimpleRouter

app_name = "account"

router = SimpleRouter()
router.register("profiles", ProfileViewset, "profile")

urlpatterns = [path("", include(router.urls))]
