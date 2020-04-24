from django import forms
from blog.models import Post, Comment, Welcome

class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text', 'photo', 'tags')

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

class EmailPostForm(forms.Form):
    name = forms. CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)

class SearchForm(forms.Form):
    query = forms.CharField()