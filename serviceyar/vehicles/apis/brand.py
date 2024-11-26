from drf_spectacular.utils import extend_schema
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from serviceyar.vehicles.models import Brand
from serviceyar.vehicles.selectors.brand import get_brand


class BrandApi(APIView):

    class OutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = Brand
            fields = ('id', 'name')

    @extend_schema(responses=OutputSerializer)
    def get(self, request, vehicle_type_id):

        try:
            query = get_brand(vehicle_type_id=vehicle_type_id)
        except Exception as ex:
            return Response(
                f"Database Error: {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputSerializer(query, many=True).data,
                        status=status.HTTP_200_OK)
