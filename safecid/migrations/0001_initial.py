# Generated by Django 5.0.6 on 2024-07-08 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sido', models.CharField(max_length=100)),
                ('sigungu', models.CharField(max_length=100)),
                ('eupmyundong', models.CharField(max_length=100)),
            ],
        ),
    ]
