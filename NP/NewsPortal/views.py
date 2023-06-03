from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datetime import datetime
from django.core.mail import send_mail

from .models import Post
from .filters import PostFilter
from .forms import PostForm
from .tasks import send_posts_week


class NewsListView(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts/news.html'
    context_object_name = "news"
    paginate_by = 12

    def get_queryset(self):
        news = super().get_queryset()
        news = news.filter(choice='news')
        return news


class NewsDetailView(DetailView):
    model = Post
    template_name = 'posts/news_id.html'
    context_object_name = 'news_id'


class SearchView(ListView):
    model = Post
    ordering = 'time_in'
    template_name = 'posts/search.html'
    context_object_name = 'result'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post',)
    template_name = 'posts/update.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        print(**kwargs)
        return Post.objects.get(pk=id)

    def form_valid(self, form_class):
        form_class.instance.time_in = datetime.now()
        return super().form_valid(form_class)


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post',)
    template_name = 'posts/update.html'
    form_class = PostForm


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsPortal.delete_post',)
    template_name = 'posts/delete.html'
    queryset = Post.objects.all()
    success_url = '/news'


def subscribe_to_category(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    for category in post.categories.all():
        category.subscribers.add(user)
    return redirect(request.META.get('HTTP_REFERER'))
