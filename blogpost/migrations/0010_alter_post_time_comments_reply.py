# Generated by Django 5.1.4 on 2025-02-11 01:23

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0009_alter_post_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateField(blank=True, default=datetime.datetime(2025, 2, 11, 1, 23, 39, 79711), null=True),
        ),
        migrations.CreateModel(
            name='Comments_reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.CharField(max_length=100)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogpost.comments')),
            ],
        ),
    ]
