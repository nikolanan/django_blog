from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.urls import reverse
from datetime import date
from .models import Post, Comment, Author
from django.views.generic import ListView
from django.views.generic import View
from .forms import CommentForm, CustomLoginForm,CreatePostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

class StartingPageView(View):
    """
    Class view that returns the starting
    page.
    :param View: The base class for all class-based views
    :type View: View
    """

    def get(self,request:HttpRequest) -> HttpResponse:
        """Is the method that handles the GET request
        for the starting page.

        :param request: The request object that contains metadata about the request.
        :type request: HttpRequest
        :return: A rendered HTML page with the latest posts.
        :rtype: HttpResponse
        """
        latest_posts = Post.objects.all().order_by("-date")[:3]
        return render(request, "blog/index.html",{
            "posts":latest_posts
        })

class AllPostsView(View):
    """ 
    Class view that returns all posts
    in the database.

    :param View: The base class for all class-based views
    :type View: View
    """

    def get(self,request:HttpRequest) -> HttpResponse:
        """ Handles the GET request for all posts.

        :param request: The request object that contains metadata about the request.
        :type request: HttpRequest
        :return: A rendered HTML page with all posts.
        :rtype: HttpResponse
        """
        all_posts = Post.objects.all()
        return render(request, "blog/all-posts.html",{
            "all_posts":all_posts
        })

class SinglePostView(View):
    """ 
    Class view that returns a single post

    :param View: The base class for all class-based views
    :type View: View
    """

    def is_stored_post(self,request:HttpRequest,post_id:int) -> bool:
        """ 
        Checks if a post is stored for later reading.

        :param request: The request object that contains metadata about the request.
        :type request: HttpRequest
        :param post_id: The ID of the post to check.
        :type post_id: int
        :return: _description_
        :rtype: _type_
        """
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self,request:HttpRequest, slug:str) -> HttpResponse:
        """ 
        Handles the GET request for a single post.

        :param request: The request object that contains metadata about the request.
        :type request: HttpRequest
        :param slug: The slug of the post to retrieve.
        :type slug: str
        :return: A rendered HTML page with the post details.
        :rtype: HttpResponse
        """
        identified_post = Post.objects.filter(slug=slug)[0]
        comment_form = CommentForm()
        return render(request, "blog/post-detail.html",{
            "post":identified_post,
            "post_tags":identified_post.tags.all(),
            "comment_form":comment_form,
            "comments": identified_post.comments.all().order_by("-id"),
            "is_saved_for_later": self.is_stored_post(request,identified_post.id)
        })
    
    def post(self,request:HttpRequest,slug:str) -> HttpResponseRedirect:
        """ 
        Handles the POST request for adding a comment to a post.

        :param request: The request object that contains metadata about the request.
        :type request: HttpRequest
        :param slug: The slug of the post to which the comment is being added.
        :type slug: str
        :return: A redirect to the post detail page after saving the comment.
        :rtype: HttpResponseRedirect
        """
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
    """ 
    Class view that handles the "read later" functionality.

    :param View: The base class for all class-based views
    :type View: View
    """

    def get(self, request:HttpRequest) -> HttpResponse:
        """ 
        Handles the GET request for displaying stored posts.

        :param request: The request object that contains metadata about the request.
        :type request: HttpRequest
        :return: A rendered HTML page with stored posts.
        :rtype: HttpResponse
        """
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

    def post(self,request:HttpRequest) -> HttpResponseRedirect:
        """ 
        Handles the POST request for adding or removing a post from the "read later" list.

        :param request: The request object that contains metadata about the request.
        :type request: HttpRequest
        :return: A redirect to the home page after updating the stored posts.
        :rtype: HttpResponseRedirect
        """
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
    """ 
    Class view that allows users to add a new post.

    :param LoginRequiredMixin: Ensures that the user is logged in to access this view.
    :type LoginRequiredMixin: LoginRequiredMixin
    :param View: The base class for all class-based views
    :type View: View
    """

    login_url = '/registration/login/' # URL to redirect to if the user is not logged in

    def get(self,request:HttpRequest) -> HttpResponse:
        """
        Handles the GET request for displaying the post creation form.

        :param request: The request object that contains metadata about the request.
        :type request: HttpRequest
        :return: A rendered HTML page with the post creation form.
        :rtype: HttpResponse
        """
        create_post_form = CreatePostForm()
        context = {"create_form":create_post_form}
        return render(request,"blog/add-post.html",context)
    
    def post(self,request:HttpRequest) -> HttpResponseRedirect:
        """ 
        Handles the POST request for creating a new post.

        :param request: The request object that contains metadata about the request.
        :type request: HttpRequest
        :return: A redirect to the post detail page after saving the new post.
        :rtype: HttpResponseRedirect
        """

        create_post_form = CreatePostForm(request.POST, request.FILES)  
        if create_post_form.is_valid():
            post = create_post_form.save(commit=False)
            author = Author.objects.get(user=request.user)
            post.author = author
            post.save()
            return redirect("post-detail-page", slug=post.slug) 
        else:
            context = {"create_form": create_post_form}
            return render(request, "blog/add-post.html", context)

class LoginView(View):
    """
    Class view that handles user login.

    :param View: The base class for all class-based views
    :type View: View
    """

    def get(self, request:HttpRequest) -> HttpResponse:
        """
        Handles the GET request for displaying the login form.

        :param request: The request object that contains metadata about the request.
        :type request: HttpRequest
        :return: A rendered HTML page with the login form.
        :rtype: HttpResponse
        """

        login_form = CustomLoginForm()
        context = {"login_form":login_form}
        return render(request, "registration/login.html",context)

    def post(self, request:HttpRequest) -> HttpResponseRedirect:
        """
        Handles the POST request for user authentication.

        :param request: The request object that contains metadata about the request.
        :type request: HttpRequest
        :return: A redirect to the home page if authentication is successful, 
        or a rendered login page with an error message if authentication fails.
        :rtype: HttpResponseRedirect
        """

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
    """ Class view that handles user registration. Not implemented yet.

    :param View: The base class for all class-based views
    :type View: View
    """

    def get(self,request):
        """
        Not implemented yet. This method is intended to handle the GET request for user registration.
        """
        return render(request,reverse("register"))


class LogoutView(View):
    """ 
    Class view that handles user logout.

    :param View: The base class for all class-based views
    :type View: View
    """

    def post(self, request:HttpRequest) -> HttpResponseRedirect:
        """
        Handles the POST request for user logout.

        :param request: The request object that contains metadata about the request.
        :type request: HttpRequest
        :return: A redirect to the login page after logging out.
        :rtype: HttpResponseRedirect
        """

        logout(request)
        return redirect('login')