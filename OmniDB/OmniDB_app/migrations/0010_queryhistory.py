# Generated by Django 2.2.7 on 2020-05-13 17:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('OmniDB_app', '0009_tab'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('duration', models.TextField(default='')),
                ('status', models.TextField(default='')),
                ('connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OmniDB_app.Connection')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]