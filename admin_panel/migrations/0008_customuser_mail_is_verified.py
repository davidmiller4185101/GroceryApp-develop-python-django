# Generated by Django 3.2.3 on 2022-07-22 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0007_customuser_is_phone_veryfied'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='mail_is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
