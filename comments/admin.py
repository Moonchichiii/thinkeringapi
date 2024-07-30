from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'get_post_title', 'created_at')

    def get_post_title(self, obj):
        return obj.post.title
    get_post_title.short_description = 'Post Title'

admin.site.register(Comment, CommentAdmin)
