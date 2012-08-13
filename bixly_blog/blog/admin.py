from django.contrib import admin
from bixly_blog.blog.models import BlogEntry


class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('creator', 'title', 'created')
    list_filter = ('created',)
    ordering = ('-created',)


admin.site.register(BlogEntry, BlogEntryAdmin)
