# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('publication', models.ForeignKey(to='test_app.Publication', on_delete=models.CASCADE)),
                ('writer', smart_selects.db_fields.ChainedManyToManyField(chained_model_field=b'publications', to='test_app.Writer', chained_field=b'publication')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=100)),
                ('continent', models.ForeignKey(to='test_app.Continent', on_delete=models.CASCADE)),
                ('country', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'continent', to='test_app.Country', chained_field=b'continent', auto_choose=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
