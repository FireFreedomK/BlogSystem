from django import forms

"""
在有更多的定制需求的情况下使用ModelForm
"""

class PostAdminForm(forms.ModelForm):
    desc=forms.CharField(widget=forms.Textarea,label='摘要',required=False)