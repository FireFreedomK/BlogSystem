from django import forms
from dal import autocomplete
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Category,Tag,Post
"""
在有更多的定制需求的情况下使用ModelForm
"""

class PostAdminForm(forms.ModelForm):
    desc=forms.CharField(widget=forms.Textarea,label='摘要',required=False)
    content_ck=forms.CharField(widget=CKEditorUploadingWidget(),label='正文',required=False)
    content_md=forms.CharField(widget=forms.Textarea(),label='正文',required=False)
    content=forms.CharField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model = Post
        fields = (
            'category', 'tag', 'desc', 'title',
            'is_md', 'content', 'content_md', 'content_ck',
            'status'
        )

    def __init__(self, instance=None, initial=None, **kwargs):
        initial = initial or {}
        if instance:
            if instance.is_md:
                initial['content_ck'] = instance.content

        super().__init__(instance=instance, initial=initial, **kwargs)

    def clean(self):
        is_md = self.cleaned_data.get('is_md')
        if is_md:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        content = self.cleaned_data.get(content_field_name)
        if not content:
            self.add_error(content_field_name, '必填项！')
            return
        self.cleaned_data['content'] = content
        return super().clean()

    class Media:
        js = ('js/post_editor.js',)


