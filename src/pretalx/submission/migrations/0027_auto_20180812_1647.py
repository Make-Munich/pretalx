# Generated by Django 2.0.8 on 2018-08-12 21:47

from django.db import migrations
import i18nfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0026_auto_20180811_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question',
            field=i18nfield.fields.I18nCharField(max_length=800, verbose_name='question'),
        ),
    ]
