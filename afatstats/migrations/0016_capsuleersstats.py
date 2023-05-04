# Generated by Django 4.0.10 on 2023-05-04 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afatstats', '0015_capsuleerscaps_capsuleersfax_capsuleerssupers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CapsuleersStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stat', models.CharField(max_length=255)),
                ('character_name', models.CharField(max_length=255)),
                ('character_id', models.IntegerField(default=0)),
                ('corporation_name', models.CharField(max_length=255)),
                ('corporation_id', models.IntegerField(default=0)),
                ('fats', models.IntegerField(default=0)),
            ],
        ),
    ]