# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 22:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20170208_0728'),
    ]

    operations = [
        migrations.RenameField(
            model_name='language',
            old_name='name',
            new_name='native_name',
        ),
        migrations.AlterUniqueTogether(
            name='contenttr',
            unique_together=set([('language', 'content')]),
        ),
        migrations.AlterUniqueTogether(
            name='periodtr',
            unique_together=set([('language', 'period')]),
        ),
        migrations.AlterUniqueTogether(
            name='topictr',
            unique_together=set([('language', 'topic')]),
        ),
    ]