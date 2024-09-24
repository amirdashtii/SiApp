from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.validators import MinLengthValidator, EmailValidator
from siapp.users.models import BaseUser
from siapp.users.validators import letter_validator, number_validator, special_char_validator

from drf_spectacular.utils import extend_schema


class registerApi(APIView):

    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField(EmailValidator())
        password = serializers.CharField(
            validators=[
                letter_validator,
                number_validator,
                special_char_validator,
                MinLengthValidator(limit_value=8)
            ]
        )
        confirm_password = serializers.CharField(max_length=255)

        def validate_email(self, email):
            if BaseUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email already exists")

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Password is required")

            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("Password does not match")

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
