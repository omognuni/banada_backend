from contact.views.message import MessageViewset
from django.urls import include, path
from rest_framework.routers import SimpleRouter

app_name = "contact"

router = SimpleRouter()
router.register(r"message", MessageViewset, "message")


urlpatterns = [path("", include(router.urls))]
