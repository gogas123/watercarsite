# Generated by Django 2.0.5 on 2018-05-24 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waterapp', '0004_constructionpost'),
    ]

    operations = [
        migrations.CreateModel(
            name='TOS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use', models.TextField()),
                ('infor', models.TextField()),
            ],
        ),
    ]
