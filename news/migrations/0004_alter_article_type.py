# Generated by Django 4.2.2 on 2023-08-06 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_article_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='type',
            field=models.CharField(choices=[('A', 'Статья'), ('N', 'Новость')], default='N', max_length=1),
        ),
    ]
