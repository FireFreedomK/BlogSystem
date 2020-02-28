"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url
from blog.views import (
    post_list,post_detail,PostDetailView,
    IndexView,CategoryView,TagView,SearchView,
    AuthorView,
)
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from django.contrib.sitemaps import views as sitemap_views
from config.views import LinkListView
from comment.views import CommentView
from blog.apis import PostViewSet
from django.urls import include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'post',PostViewSet,basename='api-post')

urlpatterns = [
    url(r'^$',IndexView.as_view(),name='index'),
    url(r'^category/(?P<category_id>\d+)/$',CategoryView.as_view(),name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$',TagView.as_view(),name='tag-list'),
    url(r'^post/(?P<post_id>\d+).html$',PostDetailView.as_view(),name='post-detail'),
    url(r'^comment/$',CommentView.as_view(),name='comment'),       #评论功能
    url(r'^links/$',LinkListView.as_view(),name='links'),       #友链功能
    url(r'^search/$',SearchView.as_view(),name='search'),       #搜索功能
    url(r'^author/(?P<owner_id>\d+)/$',AuthorView.as_view(),name='author'),     #作者页面
    #url(r'^super_admin/', admin.site.urls,name='super-admin'),     #用于管理用户
    url(r'^admin/',xadmin.site.urls,name='xadmin'),        #用于管理业务
    url(r'^rss|feed/',LatestPostFeed(),name='rss'),     #用于RSS订阅
    url(r'^sitemap\.xml$',sitemap_views.sitemap,{'sitemaps':{'posts':PostSitemap}}),     #用于实现sitemap，输出文章列表
    #url(r'^api/post/',PostList.as_view(),name='post-list'),    #使用两种方式编写的api，效果相同
    #url(r'^api/post',post_list,name='post-list'),
    url(r'^api/docs/', include_docs_urls(title='typeidea apis')),   #django-rest-framework提供的docs工具
    url(r'^api/post',include(router.urls)),
]
