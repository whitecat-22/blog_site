# from django.shortcuts import render
import logging

# Create your views here.
# blog/views.py

from django.db.models import Count, Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from blog.models import Post, Category, Tag, Comment   # Reply
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView
from blog.forms import CommentForm, BlogCreateForm  #ReplyForm

from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ContactForm


logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'


class BlogListView(ListView):
    model = Post
    template_name = 'blog.html'
    paginate_by = 3

    def get_queryset(self):
        blogs = Post.objects.order_by('-created_at')
        return blogs


class CategoryPostView(ListView):
    model = Post
    template_name = 'category_post.html'
    paginate_by = 3

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagPostView(ListView):
    model = Post
    template_name = 'tag_post.html'
    paginate_by = 3

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        qs = super().get_queryset().filter(tags=self.tag)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class PostDetailView(DetailView):
    model = Post
    slug_field = 'title'
    slug_url_kwarg = 'title'
    template_name = 'blog_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj


class SearchPostView(ListView):
    model = Post
    template_name = 'search_post.html'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct()
            return qs
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context


class CategoryListView(ListView):
    queryset = Category.objects.annotate(
        num_posts=Count('post', filter=Q(post__is_public=True)))


class TagListView(ListView):
    queryset = Tag.objects.annotate(num_posts=Count(
        'post', filter=Q(post__is_public=True)))


class CommentFormView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        post_pk = self.kwargs['pk']
        comment.post = get_object_or_404(Post, pk=post_pk)
        comment.save()
        return redirect('blog:post_detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        context['post'] = get_object_or_404(Post, pk=post_pk)
        return context


#@login_required
#def comment_approve(request, pk):
#    comment = get_object_or_404(Comment, pk=pk)
#    comment.approve()
#    return redirect('blog:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post_detail', pk=comment.post.pk)


#class ReplyFormView(CreateView):
#    model = Reply
#    form_class = ReplyForm
#
#    def form_valid(self, form):
#        reply = form.save(commit=False)
#        comment_pk = self.kwargs['pk']
#        reply.comment = get_object_or_404(Comment, pk=comment_pk)
#        reply.save()
#        return redirect('blog:post_detail', pk=reply.comment.post.pk)
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        comment_pk = self.kwargs['pk']
#        context['comment'] = get_object_or_404(Comment, pk=comment_pk)
#        return context
#
#
#@login_required
#def reply_approve(request, pk):
#    reply = get_object_or_404(Reply, pk=pk)
#    reply.approve()
#    return redirect('blog:post_detail', pk=reply.comment.post.pk)
#
#
#@login_required
#def reply_remove(request, pk):
#    reply = get_object_or_404(Reply, pk=pk)
#    reply.delete()
#    return redirect('blog:post_detail', pk=reply.comment.post.pk)



class ContactFormView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
#    success_url = '/contact_result/'
    success_url = reverse_lazy('blog:contact')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


#class ContactResultView(TemplateView):
#    template_name = 'contact_result.html'
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['success'] = "お問い合わせは正常に送信されました。"
#        return context


class BlogCreateFormView(FormView):
    template_name = 'blog_create.html'
    form_class = BlogCreateForm

#    success_url = '/blog_create/'
    success_url = reverse_lazy('blog:blog_create')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'ブログを投稿しました。')
        logger.info('Blog sent by {}'.format(form.cleaned_data['title', 'category', 'tag', 'content', 'description', 'created_at', 'updated_at', 'published_at', 'is_public']))
        return super().form_valid(form)


class AboutView(TemplateView):
    template_name = 'about.html'


class ServiceView(TemplateView):
    template_name = 'service.html'


class PortfolioView(TemplateView):
    template_name = 'portfolio.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'


class DisclaimerView(TemplateView):
    template_name = 'disclaimer.html'


class FAQView(TemplateView):
    template_name = 'FAQ.html'
