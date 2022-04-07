from django import template
from django.db.models.aggregates import Sum

from forum.models import Forum, MessageRating, Message

register = template.Library()

@register.simple_tag(name='menu')
def get_menu():
    menu = [
        {'title': 'Topics', 'url_name': 'forum:index'},
        {'title': 'Create Topic', 'url_name': 'forum:new_topic'}
    ]
    return menu

@register.inclusion_tag('forum/templatetags/list_top_topics.html')
def get_top_five():
    top_five_query = Forum.objects.filter(message__is_head=True).annotate(rating=Sum('message__messagerating__mark')).order_by('-rating')[:5]
    return {'top_five_topics': top_five_query}