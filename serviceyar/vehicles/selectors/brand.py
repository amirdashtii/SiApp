from django.db.models import QuerySet
from ..models import Brand


def get_brand() -> QuerySet[Brand]:
    return Brand.objects.all()
