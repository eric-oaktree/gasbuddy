# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-20 19:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('item_id', models.TextField()),
                ('last_price', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('volume', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Harvester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('harv_id', models.TextField()),
                ('cycle', models.IntegerField()),
                ('yld', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('region_id', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Setup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setup', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Ship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('cargo', models.IntegerField()),
                ('yld_bonus', models.DecimalField(decimal_places=2, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('p_qty', models.IntegerField()),
                ('s_qty', models.IntegerField()),
                ('p_gas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='p_gas_re', to='home.Gas')),
                ('s_gas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='s_gas_re', to='home.Gas')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('station_id', models.TextField()),
            ],
        ),
    ]