# Generated by Django 2.2 on 2020-05-20 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DJUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('_password', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=16, unique=True)),
                ('icon', models.CharField(default='', max_length=256, null=True)),
            ],
            options={
                'db_table': 'DJ_user',
            },
        ),
    ]
