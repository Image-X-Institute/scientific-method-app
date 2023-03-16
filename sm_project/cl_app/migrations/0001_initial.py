# Generated by Django 4.1.5 on 2023-03-15 23:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checklist_title', models.CharField(max_length=200, verbose_name='Checklist')),
                ('document', models.URLField(blank=True, max_length=150, verbose_name='Document Link')),
                ('checklist_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Checklist Users')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL, verbose_name='Creator Email')),
                ('researchers', models.ManyToManyField(related_name='researchers', to=settings.AUTH_USER_MODEL)),
                ('reviewers', models.ManyToManyField(blank=True, related_name='reviewers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChecklistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_title', models.CharField(max_length=200, verbose_name='Checklist Item')),
                ('item_status', models.IntegerField(choices=[(1, 'Completed'), (2, 'For Review'), (3, 'Incomplete')], default=3, verbose_name='Status')),
                ('time_estimate', models.DateField(blank=True, null=True, verbose_name='Estimated Completion Date')),
                ('item_checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cl_app.checklist', verbose_name='Checklist')),
            ],
        ),
    ]
