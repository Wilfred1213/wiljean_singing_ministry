# Generated by Django 5.0 on 2024-03-13 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiljeanApp', '0011_album_tracks'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='cover',
            field=models.ImageField(null=True, upload_to='media'),
        ),
    ]
