from contact.serializers.message import MessagePostSerializer, MessageSerializer
from contact.services.message import MessageService
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


@extend_schema(tags=["message"])
class MessageViewset(viewsets.GenericViewSet):
    serializer_class = MessageSerializer

    @action(methods=["GET"], detail=False)
    def received(self, request):
        """
        페이지 - 하트/내가 받은 반지/하트

        TODO - 서로 받은 경우 표시
        """

        service = MessageService(request.user)
        messages = service.fetch_received_messages()
        output_serializer = self.get_serializer(messages, many=True)

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def sent(self, request):
        """
        페이지 - 하트/내가 보낸 반지/하트

        """
        service = MessageService(request.user)
        messages = service.fetch_sent_messages()
        output_serializer = self.get_serializer(messages, many=True)

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=MessagePostSerializer)
    def create(self, request):
        """
        페이지 - 연락탭
        """

        input_serializer = MessagePostSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = MessageService(request.user)
        message = service.send_message(input_serializer.validated_data)

        output_serializer = self.get_serializer(message)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
