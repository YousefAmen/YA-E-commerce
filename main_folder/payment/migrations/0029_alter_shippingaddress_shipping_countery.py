# Generated by Django 5.0.7 on 2024-09-21 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0028_rename_uuid_order_order_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_countery',
            field=models.CharField(blank=True, choices=[('UK', 'United Kingdom'), ('FR', 'France'), ('DE', 'Germany'), ('IT', 'Italy'), ('ES', 'Spain'), ('GR', 'Greece'), ('CH', 'Switzerland'), ('AT', 'Austria'), ('NL', 'Netherlands'), ('PT', 'Portugal'), ('SE', 'Sweden'), ('DK', 'Denmark'), ('NO', 'Norway'), ('FI', 'Finland'), ('BE', 'Belgium'), ('IE', 'Ireland'), ('IS', 'Iceland'), ('US', 'United States'), ('CA', 'Canada'), ('MX', 'Mexico'), ('CN', 'China'), ('JP', 'Japan'), ('IN', 'India'), ('KR', 'South Korea'), ('ID', 'Indonesia'), ('TH', 'Thailand'), ('MY', 'Malaysia'), ('PH', 'Philippines'), ('VI', 'Vietnam'), ('SG', 'Singapore'), ('TW', 'Taiwan'), ('HK', 'Hong Kong'), ('MO', 'Macau'), ('BR', 'Brazil'), ('AR', 'Argentina'), ('CO', 'Colombia'), ('PE', 'Peru'), ('CL', 'Chile'), ('VE', 'Venezuela'), ('ZA', 'South Africa'), ('EG', 'Egypt'), ('MA', 'Morocco'), ('DZ', 'Algeria'), ('NG', 'Nigeria'), ('AU', 'Australia'), ('NZ', 'New Zealand')], max_length=255),
        ),
    ]
