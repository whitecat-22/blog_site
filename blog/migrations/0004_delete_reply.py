# Generated by Django 3.1.4 on 2020-12-08 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment_contentimage_reply'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Reply',
        ),
    ]
