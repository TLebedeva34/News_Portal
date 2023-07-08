from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import Article
from .filters import NewsFilter
from .forms import ArticleForm


class ArticlesList(ListView):
    model = Article
    ordering = '-date'
    template_name = 'articles.html'
    context_object_name = 'article'
    paginate_by = 10

#    def get_queryset(self):
#        queryset = super().get_queryset()
#        self.filterset = ArticleFilter(self.request.GET, queryset)
#        return self.filterset.qs
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['filterset'] = self.filterset
#        return context


class ArticleDetail(DetailView):
    model = Article
    template_name = 'article.html'
    context_object_name = 'article'


class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'


class ArticleUpdate(UpdateView):
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
        return  self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
