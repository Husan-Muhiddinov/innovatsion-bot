# Generated by Django 4.1.7 on 2023-04-06 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_alter_ids_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='user_status',
            field=models.BooleanField(default=False, null=True),
        ),
    ]