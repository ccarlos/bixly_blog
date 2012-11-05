from django.contrib import admin
from bixly_blog.blog.models import BlogEntry, Tag, BlogComment, BlogCommentLike


class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('creator', 'title', 'created')
    list_filter = ('created',)
    ordering = ('-created',)
    filter_horizontal = ('tags',)


class CommentAdmin(admin.ModelAdmin):
    fields = ['creator', 'created', 'body', 'blog']
    list_display = ['creator', 'created', 'blog']
    list_filter = ['created', 'blog']


admin.site.register(BlogEntry, BlogEntryAdmin)
admin.site.register(Tag)
admin.site.register(BlogComment, CommentAdmin)
admin.site.register(BlogCommentLike)
