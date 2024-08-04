from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Tag

class TagInline(admin.TabularInline):
    model = Post.tags.through
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'approved', 'average_rating', 'likes_count', 'image_preview')
    list_filter = ('approved', 'created_at', 'tags', 'average_rating')
    search_fields = ('title', 'content', 'author__user__username')
    ordering = ('-created_at',)
    readonly_fields = ('likes_count', 'average_rating', 'rating_count', 'created_at', 'updated_at')
    inlines = [TagInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'

    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'content', 'image', 'tags')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('approved', 'average_rating', 'rating_count', 'likes_count', 'created_at', 'updated_at'),
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('author__user', 'tags')
        return queryset

# Register the Tag model, if not already registered
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
