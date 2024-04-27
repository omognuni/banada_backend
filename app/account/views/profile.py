from account.serializers.profile import ProfilePostSerializer, ProfileSerializer
from account.services.profile import ProfileService
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


@extend_schema_view(
    list=extend_schema(
        description="요청을 보낸 유저의 프로필(마이페이지 - 나의 프로필)을 조회"
    ),
    retreive=extend_schema(description="다른 유저의 프로필을 조회"),
    create=extend_schema(request=ProfilePostSerializer),
)
class ProfileViewset(viewsets.GenericViewSet):
    serializer_class = ProfileSerializer

    def list(self, request):
        """
        요청을 보낸 유저의 프로필(마이페이지 - 나의 프로필)을 조회
        """
        service = ProfileService(user=request.user)
        profile = service.fetch_my_profile()
        output_serializer = ProfileSerializer(profile)

        return Response(status=status.HTTP_200_OK, data=output_serializer.data)

    def retrieve(self, request, id):
        """
        다른 유저의 프로필을 조회
        """
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
