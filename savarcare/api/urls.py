from django.urls import path, include

urlpatterns = [
    path('auth/', include(('savarcare.authentication.urls', 'auth'))),
    path('users/', include(('savarcare.users.urls', 'users'))),
    path('vehicles/', include(('savarcare.vehicles.urls', 'vehicles'))),
    path('care/', include(('savarcare.care.urls', 'care'))),
]
