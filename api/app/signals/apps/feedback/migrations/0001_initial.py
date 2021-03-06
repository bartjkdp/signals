# Generated by Django 2.1.7 on 2019-03-27 16:12

import django.db.models.deletion
from django.db import migrations, models

import signals.apps.feedback.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('signals', '0041_auto_20190325_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('token', models.UUIDField(
                    db_index=True,
                    default=signals.apps.feedback.models.generate_token,
                    primary_key=True,
                    serialize=False
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('submitted_at', models.DateTimeField(editable=False, null=True)),
                ('is_satisfied', models.BooleanField(null=True)),
                ('allows_contact', models.BooleanField(default=False)),
                ('text', models.TextField(blank=True, max_length=1000, null=True)),
                ('text_extra', models.TextField(blank=True, max_length=1000, null=True)),
                ('_signal', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='feedback',
                    to='signals.Signal'
                )),
            ],
        ),
        migrations.CreateModel(
            name='StandardAnswer',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('is_visible', models.BooleanField(default=True)),
                ('is_satisfied', models.BooleanField(default=True)),
                ('text', models.TextField(max_length=1000)),
            ],
        ),
    ]
