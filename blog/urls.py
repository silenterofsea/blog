from django.urls import path
from . import views
from blog.feeds import AllPostsRssFeed


app_name = 'blog'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    # path('posts/<int:pk>/', views.detail, name='detail'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    # path('categories/<int:pk>/', views.category, name='category'),
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    # path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('archives/<int:year>/<int:month>/', views.ArchivesView.as_view(), name='archive'),
    # path('tags/<int:pk>/', views.tag, name='tag'),
    path('tags/<int:pk>/', views.TagView.as_view(), name='tag'),
    # url(r'^all/rss/$', AllPostsRssFeed(), name='rss'),
    path('all/rss/', AllPostsRssFeed(), name='rss'),
    # url(r'^search/$', views.search, name='search'),
    path('search/', views.search, name='search'),
]
