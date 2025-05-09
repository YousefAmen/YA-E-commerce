# Generated by Django 5.0.7 on 2024-09-27 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0033_alter_order_summary_shipping_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_country',
            field=models.CharField(blank=True, choices=[('United Kingdom', 'United Kingdom'), ('France', 'France'), ('Germany', 'Germany'), ('Italy', 'Italy'), ('Spain', 'Spain'), ('Greece', 'Greece'), ('Switzerland', 'Switzerland'), ('Austria', 'Austria'), ('Netherlands', 'Netherlands'), ('Portugal', 'Portugal'), ('Sweden', 'Sweden'), ('Denmark', 'Denmark'), ('Norway', 'Norway'), ('Finland', 'Finland'), ('Belgium', 'Belgium'), ('Ireland', 'Ireland'), ('Iceland', 'Iceland'), ('United States', 'United States'), ('Canada', 'Canada'), ('Mexico', 'Mexico'), ('China', 'China'), ('JP', 'Japan'), ('India', 'India'), ('South Korea', 'South Korea'), ('Indonesia', 'Indonesia'), ('Thailand', 'Thailand'), ('Malaysia', 'Malaysia'), ('Philippines', 'Philippines'), ('Vietnam', 'Vietnam'), ('Singapore', 'Singapore'), ('Taiwan', 'Taiwan'), ('Hong Kong', 'Hong Kong'), ('Macau', 'Macau'), ('Brazil', 'Brazil'), ('Argentina', 'Argentina'), ('Colombia', 'Colombia'), ('Peru', 'Peru'), ('Chile', 'Chile'), ('Venezuela', 'Venezuela'), ('Australia', 'Australia'), ('New Zealand', 'New Zealand'), ('South Africa', 'South Africa'), ('Egypt', 'Egypt'), ('Morocco', 'Morocco'), ('Algeria', 'Algeria'), ('Nigeria', 'Nigeria'), ('Bahrain', 'Bahrain'), ('Kuwait', 'Kuwait'), ('Oman', 'Oman'), ('Qatar', 'Qatar'), ('Saudi Arabia', 'Saudi Arabia'), ('United Arab Emirates', 'United Arab Emirates'), ('Algeria', 'Algeria'), ('Libya', 'Libya'), ('Morocco', 'Morocco'), ('Sudan', 'Sudan'), ('Tunisia', 'Tunisia')], default='US', max_length=255),
        ),
    ]
