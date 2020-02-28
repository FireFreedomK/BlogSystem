from django.contrib.admin import AdminSite

"""
定制site(站点)
"""

class CustomSite(AdminSite):
    site_header = 'BlogSystem'
    site_title = 'BlogSystem 管理后台'
    index_title = '首页'


custom_site=CustomSite(name='cus_admin')