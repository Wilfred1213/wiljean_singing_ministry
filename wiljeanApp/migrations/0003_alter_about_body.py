# Generated by Django 5.0 on 2024-03-10 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiljeanApp', '0002_about_alter_quotes_table_alter_slider_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='body',
            field=models.TextField(max_length=10000),
        ),
    ]
