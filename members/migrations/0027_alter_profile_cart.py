# Generated by Django 5.0.7 on 2024-08-26 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0026_profile_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cart',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
