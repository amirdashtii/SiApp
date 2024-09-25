from django.urls import path, include

urlpatterns = [
    path('users/', include(('siapp.users.urls', 'users'))),
    path('auth/', include(('siapp.authentication.urls', 'auth'))),
]
