# Generated by Django 2.1.7 on 2019-03-13 08:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('signals', '0034_auto_20190205_1149'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='signal',
            index=models.Index(fields=['created_at'], name='signals_sig_created_b90766_idx'),
        ),
    ]
