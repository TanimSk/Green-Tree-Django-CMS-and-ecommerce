# Generated by Django 2.2.3 on 2022-05-01 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_post_vacancy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(default=None, null=True, upload_to='images/'),
        ),
    ]
