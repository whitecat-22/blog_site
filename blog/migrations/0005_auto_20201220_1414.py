# Generated by Django 3.1.4 on 2020-12-20 05:14

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_delete_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=markdownx.models.MarkdownxField(),
        ),
    ]
