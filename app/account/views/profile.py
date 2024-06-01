from account.serializers.profile import (
    ProfileAnswerPatchSerializer,
    ProfileAnswerPostSerializer,
    ProfileAnswerSerializer,
    ProfileAnswerValueSerializer,
    ProfileDetailSerializer,
    ProfileListSerializer,
    ProfilePostSerializer,
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
    answer=extend_schema(
        request=ProfileAnswerPostSerializer,
        responses=ProfileAnswerSerializer,
        tags=["Profile"],
    ),
    update_answer=extend_schema(
        request=ProfileAnswerPatchSerializer,
        responses=ProfileAnswerSerializer,
        tags=["Profile"],
    ),
    today=extend_schema(tags=["Profile"], responses=ProfileListSerializer),
)
class ProfileViewSet(viewsets.GenericViewSet):
    serializer_class = ProfileDetailSerializer

    def list(self, request):
        """
        전체 프로필 조회(관리자만 사용 가능)

        TODO - 관리자만 조회 가능
        """
        service = ProfileService(user=request.user)
        profile = service.fetch_profiles()
        output_serializer = ProfileListSerializer(profile, many=True)

        return Response(status=status.HTTP_200_OK, data=output_serializer.data)

    @action(methods=["GET"], detail=False)
    def my(self, request):
        """
        페이지 - 마이 페이지

        요청을 보낸 유저의 프로필(마이페이지 - 나의 프로필)을 조회
        """
        service = ProfileService(user=request.user)
        profile = service.fetch_my_profile()
        output_serializer = ProfileDetailSerializer(profile)

        return Response(status=status.HTTP_200_OK, data=output_serializer.data)

    def retrieve(self, request, pk):
        """
        페이지 - 홈, 하트/상세프로필

        다른 유저의 프로필을 조회
        다른 유저가 보낸 하트/반지 표시
        다른 유저와 나의 궁합
        """
        service = ProfileService(user=request.user)
        (profile, messages) = service.fetch_profile(pk)
        output_serializer = ProfileDetailSerializer(profile)
        output_serializer.data["message_type"] = messages
        return Response(status=status.HTTP_200_OK, data=output_serializer.data)

    def partial_update(self, request, pk):
        """
        페이지 - 마이페이지 프로필 수정, 자기 소개 수정

        자신의 프로필을 업데이트
        """
        input_serializer = ProfileDetailSerializer(data=request.data)
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

        output_serializer = ProfileDetailSerializer(profile)
        return Response(status=status.HTTP_201_CREATED, data=output_serializer.data)

    def delete(self, request, pk):
        """
        자신의 프로필을 삭제
        """
        service = ProfileService(user=request.user)
        service.delete_my_profile()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["GET"], detail=False)
    def today(self, request):
        """
        페이지 - 메인홈 / 홈 1

        하루에 네 번 랜덤으로 소개
        """
        service = ProfileService(user=request.user)
        try:
            profiles = service.fetch_random_profiles()
            # Debugging: Print or log the fetched profiles
            print(f"Fetched Profiles: {profiles}")

            output_serializer = ProfileListSerializer(profiles, many=True)
            return Response(status=status.HTTP_200_OK, data=output_serializer.data)
        except Exception as e:
            # Debugging: Print or log the exception
            print(f"Error: {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": str(e)})

    @action(methods=["POST"], detail=False)
    def answer(self, request):
        """
        페이지 - 연애 시뮬레이션

        연애 시뮬레이션에 대한 답변을 등록
        """
        input_serializer = ProfileAnswerPostSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = ProfileService(user=request.user)
        answer = service.create_answer(input_serializer.validated_data)

        output_serializer = ProfileAnswerSerializer(answer)
        return Response(status=status.HTTP_201_CREATED, data=output_serializer.data)

    @action(methods=["PATCH"], detail=True)
    def update_answer(self, request, pk):
        """
        페이지 - 연애 시뮬레이션

        연애 시뮬레이션에 대한 답변을 수정
        """
        input_serializer = ProfileAnswerPatchSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = ProfileService(user=request.user)
        answer = service.update_answer(pk, input_serializer.validated_data)

        output_serializer = ProfileAnswerSerializer(answer)
        return Response(status=status.HTTP_200_OK, data=output_serializer.data)

    @action(methods=["GET"], detail=True)
    def values(self, request, pk):
        """
        페이지 - 가치관 페이지
        """
        service = ProfileService(user=request.user)
        match_result = service.match_answer(pk)

        output_serializer = ProfileAnswerValueSerializer(match_result, many=True)
        return Response(status=status.HTTP_200_OK, data=output_serializer.data)
