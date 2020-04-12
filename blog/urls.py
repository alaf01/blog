from django.urls import path
from blog import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/',views.CreatePostView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/remove/', views.PostDeleteView.as_view(), name='post_remove'),
    path('drafts/', views.PostDeleteView.as_view(), name='post_draft_list'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='approve'),
    path('comment/<int:pk>/disapprove/', views.comment_disapprove, name='disapprove'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='delete'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:post_pk>/<int:comment_pk>/score_up/', views.score_up, name='score_up'),
    path('post/<int:post_pk>/<int:comment_pk>/score_down/', views.score_down, name='score_down')


]