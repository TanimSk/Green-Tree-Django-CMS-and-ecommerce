# Generated by Django 2.2.3 on 2022-04-22 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(default='Not given', max_length=20),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(default='Not given'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='Not given', max_length=250),
        ),
    ]
