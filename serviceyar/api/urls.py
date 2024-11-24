from django.urls import path, include

urlpatterns = [
    path('auth/', include(('serviceyar.authentication.urls', 'auth'))),
    path('users/', include(('serviceyar.users.urls', 'users'))),
    path('vehicles/', include(('serviceyar.vehicles.urls', 'vehicles'))),
]
