# Generated by Django 3.2.9 on 2022-09-03 20:26

from django.db import migrations, models
import django.db.models.deletion
import guests.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('invitation_id', models.CharField(db_index=True, default=guests.models._random_uuid, max_length=32, unique=True)),
                ('save_the_date_sent', models.DateTimeField(blank=True, default=None, null=True)),
                ('save_the_date_viewed', models.DateTimeField(blank=True, default=None, null=True)),
                ('invite_sent', models.DateTimeField(blank=True, default=None, null=True)),
                ('invite_viewed', models.DateTimeField(blank=True, default=None, null=True)),
            ],
            options={
                'db_table': 'party',
            },
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('attending_canada', models.BooleanField(default=None, null=True)),
                ('attending_france', models.BooleanField(default=None, null=True)),
                ('dietary_restrictions', models.TextField(blank=True, default=None, null=True)),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guests.party')),
            ],
            options={
                'db_table': 'guests',
            },
        ),
    ]