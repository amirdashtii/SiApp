from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from siapp.users.models import BaseUser

from drf_spectacular.utils import extend_schema


class registerApi(APIView):

    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        password = serializers.CharField(max_length=255)
        confirm_password = serializers.CharField(max_length=255)

    class OutputRegisterSerializer(serializers.Serializer):
        class Meta:
            model = BaseUser
            fields = ('id', 'email')

    @extend_schema(request=InputRegisterSerializer, responses=OutputRegisterSerializer)
    def post(self, request):
        serializers = self.InputRegisterSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        try:
            query = create_user(
                email=serializers.validated_data.get("email"),
                password=serializers.validated_data.get("password"),
            )
        except Exception as ex:
            return Response(
                f"Database Error: {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputRegisterSerializer(query, context={'request': request}).data)
