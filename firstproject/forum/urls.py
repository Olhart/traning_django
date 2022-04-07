from django.urls import path
from django.views.generic import TemplateView
from .views import *
from django.conf.urls.static import static
from firstproject import settings

app_name = "forum"

urlpatterns = [
    path('', IndexForum.as_view(), name='index'),
    path('user/<int:pk>/', UserView.as_view(), name='user'),
    path('topic/<int:pk>/', Topic_View, name='topic'),
    path('topic/create/', TopicCreate, name='new_topic'),
    path('topic/<int:pk>/deletemsg/', DeleteMessage, name='delete_message'),
    path('user/add/', UserCreateView.as_view(), name='user_add'),
    path('user/<int:pk>/update', UserUpdateView.as_view(), name='user_update'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    # path('topic/<int:pk>/', TopicView.as_view(), name='topic'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)