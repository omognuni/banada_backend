from account.serializers.profile import ProfilePostSerializer, ProfileSerializer
from account.services.profile import ProfileService
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ProfileViewset(viewsets.GenericViewSet):
    serializer_class = ProfileSerializer

    def list(self, request):
        service = ProfileService(user=request.user)
        profile = service.fetch_my_profile()
        output_serializer = ProfileSerializer(profile)

        return Response(status=status.HTTP_200_OK, data=output_serializer.data)

    def retrieve(self, request, id):
        service = ProfileService(user=request.user)
        profile = service.fetch_profile(id)
        output_serializer = ProfileSerializer(profile)
        return Response(status=status.HTTP_200_OK, data=output_serializer.data)

    def update(self, request):
        input_serializer = ProfileSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = ProfileService(user=request.user)
        profile = service.update_my_profile(input_serializer.validated_data)

        output_serializer = ProfilePostSerializer(profile)
        return Response(status=status.HTTP_200_OK, data=output_serializer.data)

    def create(self, request):
        input_serializer = ProfilePostSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = ProfileService(user=request.user)
        profile = service.create_my_profile(input_serializer.validated_data)

        output_serializer = ProfileSerializer(profile)
        return Response(status=status.HTTP_201_CREATED, data=output_serializer.data)

    def delete(self, request):
        service = ProfileService(user=request.user)
        service.delete_my_profile()

        return Response(status=status.HTTP_204_NO_CONTENT)
