from django import template

register = template.Library()

@register.inclusion_tag('account/templatetags/account_panel.html')
def get_account_panel(user=None):

    return {'user': user}