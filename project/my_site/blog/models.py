from django.db import models
from django.core import validators
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class Author(models.Model):
    bio = models.TextField(null=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,default=None)
    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"

class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.caption}"

class Post(models.Model):
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
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="comments")

