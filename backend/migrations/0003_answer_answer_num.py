# Generated by Django 3.1.1 on 2020-11-22 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20201122_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='answer_num',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
