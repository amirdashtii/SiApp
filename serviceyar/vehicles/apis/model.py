from drf_spectacular.utils import extend_schema
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from serviceyar.vehicles.models import Model
from serviceyar.vehicles.selectors.model import get_model


class ModelApi(APIView):

    class OutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = Model
            fields = ('id', 'name')

    @extend_schema(responses=OutputSerializer)
    def get(self, request, vehicle_type_id, brand_id):
        try:
            query = get_model(vehicle_type_id, brand_id)
        except Exception as ex:
            return Response(
                f"Database Error: {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputSerializer(query, many=True).data,
                        status=status.HTTP_200_OK)
