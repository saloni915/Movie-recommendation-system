# Generated by Django 2.1.2 on 2018-11-05 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videosharing1', '0008_auto_20181105_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='channel_discription',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='channel',
            name='email',
            field=models.EmailField(default='', max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name='channel',
            name='facebook_link',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='channel',
            name='instragram_link',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]
