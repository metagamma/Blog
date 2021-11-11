from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post

# Just dummy data
''' 
posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]
'''

# Function view
'''
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)
'''

# This is a replacement for the home function view upside
# It's called class view


class PostListView(ListView):
    model = Post
    # This is the naming convention: <app>/<model>_<viewtype>.html
    # However, in this case a custom name is created using the varible template_name
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    # minus sign is used when we want to order from newest to oldest
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


# The following two view classes are linked with post_form.html
# This is the default name that Django looks up when we use CreateView or UpdateView
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user  # current user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user  # current user
        return super().form_valid(form)

    # This function is used to check if the user is the post owner
    def test_func(self):
        post = self.get_object()  # get the post
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # path that the user will be redirected when delete a post
    success_url = "/" 
    # This function is used to check if the user is the post owner
    def test_func(self):
        post = self.get_object()  # get the post
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
