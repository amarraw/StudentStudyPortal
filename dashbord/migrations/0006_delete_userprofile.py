# Generated by Django 5.1.2 on 2024-10-20 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dashbord", "0005_userprofile"),
    ]

    operations = [
        migrations.DeleteModel(
            name="UserProfile",
        ),
    ]
