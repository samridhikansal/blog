# Generated by Django 5.1.4 on 2025-02-01 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0006_alter_comments_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='author',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
