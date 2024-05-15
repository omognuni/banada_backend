from account.serializers.profile import (
    ProfileAnswerPatchSerializer,
    ProfileAnswerPostSerializer,
    ProfileAnswerSerializer,
    ProfilePostSerializer,
    ProfileSerializer,
)
from account.services.profile import ProfileService
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


@extend_schema_view(
    list=extend_schema(
        tags=["Profile"],
    ),
    retrieve=extend_schema(tags=["Profile"]),
    create=extend_schema(request=ProfilePostSerializer, tags=["Profile"]),
    partial_update=extend_schema(request=ProfilePostSerializer, tags=["Profile"]),
    answer=extend_schema(request=ProfileAnswerPostSerializer, tags=["Profile"]),
    update_answer=extend_schema(request=ProfileAnswerPatchSerializer, tags=["Profile"]),
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
        (profile, messages) = service.fetch_profile(id)
        output_serializer = ProfileSerializer(profile)
        data = output_serializer.data["match_type"] = messages
        return Response(status=status.HTTP_200_OK, data=data)

    def partial_update(self, request):
        """
        자신의 프로필을 업데이트
        """
        input_serializer = ProfileSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = ProfileService(user=request.user)
        profile = service.update_my_profile(input_serializer.validated_data)

        output_serializer = ProfilePostSerializer(profile)
        return Response(status=status.HTTP_200_OK, data=output_serializer.data)

    def create(self, request):
        """
        자신의 프로필을 생성
        """
        input_serializer = ProfilePostSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = ProfileService(user=request.user)
        profile = service.create_my_profile(input_serializer.validated_data)

        output_serializer = ProfileSerializer(profile)
        return Response(status=status.HTTP_201_CREATED, data=output_serializer.data)

    def delete(self, request):
        """
        자신의 프로필을 삭제
        """
        service = ProfileService(user=request.user)
        service.delete_my_profile()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["POST"], detail=False)
    def answer(self, request):
        """
        연애 시뮬레이션에 대한 답변을 등록
        """
        input_serializer = ProfileAnswerPostSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = ProfileService(user=request.user)
        answer = service.create_answer(input_serializer.validated_data)

        output_serializer = ProfileAnswerSerializer(answer)
        return Response(status=status.HTTP_201_CREATED, data=output_serializer.data)

    @action(methods=["PATCH"], detail=True)
    def update_answer(self, request, answer_id):
        """
        연애 시뮬레이션에 대한 답변을 수정
        """
        input_serializer = ProfileAnswerPatchSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = ProfileService(user=request.user)
        answer = service.update_answer(answer_id, input_serializer.validated_data)

        output_serializer = ProfileAnswerSerializer(answer)
        return Response(status=status.HTTP_200_OK, data=output_serializer.data)
