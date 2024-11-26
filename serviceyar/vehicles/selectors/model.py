from django.db.models import QuerySet
from ..models import Model, Brand


def get_model(vehicle_type_id, brand_id) -> QuerySet[Model]:
    brands_ids=Brand.objects.filter(vehicle_type_id=vehicle_type_id).values_list('id', flat=True)
    if brand_id not in brands_ids: 
        return Model.objects.none()
    return Model.objects.filter(brand_id=brand_id)
