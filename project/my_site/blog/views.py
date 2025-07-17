from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date
from .models import Post, Comment, Author
from django.views.generic import ListView
from django.views.generic import View
from .forms import CommentForm, CustomLoginForm,CreatePostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

all_posts = [

]

def get_date(post):
    return post["date"]

class StartingPageView(View):
    def get(self,request):
        latest_posts = Post.objects.all().order_by("-date")[:3]
        return render(request, "blog/index.html",{
            "posts":latest_posts
        })

class AllPostsView(View):

    def get(self,request):
        all_posts = Post.objects.all()
        return render(request, "blog/all-posts.html",{
            "all_posts":all_posts
        })

class SinglePostView(View):
    def is_stored_post(self,request,post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self,request, slug):
        identified_post = Post.objects.filter(slug=slug)[0]
        

        comment_form = CommentForm()
        return render(request, "blog/post-detail.html",{
            "post":identified_post,
            "post_tags":identified_post.tags.all(),
            "comment_form":comment_form,
            "comments": identified_post.comments.all().order_by("-id"),
            "is_saved_for_later": self.is_stored_post(request,identified_post.id)
        })
    
    def post(self,request,slug):
        comment_form = CommentForm(request.POST)
        identified_post = Post.objects.filter(slug=slug)[0]
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = identified_post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page",args=[slug]))
        
        return render(request, "blog/post-detail.html",{
            "post":identified_post,
            "post_tags":identified_post.tags.all(),
            "comment_form":comment_form,
            "comments": identified_post.comments.all().order_by("-id")
        })

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)

    def post(self,request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []
        
        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        
        request.session["stored_posts"] = stored_posts
        
        return HttpResponseRedirect("/")

class AddPostView(LoginRequiredMixin,View):
    login_url = '/registration/login/'
    
    def get(self,request):
        create_post_form = CreatePostForm()
        context = {"create_form":create_post_form}
        return render(request,"blog/add-post.html",context)
    def post(self,request):
        create_post_form = CreatePostForm(request.POST, request.FILES)  
        if create_post_form.is_valid():
            post = create_post_form.save(commit=False)
            author = Author.objects.get(user=request.user)
            post.author = author
            post.save()
            return redirect("post-detail", pk=post.pk)  
        else:
            context = {"create_form": create_post_form}
            return render(request, "blog/add-post.html", context)

class LoginView(View):
    def get(self, request):
        login_form = CustomLoginForm()
        context = {"login_form":login_form}
        return render(request, "registration/login.html",context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')  # Change this to your desired success URL
        else:
            login_form = CustomLoginForm()
            return render(request, 'registration/login.html', {
                'error': 'Invalid username or password',
                "login_form":login_form
            })
        
class RegisterView(View):
    def get(self,request):
        return render(request,reverse("register"))


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')