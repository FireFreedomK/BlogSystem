

class BaseOwnerAdmin:
    """
    1. 用来处理文章、分类、标签、侧边栏、友链这些model的owner字段自动补充
    2. 用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner', )

    """
        自定义列表页数据：当前登录的用户在列表页中只能看到自己创建的文章
    """
    def get_list_queryset(self):
        request=self.request
        qs = super().get_list_queryset()
        return qs.filter(owner=request.user)

    """
        通过给obj.owner赋值，达到自动设置owner的目的
        request是当前请求
        request.user是当前已经登陆的用户，未登录拿到的是匿名用户对象
    """
    def save_model(self):
        self.new_obj.owner = self.request.user
        return super().save_models()