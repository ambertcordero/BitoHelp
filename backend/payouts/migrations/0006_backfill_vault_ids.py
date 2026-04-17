from django.db import migrations, models


def backfill_vault_ids(apps, schema_editor):
    PayoutApproval = apps.get_model('payouts', 'PayoutApproval')
    refs = (
        PayoutApproval.objects
        .values('donation_ref')
        .annotate(earliest=models.Min('created_at'))
        .order_by('earliest')
    )
    for idx, ref_row in enumerate(refs, start=1):
        vault_id = f'VLT-{idx:04d}'
        PayoutApproval.objects.filter(
            donation_ref=ref_row['donation_ref']
        ).update(vault_id=vault_id)


class Migration(migrations.Migration):

    dependencies = [
        ('payouts', '0005_payoutapproval_vault_id'),
    ]

    operations = [
        migrations.RunPython(backfill_vault_ids, migrations.RunPython.noop),
    ]
