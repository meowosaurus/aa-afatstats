# Generated by Django 4.0.10 on 2023-05-03 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('afatstats', '0006_alter_general_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorporationData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corporation_name', models.CharField(max_length=255, unique=True)),
                ('corporation_id', models.IntegerField(default=0)),
                ('corporation_ticker', models.CharField(max_length=255, unique=True)),
                ('member_count', models.IntegerField(default=0)),
                ('players', models.IntegerField(default=0)),
                ('fats', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CorporationMains',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_character', models.CharField(max_length=255, unique=True)),
                ('corporation_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='afatstats.corporationdata')),
            ],
        ),
        migrations.CreateModel(
            name='CorporationAlts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt_character', models.CharField(max_length=255, unique=True)),
                ('main_character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='afatstats.corporationmains')),
            ],
        ),
    ]
