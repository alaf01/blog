from django import forms
from blog.models import Post, Comment, Welcome

class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text', 'photo')

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')

    widgets = {
        'author':forms.TextInput(attrs={'class':'textinputclass'}),
        'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
        }

class WelcomeForm(forms.ModelForm):

    class Meta():
        model = Welcome
        fields = ('__all__')