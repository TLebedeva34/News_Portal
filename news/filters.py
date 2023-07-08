from django_filters import FilterSet, DateFilter, ModelMultipleChoiceFilter
from django.forms import DateInput
from .models import Article, Category


#class ArticleFilter(FilterSet):
#    category = ModelMultipleChoiceFilter(
#       field_name='CategoryArticle__category',
#       queryset=Category.objects.all(),
#       label='Category',
#       conjoined=True,
#    )
#
#    class Meta:
#        model = Article
#        fields = {
#            'title': ['icontains'],
#            'category': ['exact'],
#        }


class NewsFilter(FilterSet):
    added_after = DateFilter(
        field_name='date',
        lookup_expr='gt',
        widget=DateInput(
            format='%d-%m-%Y',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Article
        fields = {
            'title': ['icontains'],
            'category': ['exact']
        }
