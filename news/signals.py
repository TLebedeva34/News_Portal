from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Article


@receiver(post_save, sender=Article)
def news_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        ubscriptios__category=instance.category
    ).values_lisrt('email', flat=True)

    subject = f'Новая статья в категории {instance.category}'

    text_content = (
        f'Ссылка на статью:http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на статью</a>'

    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
