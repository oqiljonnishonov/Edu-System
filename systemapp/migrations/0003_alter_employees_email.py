# Generated by Django 4.1.7 on 2023-03-12 13:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("systemapp", "0002_alter_moderatorinheri_level"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employees",
            name="email",
            field=models.CharField(
                max_length=50,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="email nust be entered in the format: 'example@demein'-> oqiljonnishonov@gmail.com.",
                        regex="\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,7}\\b",
                    )
                ],
            ),
        ),
    ]
