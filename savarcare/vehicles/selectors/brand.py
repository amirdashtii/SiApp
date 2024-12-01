from django.db.models import QuerySet
from ..models import Brand


def get_brand(vehicle_type_id) -> QuerySet[Brand]:
    return Brand.objects.filter(vehicle_type_id=vehicle_type_id)
