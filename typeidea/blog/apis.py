from rest_framework import viewsets,generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post, Category
from .serializers import (
    PostSerializer, PostDetailSerializer,
    CategorySerializer, CategoryDetailSerializer
)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """ 提供文章接口 """
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer        #重新设置serializer_class的值，达到不同接口使用不同Serializer的目的
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)


@api_view()     #该装饰器的作用是将一个view转换为api view
def post_list(request):
    posts=Post.objects.filter(status=Post.STATUS_NORMAL)
    post_serializers=PostSerializer(posts,many=True)
    return Response(post_serializers.data)


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer