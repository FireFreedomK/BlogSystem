from django.urls import reverse
from django.utils.html import format_html
from .models import Post,Category,Tag
from .adminforms import PostAdminForm
from typeidea.adminx import BaseOwnerAdmin
from xadmin.layout import Row,Fieldset,Container
from xadmin.filters import manager,RelatedFieldListFilter
import xadmin

# Register your models here.

"""
在同一页面下编辑关联数据
在分类页面下编辑文章
"""
class PostInline:  # StackedInline  样式不同
    form_layout=(
        Container("title","desc")
    )
    extra = 1
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    #inlines = [PostInline,]

    list_display = ('name','status','is_nav','created_time','post_count')
    fields = ('name','status','is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'



@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')



class CategoryOwnerFilter(RelatedFieldListFilter):
    """自定义过滤器只展示当前用户分类"""

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name=='category'

    def __init__(self, field, request, params, model, admin_view, field_path):
        super().__init__(field, request, params, model, admin_view, field_path)
        #重新获取lookup_choices,根据owner过滤
        self.lookup_choices=Category.objects.filter(owner=request.user).values_list('id','name')

manager.register(CategoryOwnerFilter,take_priority=True)



@xadmin.sites.register(Post)
class Postadmin(BaseOwnerAdmin):
    form=PostAdminForm

    list_display = [
        'title', 'category', 'status',
        'created_time','owner','operator',
    ]
    list_display_links = []

    list_filter = ['category',]      #注意这里不是定义的filter类，而是字段名
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面，用于控制是否在页面顶部展示“保存”、“保存并继续”、“保存并新增另一个”三个按钮
    save_on_top = True

    #指定哪些字段不展示
    exclude = ['owner']

    #限定要展示的字段
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    form_layout = (
        Fieldset(
            '基础信息',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'content',
        )
    )

    #用于控制多对多字段的展示效果，横向展示、纵向展示
    # filter_horizontal = ('tag', )
    #filter_vertical = ('tag',)

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))   #使用reverse方式获取后台地址
        )

    operator.short_description = '操作'

    """自定义静态资源引入"""
    # def get_media(self):
    # # xadmin基于bootstrap，引入会页面样式冲突，仅供参考, 故注释。
    # media = super().get_media()
    # media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
    # media.add_css({
    # 'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
    # })
    # return media


# """
# 在admin页面上查看操作日志
# """
# @xadmin.sites.register(LogEntry)
# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ['object_repr','object_id','action_flag','user','change_message']




