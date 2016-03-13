# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-13 22:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('public', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='FolderPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ehealth.Folder')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('source', models.CharField(max_length=128)),
                ('summary', models.TextField()),
                ('url', models.URLField()),
                ('readability_score', models.IntegerField()),
                ('sentiment_score', models.IntegerField()),
                ('subjectivity_score', models.IntegerField()),
                ('times_saved', models.BigIntegerField()),
                ('category', models.ManyToManyField(to='ehealth.Category')),
            ],
        ),
        migrations.CreateModel(
            name='PageCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ehealth.Category')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ehealth.Page')),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('category', models.ManyToManyField(to='ehealth.Category')),
            ],
        ),
        migrations.CreateModel(
            name='QueryCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ehealth.Category')),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ehealth.Query')),
            ],
        ),
        migrations.CreateModel(
            name='Searcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(blank=True, upload_to=b'profile_images')),
                ('history', models.ManyToManyField(to='ehealth.Query')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ehealth.Query')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ehealth.Searcher')),
            ],
        ),
        migrations.AddField(
            model_name='folderpage',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ehealth.Page'),
        ),
        migrations.AddField(
            model_name='folder',
            name='pages',
            field=models.ManyToManyField(blank=True, to='ehealth.Page'),
        ),
        migrations.AddField(
            model_name='folder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folders', to='ehealth.Searcher'),
        ),
    ]
