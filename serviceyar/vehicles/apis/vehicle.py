from drf_spectacular.utils import extend_schema
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from serviceyar.api.mixins import ApiAuthMixin
from serviceyar.vehicles.models import Vehicle
from serviceyar.vehicles.validators import validate_year
from serviceyar.vehicles.selectors.vehicle import get_vehicle_list, get_vehicle_by_id
from serviceyar.vehicles.services.vehicles import create_vehicle


class VehicleApi(ApiAuthMixin, APIView):

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=False)
        model_id    = serializers.IntegerField(required=True)
        color = serializers.CharField(max_length=255, required=False)
        year = serializers.IntegerField(
            validators=[validate_year], required=False)
        plate_number = serializers.CharField(max_length=255, required=False)
        mileage = serializers.IntegerField(required=False)
        insurance_date = serializers.DateField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField('get_user')
        model = serializers.SerializerMethodField("get_model")

        class Meta:
            model = Vehicle
            fields = ('id', 'user', 'name', 'model',
                      'color', 'year', 'plate_number', 'mileage', 'insurance_date')

        def get_user(self, vehicle):
            return vehicle.user.email

        def get_model(self, vehicle):
            return vehicle.model.name

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        try:
            query = get_vehicle_list(user=request.user)
        except Exception as ex:
            return Response(
                {"error": f"Database Error: {str(ex)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputSerializer(query, many=True).data,
                        status=status.HTTP_200_OK)

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def post(self, request):
        serializers = self.InputSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        try:
            vehicle = create_vehicle(
                user=request.user,
                model_id=serializers.validated_data.get(
                    "model_id"),
                name=serializers.validated_data.get("name"),
                color=serializers.validated_data.get("color"),
                year=serializers.validated_data.get("year"),
                plate_number=serializers.validated_data.get("plate_number"),
                mileage=serializers.validated_data.get("mileage"),
                insurance_date=serializers.validated_data.get("insurance_date")
            )
        except Exception as ex:
            return Response(
                f"Database Error: {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputSerializer(vehicle, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)


class VehicleDetailApi(ApiAuthMixin, APIView):

    class OutputSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField('get_user')
        model = serializers.SerializerMethodField("get_model")

        class Meta:
            model = Vehicle
            fields = ('id', 'user', 'name', 'model',
                      'color', 'year', 'plate_number', 'mileage', 'insurance_date')

        def get_user(self, vehicle):
            return vehicle.user.email

        def get_model(self, vehicle):
            return vehicle.model.name

    @extend_schema(responses=OutputSerializer)
    def get(self, request, vehicle_id):
        try:
            vehicle = get_vehicle_by_id(
                user=request.user, vehicle_id=vehicle_id)
        except Exception as ex:
            return Response(
                {"error": f"Database Error: {str(ex)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputSerializer(vehicle).data,
                        status=status.HTTP_200_OK)
