from django.db import migrations

def run_manual_updates(apps, schema_editor):
    Invoice = apps.get_model('invoice', 'Invoice')

    # ✅ Your custom update: Change invoice_type=0 ➝ invoice_type=1
    Invoice.objects.filter(invoice_type=0).update(invoice_type=1)


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(run_manual_updates),
    ]
