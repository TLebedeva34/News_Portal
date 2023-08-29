from celery import shared_task
from datetime import datetime
from .models import Article, Subscription
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def new_post_email_task(article_id):
    news = Article.objects.get(pk=article_id)
    categories = Article.category.all()
    title = Article.title
    subscribers_email = set(Subscription.objects.filter.values_list('user__email', flat=True))
    html_content = render_to_string(
        'new_article.html',
        {
            'text': news.title,
            'link': f'{settings.SITE_URL}/news/{article_id}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email
    )


@shared_task
def send_monday_email_task():
    today = datetime.now()
    last_week = today - datetime.timedelta(day=7)
    news = Article.objects.get(date__gte=last_week)
    categories = Article.category.all()
    title = Article.title
    subscribers_email = set(Subscription.objects.filter.values_list('user__email', flat=True))
    html_content = render_to_string(
        'monday_email.html',
        {
            'text': news.title,
            'link': f'{settings.SITE_URL}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email
    )
