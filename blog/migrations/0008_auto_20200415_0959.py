# Generated by Django 2.2.11 on 2020-04-15 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(blank=True, default='', null=True, upload_to='blogPhotos'),
        ),
    ]