# Generated by Django 4.0.10 on 2023-05-03 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afatstats', '0007_corporationdata_corporationmains_corporationalts'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporationdata',
            name='rel_fats',
            field=models.IntegerField(default=0),
        ),
    ]
