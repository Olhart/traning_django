from django import forms

class MessageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    author = forms.CharField()

class DeleteMessageForm(forms.Form):
    message_pk = forms.CharField()

class CreateTopicForm(forms.Form):
    title = forms.CharField(label='Topic title')
    text = forms.CharField(widget=forms.Textarea, label='Topic text')
    author = forms.CharField(label='User')

class LoginForm(forms.Form):
    login = forms.CharField(max_length=32, label='Login')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')