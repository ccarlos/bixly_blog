from django.contrib import admin
from bixly_blog.blog.models import BlogEntry, Tag


class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('creator', 'title', 'created')
    list_filter = ('created',)
    ordering = ('-created',)
    filter_horizontal = ('tags',)


admin.site.register(BlogEntry, BlogEntryAdmin)
admin.site.register(Tag)
