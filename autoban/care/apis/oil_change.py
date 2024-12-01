from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView


from autoban.api.mixins import ApiAuthMixin
from autoban.care.models import OilChange
from autoban.care.validators import oil_change_validator, oil_change_update_validator
from autoban.care.selectors.care import (
    get_oil_change_list,
    get_oil_change_vehicle_list,
    get_oil_change_by_id,
    get_last_oil_change
)
from autoban.care.services.care import (
    create_oil_change,
    update_oil_change,
    delete_oil_change
)


class OilChangeListCreateApi(ApiAuthMixin, APIView):

    class InputSerializer(serializers.Serializer):
        user_id = serializers.UUIDField(required=True)
        vehicle_id = serializers.IntegerField(required=True)
        service_date = serializers.DateField(required=True)
        oil_type = serializers.CharField(max_length=255, required=False)
        mileage = serializers.IntegerField(required=True)
        oil_lifetime_distance = serializers.IntegerField(required=False)
        next_change_mileage = serializers.IntegerField(required=False)
        next_service_date = serializers.DateField(required=False)

        def validate(self, data):
            try:
                return oil_change_validator(data)
            except ValidationError as e:
                raise serializers.ValidationError(e)

    class OutputSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField('get_user')
        vehicle = serializers.SerializerMethodField("get_vehicle")

        class Meta:
            model = OilChange
            fields = ('id', 'user', 'vehicle', 'service_date', 'oil_type', 'mileage',
                      'oil_lifetime_distance', 'next_change_mileage', 'next_service_date')

        def get_user(self, oil_change):
            return oil_change.user.email

        def get_vehicle(self, oil_change):
            return oil_change.vehicle.name

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        try:
            query = get_oil_change_list(user=request.user)
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
            oil_change_data = {
                key: value for key, value in serializers.validated_data.items()
            }
            if not oil_change_data.get("next_change_mileage"):
                if not oil_change_data.get("oil_lifetime_distance"):
                    oil_change_data["oil_lifetime_distance"] = 5000

                oil_change_data["next_change_mileage"] = oil_change_data["mileage"] + \
                    oil_change_data["oil_lifetime_distance"]

            oil_change = create_oil_change(
                user=request.user, **oil_change_data)

        except Exception as ex:
            return Response(
                f"Database Error: {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputSerializer(oil_change, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)


class OilChangeVehicleListApi(ApiAuthMixin, APIView):

    class OutputSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField('get_user')
        vehicle = serializers.SerializerMethodField("get_vehicle")

        class Meta:
            model = OilChange
            fields = ('id', 'user', 'vehicle', 'service_date', 'oil_type', 'mileage',
                      'oil_lifetime_distance', 'next_change_mileage', 'next_service_date')

        def get_user(self, oil_change):
            return oil_change.user.email

        def get_vehicle(self, oil_change):
            return oil_change.vehicle.name

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        try:
            query = get_oil_change_vehicle_list(
                user=request.user, vehicle=request.vehicle)
        except Exception as ex:
            return Response(
                {"error": f"Database Error: {str(ex)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputSerializer(query, many=True).data,
                        status=status.HTTP_200_OK)


class OilChangeDetailApi(ApiAuthMixin, APIView):

    class InputSerializer(serializers.Serializer):
        user_id = serializers.UUIDField(required=False)
        vehicle_id = serializers.IntegerField(required=False)
        service_date = serializers.DateField(required=False)
        oil_type = serializers.CharField(max_length=255, required=False)
        mileage = serializers.IntegerField(required=False)
        oil_lifetime_distance = serializers.IntegerField(required=False)
        next_change_mileage = serializers.IntegerField(required=False)
        next_service_date = serializers.DateField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField('get_user')
        vehicle = serializers.SerializerMethodField("get_vehicle")

        class Meta:
            model = OilChange
            fields = ('id', 'user', 'vehicle', 'service_date', 'oil_type', 'mileage',
                      'oil_lifetime_distance', 'next_change_mileage', 'next_service_date')

        def get_user(self, oil_change):
            return oil_change.user.email

        def get_vehicle(self, oil_change):
            return oil_change.vehicle.name

    @extend_schema(responses=OutputSerializer)
    def get(self, request, oil_change_id):
        try:
            oil_change = get_oil_change_by_id(
                user=request.user, oil_change_id=oil_change_id)
        except Exception as ex:
            return Response(
                {"error": f"Database Error: {str(ex)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputSerializer(oil_change).data,
                        status=status.HTTP_200_OK)

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def put(self, request, oil_change_id):
        try:
            oil_change = get_oil_change_by_id(
                user=request.user, oil_change_id=oil_change_id)
        except Exception as ex:
            return Response(
                {"error": f"Database Error: {str(ex)}"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            oil_change_update_validator(oil_change, request.data)
        except ValidationError as e:
            raise serializers.ValidationError(e)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            updated_oil_change = update_oil_change(
                oil_change=oil_change,
                **serializer.validated_data
            )
        except Exception as ex:
            return Response(
                {"error": f"Update Error: {str(ex)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"updated": "update was successful"},
            status=status.HTTP_200_OK)

    @extend_schema(responses=None)
    def delete(self, request, oil_change_id):
        try:
            oil_change = get_oil_change_by_id(
                user=request.user, oil_change_id=oil_change_id)
        except Exception as ex:
            return Response(
                {"error": f"Database Error: {str(ex)}"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            delete_oil_change(oil_change)
        except Exception as ex:
            return Response(
                {"error": f"Database ErrorL {str(ex)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"deleted": "delete was successful"},
            status=status.HTTP_200_OK
        )


class LastOilChangeDetailApi(ApiAuthMixin, APIView):

    class OutputSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField('get_user')
        vehicle = serializers.SerializerMethodField("get_vehicle")

        class Meta:
            model = OilChange
            fields = ('id', 'user', 'vehicle', 'service_date', 'oil_type', 'mileage',
                      'oil_lifetime_distance', 'next_change_mileage', 'next_service_date')

        def get_user(self, oil_change):
            return oil_change.user.email

        def get_vehicle(self, oil_change):
            return oil_change.vehicle.name

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        try:
            oil_change = get_last_oil_change(
                user=request.user, vehicle=request.vehicle)
        except Exception as ex:
            return Response(
                {"error": f"Database Error: {str(ex)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputSerializer(oil_change).data,
                        status=status.HTTP_200_OK)
