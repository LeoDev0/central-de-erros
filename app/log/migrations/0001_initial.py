# Generated by Django 2.2.13 on 2020-07-07 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('details', models.CharField(max_length=255)),
                ('level', models.CharField(choices=[('DEBUG', 'DEBUG'), ('WARNING', 'WARNING'), ('ERROR', 'ERROR')], max_length=20)),
                ('origin', models.GenericIPAddressField(protocol='IPv4')),
                ('events', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('archived', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
