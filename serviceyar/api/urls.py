from django.urls import path, include

urlpatterns = [
    path('users/', include(('serviceyar.users.urls', 'users'))),
    path('auth/', include(('serviceyar.authentication.urls', 'auth'))),
]
