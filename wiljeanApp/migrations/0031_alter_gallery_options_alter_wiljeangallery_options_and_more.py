# Generated by Django 5.0 on 2024-04-10 19:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiljeanApp', '0030_contact_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gallery',
            options={'ordering': ('-photo',)},
        ),
        migrations.AlterModelOptions(
            name='wiljeangallery',
            options={'ordering': ('-photo',)},
        ),
        migrations.CreateModel(
            name='blogComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('message', models.TextField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wiljeanApp.blog')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
