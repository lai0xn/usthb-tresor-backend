# Generated by Django 5.0.2 on 2024-02-19 21:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('short', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, null=True, upload_to='files')),
                ('drive_link', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField()),
                ('title', models.CharField(max_length=100)),
                ('downloads_count', models.IntegerField(default=0)),
                ('file_type', models.CharField(choices=[('Lesson', 'cour'), ('TD', 'td'), ('Exam', 'exam')], max_length=20)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.module')),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short', models.CharField(max_length=10)),
                ('modules', models.ManyToManyField(to='files.module')),
            ],
        ),
    ]
