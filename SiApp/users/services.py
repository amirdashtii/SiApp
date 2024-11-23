from django.db import transaction
from .models import BaseUser, Profile


def create_profile(*, user: BaseUser, first_name: str | None, last_name: str | None, birth_date: str | None, phone_number: str | None) -> Profile:
    return Profile.objects.create(user=user, first_name=first_name, last_name=last_name, birth_date=birth_date, phone_number=phone_number)


def create_user(*, email: str, password: str) -> BaseUser:
    return BaseUser.objects.create_user(email=email, password=password)


@transaction.atomic
def register(*, email: str, password: str,  first_name: str | None, last_name: str | None, birth_date: str | None, phone_number: str | None) -> BaseUser:

    user = create_user(email=email, password=password)
    create_profile(user=user, first_name=first_name, last_name=last_name, birth_date=birth_date, phone_number=phone_number)

    return user
