from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .models import Article, Subscription, Category
from .filters import NewsFilter
from .forms import ArticleForm

from django.http import HttpResponse
from django.views import View
from .tasks import new_post_email_task


class ArticlesList(ListView):
    model = Article
    ordering = '-date'
    template_name = 'articles.html'
    context_object_name = 'article'
    paginate_by = 10


class ArticleDetail(DetailView):
    model = Article
    template_name = 'article.html'
    context_object_name = 'article'


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_news',)
    raise_exception = True
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        if self.request.path == '/news/articles/create/':
            article.type = 'A'
        article.save()
        new_post_email_task.delay(article.id)
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_news',)
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'


class ArticleDelete(DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')


class NewsSearch(ListView):
    model = Article
    ordering = 'date'
    template_name = 'news_search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(
                user=request.user,
                category=category
            )
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscription = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        'subscriptions.html',
        {'categories': categories_with_subscription},
    )


class IndexView(View):
    def get(self, request):
        hello.delay()
        return HttpResponse('Hello!')
