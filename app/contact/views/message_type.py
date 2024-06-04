from contact.models import MessageType
from contact.serializers.message import MessageTypeSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets


@extend_schema(tags=["message"])
class MessageTypeViewSet(viewsets.ModelViewSet):
    queryset = MessageType.objects.all()
    serializer_class = MessageTypeSerializer
