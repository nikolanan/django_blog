from django.db import models
from django.core import validators
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class Author(models.Model):
    """
    A model that extends the the built-in class
    User 1:1 to provide additional fields. Building user as out-of-the-box
    Django solution.
    """
    bio = models.TextField(null=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,default=None)
    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"

class Tag(models.Model):
    """ 
    A simple model that represents
    a tag of a post.
    """
    caption = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.caption}"

class Post(models.Model):
    """
    A model that represents a single post in the database.
    A post may have many tags (M:M) and each post has a
    particular user.
    """
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=200)
    image = models.ImageField(upload_to="posts", null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[validators.MinLengthValidator(10)])
    author = models.ForeignKey(Author,on_delete=models.SET_NULL, related_name="posts",null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    """
    A model represenenting a comment of a post.
    A comment is for a particular post, a post may have many
    comments - post - comment (1:M).
    """
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="comments")
