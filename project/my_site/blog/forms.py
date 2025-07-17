from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
        labels = {
            "user_name":"Your name",
            "user_email":"Your email",
            "text":"Your comment"
        }

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["date","slug","author"]
        labels = {
            "title":"Title",
            "excerpt":"Post description",
            "image":"Upload image",
            "content":"Text",
            "tags":"Tags"
        }

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"})
    )