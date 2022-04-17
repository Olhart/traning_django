from django.contrib import admin
from forum.models import Forum, MessageRating, User, Message

class MessageInline(admin.StackedInline):
    model = Message
    extra = 1

class ForumAdmin(admin.ModelAdmin):
    # fields = ['title', 'author', 'is_published']
    list_display = ('id', 'title', 'author', 'create_date', 'is_published')
    list_display_links = ('title', 'author')
    list_editable = ('is_published',)
    fieldsets = [
        (None, {'fields': ['title', 'is_published']}),
        ('Author', {'fields': ['author'], 'classes': ['collapse']}),
    ]
    inlines = [MessageInline,]

admin.site.register(Forum, ForumAdmin)
admin.site.register(User)
# admin.site.register(Message)