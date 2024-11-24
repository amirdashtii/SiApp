from drf_spectacular.utils import extend_schema
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from serviceyar.vehicles.models import VehicleModel
from serviceyar.vehicles.selectors.vehicle_model import get_vehicle_model


class VehicleModelApi(APIView):

    class OutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = VehicleModel
            fields = ('id', 'name')

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        try:
            query = get_vehicle_model()
        except Exception as ex:
            return Response(
                f"Database Error: {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputSerializer(query, many=True).data,
                        status=status.HTTP_200_OK)
