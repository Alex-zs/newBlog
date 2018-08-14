# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-08-07 17:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import main.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutMe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('abstract', models.CharField(max_length=100)),
                ('html_file', models.FileField(null=True, upload_to='markdown/')),
                ('content', models.TextField(blank=True, max_length=10000, null=True)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('cover', models.ImageField(storage=main.storage.ImageStorage(), upload_to='aboutMe', verbose_name='封面')),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(storage=main.storage.ImageStorage(), upload_to='album', verbose_name='照片')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('html_file', models.FileField(null=True, upload_to='markdown/')),
                ('content', models.TextField(blank=True, max_length=10000, null=True)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='发表时间')),
                ('views', models.PositiveIntegerField(default=0)),
                ('abstract', models.CharField(blank=True, max_length=60, null=True, verbose_name='摘要')),
                ('cover', models.ImageField(storage=main.storage.ImageStorage(), upload_to='article_img', verbose_name='封面')),
            ],
        ),
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('html_file', models.FileField(null=True, upload_to='markdown/')),
                ('content', models.TextField(blank=True, max_length=10000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IpRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=18)),
                ('time', models.DateTimeField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Article')),
            ],
        ),
    ]