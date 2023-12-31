# Generated by Django 4.2.5 on 2023-10-01 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=250, verbose_name='Наименование')),
                ('course_preview', models.ImageField(blank=True, null=True, upload_to='main/course/', verbose_name='Превью')),
                ('course_description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'курс',
                'verbose_name_plural': 'курсы',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_name', models.CharField(max_length=250, verbose_name='Наименование')),
                ('lesson_description', models.TextField(verbose_name='Описание')),
                ('lesson_preview', models.ImageField(blank=True, null=True, upload_to='main/lesson/', verbose_name='Превью')),
                ('video_url', models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course', verbose_name='курс')),
            ],
            options={
                'verbose_name': 'урок',
                'verbose_name_plural': 'уроки',
            },
        ),
    ]
