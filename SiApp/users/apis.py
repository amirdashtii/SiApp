from django.core.validators import MinLengthValidator, EmailValidator
from drf_spectacular.utils import extend_schema
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView


from siapp.api.mixins import ApiAuthMixin
from siapp.users.models import BaseUser, Profile
from siapp.users.selectors import get_profile
from siapp.users.services import register
from siapp.users.validators import letter_validator, number_validator, special_char_validator


class ProfileApi(ApiAuthMixin, APIView):

    class OutputProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ('first_name', 'last_name', 'birthdate', 'phone_number')

    @extend_schema(responses=OutputProfileSerializer)
    def get(self, request):
        query = get_profile(user=request.user)
        return Response(self.OutputProfileSerializer(query, context={'request': request}).data)


class RegisterApi(APIView):

    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField(validators=[EmailValidator()])
        first_name = serializers.CharField(max_length=255, required=False)
        last_name = serializers.CharField(max_length=255, required=False)
        birthdate = serializers.DateField(required=False)
        phone_number = serializers.CharField(max_length=255, required=False)

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
            return email

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Password is required")

            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("Password does not match")
            return data

    class OutputRegisterSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ('id', 'email')

    @extend_schema(request=InputRegisterSerializer, responses=OutputRegisterSerializer)
    def post(self, request):
        serializers = self.InputRegisterSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        try:
            user = register(
                email=serializers.validated_data.get("email"),
                password=serializers.validated_data.get("password"),
                first_name=serializers.validated_data.get("first_name"),
                last_name=serializers.validated_data.get("last_name"),
                birthdate=serializers.validated_data.get("birthdate"),
                phone_number=serializers.validated_data.get("phone_number")
            )
        except Exception as ex:
            return Response(
                f"Database Error: {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputRegisterSerializer(user, context={'request': request}).data)
