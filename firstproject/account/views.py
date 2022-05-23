from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.db.models.aggregates import Sum
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils import timezone

from forum.models import Message
from account.models import User, Session

from account.forms import LoginForm, RegisterForm

def login(request):
    errors = ''
    if request.method == 'POST':
        user = request.POST.get('login')
        password = request.POST.get('password')
        url = request.POST.get('continue', '/')
        session = Session.custom.do_login(user, password)
        if session:
            response = HttpResponseRedirect(url)
            response.set_cookie(
                'sessid', session.key,
                domain=None, httponly=True,
                expires=session.expires
            )
            return response
        else:
            error = u'Неверный логин / пароль'
    form = LoginForm()

    return render(request, 'account/login.html', {'errors': errors, 'form': form })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User(**form.cleaned_data)
            user.save()
            Session.custom.do_login(login = user.username, password=user.password)
            url = request.POST.get('continue', reverse_lazy('forum:index'))
            return HttpResponseRedirect(url)
    else:
        form = RegisterForm()
    return render(request, 'account/user_add.html', {'form':form})


def logout(request):
    session = request.COOKIES.get('sessid')
    url = request.GET.get('continue', '/')
    if session is not None:
        try:
            Session.objects.get(key=session).delete()
        except Session.DoesNotExist:
            pass
    return HttpResponseRedirect(url)

class UserView(DetailView):
    context_object_name = 'user'
    template_name = "account/user_detail.html"
    queryset = User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_rating = Message.objects.filter(author__pk=self.kwargs['pk']).aggregate(rating=Sum('messagerating__mark'))
        context['user_rating'] = user_rating
        return context

# class UserCreateView(CreateView):
#     model = User
#     template_name = "account/user_add.html"
#     fields = ['username', 'first_name', 'last_name', 'password', 'email_address']

class UserUpdateView(UpdateView):
    model = User
    template_name = "account/user_update.html"
    context_object_name = "user"
    fields = ['username', 'first_name', 'last_name', 'password', 'email_address']

class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('forum:index')
