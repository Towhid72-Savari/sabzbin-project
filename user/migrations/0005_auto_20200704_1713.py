# Generated by Django 3.0.2 on 2020-07-04 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200704_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userscoretransaction',
            name='points',
            field=models.CharField(choices=[('profile', '1'), ('referral', '1')], max_length=255),
        ),
    ]