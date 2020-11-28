# Register your models here.
# blog/admin.py

from django.contrib import admin

from blog.models import Category, Tag, Post, ContentImage, Comment, Reply

from django.contrib.sitemaps import ping_google


class ContentImageInline(admin.TabularInline):
    model = ContentImage
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [
        ContentImageInline,
    ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            ping_google()
        except Exception:
            pass


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Reply)
