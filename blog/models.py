# blog/models.py

from django.db import models
from django.utils import timezone

from django.contrib.sitemaps import ping_google

from markdownx.models import MarkdownxField


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=255)
    content = MarkdownxField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to='post_images/', null=True, blank=True
        )

    """ カスタムメソッド """
    def get_text_markdownx(self):
        return mark_safe(markdownify(self.text))

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.is_public and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

        try:
            ping_google()
        except Exception:
            pass

    def __str__(self):
        return self.title


class ContentImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    content_image = models.ImageField(upload_to='post_content_images/')


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['-timestamp']

#    def approve(self):
#        self.approved = True
#        self.save()

    def __str__(self):
        self.save()
        return self.text


#class Reply(models.Model):
#    comment = models.ForeignKey(
#        Comment, on_delete=models.CASCADE, related_name='replies')
#    author = models.CharField(max_length=50)
#    text = models.TextField()
#    timestamp = models.DateTimeField(auto_now_add=True)
#    approved = models.BooleanField(default=False)
#
#    def approve(self):
#        self.approved = True
#        self.save()
#
#    def __str__(self):
#        return self.text
