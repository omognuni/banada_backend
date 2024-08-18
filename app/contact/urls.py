from contact.views.contact import ContactViewSet
from contact.views.message import MessageViewSet
from contact.views.message_type import MessageTypeViewSet
from django.urls import include, path
from rest_framework.routers import SimpleRouter

app_name = "contact"

router = SimpleRouter()
router.register(r"contact", ContactViewSet, "contact")
router.register(r"message", MessageViewSet, "message")
router.register(r"messagetype", MessageTypeViewSet, "messagetype")


urlpatterns = [path("", include(router.urls))]
