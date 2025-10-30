from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "description"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "category",
        "status",
        "published_at",
        "created_at",
    ]
    list_filter = ["status", "category", "created_at", "published_at"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ["-published_at", "-created_at"]
    raw_id_fields = ["author"]

    fieldsets = (
        ("Post Information", {"fields": ("title", "slug", "author", "category")}),
        ("Content", {"fields": ("content", "excerpt", "featured_image")}),
        ("Publication", {"fields": ("status", "published_at")}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "created_at", "approved"]
    list_filter = ["approved", "created_at"]
    search_fields = ["content", "author__username", "post__title"]
    actions = ["approve_comments", "unapprove_comments"]
    raw_id_fields = ["post", "author"]

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = "Approve selected comments"

    def unapprove_comments(self, request, queryset):
        queryset.update(approved=False)

    unapprove_comments.short_description = "Unapprove selected comments"
