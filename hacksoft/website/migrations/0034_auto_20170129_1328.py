# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-29 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0033_blogpostspage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpostspage',
            old_name='cover_image',
            new_name='header_image',
        ),
        migrations.AddField(
            model_name='blogpostspage',
            name='header_text',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
