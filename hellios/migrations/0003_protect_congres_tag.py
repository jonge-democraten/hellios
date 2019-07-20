# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hellios', '0002_auto_20161228_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='congres',
            name='tag',
            field=models.ForeignKey(to='hellios.Tag', on_delete=django.db.models.deletion.PROTECT, verbose_name='Congrestag'),
        ),
    ]
