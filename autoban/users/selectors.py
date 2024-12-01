from .models import BaseUser, Profile

def get_profile(user: BaseUser) -> Profile:
    return Profile.objects.get(user=user)