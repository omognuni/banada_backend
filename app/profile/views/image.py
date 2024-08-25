from profile.models import ProfileImage
from profile.serializers.profile import ProfileImageSerializer

from rest_framework.viewsets import ModelViewSet


class ImageViewSet(ModelViewSet):
    queryset = ProfileImage.objects.all()
    serializer_class = ProfileImageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile__user=self.request.user)
        return queryset
