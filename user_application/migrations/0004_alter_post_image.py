# Generated by Django 5.0.1 on 2024-06-05 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_application', '0003_comment_created_comment_updated_like_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='image/'),
        ),
    ]
