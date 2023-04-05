from django.views.generic import ListView, DetailView
from .models import Post
from django.http import Http404
from datetime import datetime


class NewsList(ListView):
    model = Post
    ordering = 'time_in'
    template_name = 'news.html'
    context_object_name = 'post_news'

    def get_queryset(self):
        news = super().get_queryset()
        news = news.filter(selection_field='news')
        return news

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['time_now'] = datetime.utcnow()
    #     return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_id.html'
    context_object_name = 'news_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.selection_field == 'news':
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            raise Http404("Страница не найдена")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['some_other_data'] = ...
        return context
