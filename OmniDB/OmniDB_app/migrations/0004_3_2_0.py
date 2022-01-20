# manually created

from django.db import migrations


def populate_technologies(apps, schema_editor):
    Technology = apps.get_model('OmniDB_app', 'Technology')
    Technology(name='mssql').save()


class Migration(migrations.Migration):

    dependencies = [
        ('OmniDB_app', '0003_3_1_0'),
    ]

    operations = [
        migrations.RunPython(
            code=populate_technologies,
        )
    ]
