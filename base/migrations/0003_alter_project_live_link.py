# Generated by Django 4.0.3 on 2022-04-08 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_project_reviews_project_ratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='live_link',
            field=models.TextField(blank=True),
        ),
    ]
