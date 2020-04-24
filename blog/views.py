from django.core.mail import send_mail
from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post, Comment, Welcome
from blog.forms import PostForm,CommentForm, WelcomeForm, EmailPostForm
from django.urls import reverse_lazy, reverse
from django.views.generic import (View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from .forms import EmailPostForm, CommentForm, SearchForm


class AboutView(View):
    welcome = Welcome.objects.filter(pk=1)
    template_name = 'about.html'


class PostListView(ListView):
    model = Post
    paginate_by = 9

    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-published_date')

class PostListViewAll(ListView, LoginRequiredMixin):
    model = Post
    paginate_by = 9
    template_name = "post_list_all.html"

    def get_queryset(self):
        return Post.objects.filter(status='draft').order_by('-create_date')

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
        return Post.objects.filter(status='draft').order_by('-created_date')

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
    return redirect('unpublished')

@login_required
def post_unpublish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.unpublish()
    return redirect('post_list')

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
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

def post_share(request, pk):
    post = get_object_or_404(Post, pk=pk)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                                            post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com',[cd['to']])
            sent = True
    else:
         form = EmailPostForm()

    return render(request, 'blog/post_share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent
                                                    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                       .order_by('-same_tags', '-published_date')[:4]
    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'similar_posts': similar_posts})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.05).order_by('-similarity')
    return render(request,
                  'blog/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})