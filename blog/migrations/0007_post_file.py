# Generated by Django 4.0.3 on 2022-03-16 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='blog/files/%Y/%m/%d'),
        ),
    ]
