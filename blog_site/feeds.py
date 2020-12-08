# myproject/feeds.py

from django.contrib.syndication.views import Feed
from django.urls import reverse

from blog.models import Post


class LatestPostsFeed(Feed):
    title = "しろねこブログ 最新記事"
    link = "/blog/"
    description = "しろねこ のブログ記事に関する最新情報。"

    def items(self):
        return Post.objects.order_by('-published_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    # モデルに get_absolute_url() が定義されている場合は不要
    def item_link(self, item):
        return reverse('blog:post_detail', args=[item.pk])
