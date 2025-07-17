from django.contrib import admin
from .models import Author,Tag, Post, Comment

class PostAdmin(admin.ModelAdmin):
    """A model admin for the Post model.

    :param admin: Django admin module
    :type admin: module
    """

    list_filter = ("author","tags","date")
    list_display = ("title","date","author")
    prepopulated_fields = {"slug":("title",)}

class CommentAdmin(admin.ModelAdmin):
    """A model admin for the Comment model.

    :param admin: Django admin module
    :type admin: module
    """
    
    list_display = ("user_name","post")

admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
