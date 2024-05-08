from contact.serializers.message import MessagePostSerializer, MessageSerializer
from contact.services.message import MessageService
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class MessageViewset(viewsets.GenericViewSet):
    serializer_class = MessageSerializer

    @action(methods=["GET"], detail=False)
    def received(self, request):
        service = MessageService(request.user)
        messages = service.fetch_received_messages()
        output_serializer = self.get_serializer(messages, many=True)

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def sent(self, request):
        service = MessageService(request.user)
        messages = service.fetch_sent_messages()
        output_serializer = self.get_serializer(messages, many=True)

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        input_serializer = MessagePostSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = MessageService(request.user)
        message = service.send_message(input_serializer.validated_data)

        output_serializer = self.get_serializer(message)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)