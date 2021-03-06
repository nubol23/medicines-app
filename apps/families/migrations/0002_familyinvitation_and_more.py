# Generated by Django 4.0.3 on 2022-03-10 20:59

import uuid

import django.contrib.postgres.fields.citext
import django.db.models.deletion
from django.conf import settings
from django.contrib.postgres.operations import CITextExtension
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('families', '0001_initial'),
    ]

    operations = [
        CITextExtension(),
        migrations.CreateModel(
            name='FamilyInvitation',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', django.contrib.postgres.fields.citext.CIEmailField(max_length=255)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('phone_number', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('PE', 'Pending'), ('AC', 'Accepted'), ('RE', 'Revoked')], default='PE', max_length=2)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invitations', to='families.family')),
                ('invited_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_invitations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='familyinvitation',
            index=models.Index(fields=['-created_on'], name='families_fa_created_5346f9_idx'),
        ),
    ]
