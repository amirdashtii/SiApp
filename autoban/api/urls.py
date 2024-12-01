from django.urls import path, include

urlpatterns = [
    path('auth/', include(('autoban.authentication.urls', 'auth'))),
    path('users/', include(('autoban.users.urls', 'users'))),
    path('vehicles/', include(('autoban.vehicles.urls', 'vehicles'))),
    path('care/', include(('autoban.care.urls', 'care'))),
]
