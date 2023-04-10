from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import Http404, HttpResponse, response
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages
from django.views import View
from django.shortcuts import render, reverse, redirect
from django.core.mail import EmailMultiAlternatives
from datetime import date
from django.template.loader import render_to_string

from .models import Post, Category, PostCategory
from .filters import NewsFilter
from .forms import PostForm



class NewsList(ListView):
    model = Post
    template_name = 'post/news.html'
    context_object_name = 'post_news'
    paginate_by = 2

    def get_queryset(self):
        news = super().get_queryset()
        news = news.filter(selection_field='news')
        return news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        context['count'] = self.get_queryset().filter(selection_field='news').count()
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'post/news_id.html'
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
        return context


class SearchList(ListView):
    model = Post
    template_name = 'post/news_search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        author_query = self.request.GET.get('author')
        header_query = self.request.GET.get('header_field')
        time_query = self.request.GET.get('time_in')

        object_list = self.model.objects.filter(selection_field='news')
        if query:
            object_list = object_list.filter(Q(title__icontains=query))
        if author_query:
            object_list = object_list.filter(Q(author__user__username__icontains=author_query))
        if header_query:
            object_list = object_list.filter(Q(header_field__icontains=header_query))
        if time_query:
            object_list = object_list.filter(Q(time_in__gt=time_query))
        return object_list.order_by('-time_in')


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'post/add.html'
    form_class = PostForm
    permission_required = ('NewsPortal.add_post',)
    success_url = reverse_lazy('created')

    # def form_valid(self, form):
    #     post = form.save()
    #
    #     categories = PostCategory.objects.filter(post=post)
    #     subscribers = []
    #     for category in categories:
    #         subscribers += list(category.category.subscribers.all())
    #
    #     for subscriber in subscribers:
    #         send_mail(
    #             subject='New Post Notification',
    #             message=f'A new post has been created in {category.category.category_name} category.',
    #             from_email='khegaivyacheslavA@yandex.ru',
    #             recipient_list=[subscriber.email],
    #             fail_silently=False,
    #         )
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('created', kwargs={'pk': self.object.id})


class PostSuccessfullyView(DetailView):
    template_name = 'post/created.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        email = user.email
        header_field = self.object.header_field
        # print(f'user: {user}')
        # print(f'email: {email}')
        # print(f'header_field: {header_field}')

        html = render_to_string('post/created.html',
                                {'header_field': header_field,
                                 'user': user
                                 }
                                )
        print(html)
        msg = EmailMultiAlternatives(
            subject=f'{header_field} subscription',
            body='',
            from_email='khegaivyacheslavA@yandex.ru',
            to=[email]
        )
        msg.attach_alternative(html, "text/html")
        try:
            msg.send()
        except Exception as e:
            print(e)
        return context

    # def distribution_news(self):
    #     user = self.request.user
    #     email = user.email
    #     header_field = self.object.header_field
    #     print(f'user: {user}')
    #     print(f'email: {email}')
    #     print(f'header_field: {header_field}')
    #
    #     html = render_to_string('post/created.html',
    #                             {'header_field': header_field,
    #                              'user': user
    #                              }
    #                             )
    #     msg = EmailMultiAlternatives(
    #         subject=f'{header_field} subscription',
    #         body='',
    #         from_email='khegaivyacheslavA@yandex.com',
    #         to=[email]
    #     )
    #     msg.attach_alternative(html, "text/html")
    #     try:
    #         msg.send()
    #     except Exception as e:
    #         print(e)
    #     return redirect('created')




    # html = render_to_string('post/created.html',
    #                         'selection_field': selection_field)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post/edit.html'
    form_class = PostForm
    permission_required = ('NewsPortal.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'post/delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
