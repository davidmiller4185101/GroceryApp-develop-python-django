# Generated by Django 3.2.3 on 2021-11-11 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'grocer'), (2, 'buyer'), (3, 'deliverer'), (4, 'admin')], default=1),
        ),
    ]
