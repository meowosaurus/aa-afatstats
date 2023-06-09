# Generated by Django 4.0.10 on 2023-05-04 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afatstats', '0014_capsuleersboosts_capsuleerslogi_capsuleerssnowflakes_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CapsuleersCaps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character_name', models.CharField(max_length=255, unique=True)),
                ('character_id', models.IntegerField(default=0)),
                ('corporation_name', models.CharField(max_length=255)),
                ('corporation_id', models.IntegerField(default=0)),
                ('fats', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CapsuleersFAX',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character_name', models.CharField(max_length=255, unique=True)),
                ('character_id', models.IntegerField(default=0)),
                ('corporation_name', models.CharField(max_length=255)),
                ('corporation_id', models.IntegerField(default=0)),
                ('fats', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CapsuleersSupers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character_name', models.CharField(max_length=255, unique=True)),
                ('character_id', models.IntegerField(default=0)),
                ('corporation_name', models.CharField(max_length=255)),
                ('corporation_id', models.IntegerField(default=0)),
                ('fats', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CapsuleersTitans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character_name', models.CharField(max_length=255, unique=True)),
                ('character_id', models.IntegerField(default=0)),
                ('corporation_name', models.CharField(max_length=255)),
                ('corporation_id', models.IntegerField(default=0)),
                ('fats', models.IntegerField(default=0)),
            ],
        ),
    ]
