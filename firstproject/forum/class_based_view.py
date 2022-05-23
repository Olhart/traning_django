from django.views.generic import ListView, DetailView
from django.db.models.aggregates import Sum, Min

from forum.models import Forum, Message

class IndexForum(ListView):
    model = Forum
    paginate_by = 10
    # queryset = Forum.objects.all().select_related('author')

    def get_queryset(self):
        queryset = Forum.objects.filter(is_published=True).values('pk', 'title', 'author__username').annotate(rating=Sum('message__messagerating__mark'), last_message_date=Min('message__create_date')).order_by('title')
        return queryset

class TopicView(DetailView):
    template_name = "forum/topic.html"
    context_object_name = "topic"
    queryset = Forum.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        msg_rating = Forum.objects.filter(pk=self.kwargs['pk']).values('message').annotate(rating=Sum("message__messagerating__mark"))
        context['rating'] = msg_rating
        return context