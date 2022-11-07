# Generated by Django 4.1.3 on 2022-11-07 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('second_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='second name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='authors/')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.CharField(max_length=250)),
                ('release_date', models.DateField()),
                ('addition_date', models.DateField()),
                ('free', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='books/')),
                ('code', models.CharField(max_length=150)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='books.author')),
                ('genres', models.ManyToManyField(to='books.genre')),
                ('translator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translators', to='books.author')),
            ],
        ),
    ]