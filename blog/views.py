
from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post, Comment, Welcome
from blog.forms import PostForm,CommentForm, WelcomeForm
from django.urls import reverse_lazy, reverse
from django.views.generic import (View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class AboutView(View):
    welcome = Welcome.objects.filter(pk=1)
    template_name = 'about.html'


class PostListView(ListView):
    model = Post
    paginate_by = 9

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostListViewAll(ListView, LoginRequiredMixin):
    model = Post
    paginate_by = 9
    template_name = "post_list_all.html"

    def get_queryset(self):
        return Post.objects.filter(published_date=None).order_by('-create_date')

class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    #where to go if not logged in
    login_url='/login/'
    #where to go after login
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
    template_name = "blog/add_photo.html"

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    #where to go after login
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    reditect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')

class WelcomeView(UpdateView):
    model = Welcome
    form_class = WelcomeForm
    template_name = "blog/welcome_form.html"

    def get_success_url(self):
        return reverse('about')


#####################################################
#####################################################
@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_list')

def post_unpublish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.unpublish()
    return redirect('unpublished')

def post_remove(request, pk):
    post = get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('post_list')

def post_remove_unpublished(request, pk):
    post = get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('unpublished')

def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            success = True
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return render (request, 'blog/post_detail.html', {'post':post, 'success' :success})
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_disapprove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.disapprove()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

def score_up(request, post_pk, comment_pk):
    post=get_object_or_404(Post, pk=post_pk)
    comment=get_object_or_404(Comment, pk=comment_pk)
    comment.get_score_up()
    return render(request, 'blog/post_detail.html',
                  {'post': post, 'comment': comment})

def score_down(request, post_pk, comment_pk):
    post=get_object_or_404(Post, pk=post_pk)
    comment=get_object_or_404(Comment, pk=comment_pk)
    comment.get_score_down()
    return render(request, 'blog/post_detail.html',
                  {'post': post, 'comment': comment})

def welcome(request):
    welcome = get_object_or_404(Welcome,pk=1)
    return render(request, 'blog/about.html', {'welcome': welcome})