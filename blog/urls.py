from django.urls import path
from blog import views

urlpatterns = [
    path('', views.AboutView.as_view(), name='about'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('unublished/', views.PostListViewAll.as_view(), name='unpublished'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/',views.CreatePostView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/remove/', views.post_remove, name='remove'),
    path('post/<int:pk>/remove_unpublished/', views.post_remove_unpublished, name='remove_unpublished'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='approve'),
    path('comment/<int:pk>/disapprove/', views.comment_disapprove, name='disapprove'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='delete'),
    path('post/<int:pk>/publish/', views.post_publish, name='publish'),
    path('post/<int:pk>/unpublish/', views.post_unpublish, name='unpublish'),
    path('post/<int:post_pk>/<int:comment_pk>/score_up/', views.score_up, name='score_up'),
    path('post/<int:post_pk>/<int:comment_pk>/score_down/', views.score_down, name='score_down')


]