# Generated by Django 5.0 on 2024-03-10 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiljeanApp', '0003_alter_about_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
            ],
        ),
    ]
