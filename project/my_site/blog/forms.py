from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    """A form for creating a comment on a post.

    :param forms: Django forms module
    :type forms: module
    """
    class Meta:
        """
        Meta class for CommentForm.
        """
        model = Comment
        exclude = ["post"]
        labels = {
            "user_name":"Your name",
            "user_email":"Your email",
            "text":"Your comment"
        }

class CreatePostForm(forms.ModelForm):
    """
    A form for creating a new post.

    :param forms: Django forms module
    :type forms: module
    """
    class Meta:
        """
        Meta class for CreatePostForm.
        """
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
    """A custom login form that extends Django's built-in authentication form.

    :param forms: Django forms module
    :type forms: module
    """

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"})
    )