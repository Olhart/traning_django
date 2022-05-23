from django.urls import path
from django.views.generic import TemplateView
from .views import *
from django.conf.urls.static import static
from firstproject import settings

app_name = "forum"

urlpatterns = [
    path('', IndexForum.as_view(), name='index'),
    path('topic/<int:pk>/', Topic_View, name='topic'),
    path('topic/create/', TopicCreate, name='new_topic'),
    path('topic/<int:pk>/deletemsg/', DeleteMessage, name='delete_message'),

    # path('topic/<int:pk>/', TopicView.as_view(), name='topic'),
    path('test/', test)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)