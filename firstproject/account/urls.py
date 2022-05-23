from django.urls import path
from .views import *
from django.conf.urls.static import static
from firstproject import settings

app_name = "account"

urlpatterns = [
    path('<int:pk>/', UserView.as_view(), name='user'),
    path('<int:pk>/update', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)