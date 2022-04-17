from django.views.generic import ListView, DetailView
from django.db.models.aggregates import Sum, Min
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Forum, User, Message

class IndexForum(ListView):
    model = Forum
    paginate_by = 10
    # queryset = Forum.objects.all().select_related('author')

    def get_queryset(self):
        queryset = Forum.objects.filter(is_published=True).values('pk', 'title', 'author__username').annotate(rating=Sum('message__messagerating__mark'), last_message_date=Min('message__create_date')).order_by('title')
        return queryset

class UserView(DetailView):
    context_object_name = 'user'
    template_name = "forum/user_detail.html"
    queryset = User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_rating = Message.objects.filter(author__pk=self.kwargs['pk']).aggregate(rating=Sum('messagerating__mark'))
        context['user_rating'] = user_rating
        return context

class TopicView(DetailView):
    template_name = "forum/topic.html"
    context_object_name = "topic"
    queryset = Forum.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        msg_rating = Forum.objects.filter(pk=self.kwargs['pk']).values('message').annotate(rating=Sum("message__messagerating__mark"))
        context['rating'] = msg_rating
        return context

class UserCreateView(CreateView):
    model = User
    template_name = "forum/user_add.html"
    fields = ['username', 'first_name', 'last_name', 'password', 'email_address']

class UserUpdateView(UpdateView):
    model = User
    template_name = "forum/user_update.html"
    context_object_name = "user"
    fields = ['username', 'first_name', 'last_name', 'password', 'email_address']

class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('forum:index')