from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.db.models.aggregates import Sum
from django.urls import reverse

from forum.models import Forum, Message, Category
from account.models import User
from .forms import MessageForm, DeleteMessageForm, CreateTopicForm
from forum.class_based_view import *


def TopicCreate(request):
    if request.method == 'POST':
        form = CreateTopicForm(request.POST)
        if form.is_valid():
            topic_title = form.cleaned_data['title']
            message_text = form.cleaned_data['text']
            topic_author_name = form.cleaned_data['author']
            topic_author = get_object_or_404(User, username=topic_author_name)
            new_topic = Forum.objects.create(
                title=topic_title, author=topic_author)
            Message.objects.create(
                text=message_text, forum=new_topic, author=topic_author, is_head=True)
            return HttpResponseRedirect(reverse('forum:topic', kwargs={'pk': new_topic.pk}))
    else:
        form = CreateTopicForm()

    return render(request, 'forum/addtopic.html', {'form': form})


def Topic_View(request, pk):
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            forum = get_object_or_404(Forum, pk=pk)
            message_text = form.cleaned_data['text']
            author_name = form.cleaned_data['author']
            message_author = get_object_or_404(User, username=author_name)
            Message.objects.create(author=message_author, text=message_text, forum=forum)
            return HttpResponseRedirect(reverse('forum:topic', kwargs={'pk': pk}))
    else:
        form = MessageForm()
        msgs = Forum.custom.get_messages_with_rating(pk)
    return render(request, 'forum/topic.html', {'form': form, 'messages': msgs, 'pk':pk})


def DeleteMessage(request, pk):
    form = DeleteMessageForm(request.POST)
    if form.is_valid():
        msg_pk = form.cleaned_data['message_pk']
        Message.objects.get(pk=msg_pk).delete()
        return HttpResponseRedirect(reverse('forum:topic', kwargs={'pk': pk}))
    return HttpResponseRedirect(reverse('forum:topic', kwargs={'pk': pk}))

def test(request):

    return HttpResponse('hi')