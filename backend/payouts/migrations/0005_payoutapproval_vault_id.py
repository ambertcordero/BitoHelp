from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payouts', '0004_tighten_txid_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='payoutapproval',
            name='vault_id',
            field=models.CharField(
                blank=True, db_index=True, help_text='Auto-assigned vault identifier (VLT-0001)',
                max_length=20,
            ),
        ),
    ]
