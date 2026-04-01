import os
import django
import hashlib
import secrets
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitohelp_api.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
from donations.models import Donation
from nonprofits.models import Nonprofit
from payouts.models import PayoutApproval

# Clear existing
Donation.objects.all().delete()
PayoutApproval.objects.all().delete()
print("Cleared existing donations and payout approvals.")

nonprofits = list(Nonprofit.objects.all())
if not nonprofits:
    print("No nonprofits found. Run seed_nonprofits.py first.")
    exit()

# Seed Donations
donations_data = [
    {
        'txid': 'abc123tx0001',
        'recipient': nonprofits[0].bch_address,
        'amount': Decimal('0.05'),
        'coin': 'BCH',
        'cause': nonprofits[0].name,
        'message': 'Keep up the good work!',
        'donor_name': 'Juan dela Cruz',
        'donor_email': 'juan@example.com',
        'donor_contact': '09171234567',
        'nonprofit': nonprofits[0],
        'contract': 'vault',
        'interval': 'monthly',
        'payout_mode': 'inbox_approval',
        'explorer_url': 'https://chipnet.imaginary.cash/tx/abc123tx0001',
    },
    {
        'txid': 'def456tx0002',
        'recipient': nonprofits[1].bch_address,
        'amount': Decimal('0.10'),
        'coin': 'BCH',
        'cause': nonprofits[1].name,
        'message': 'For the community.',
        'donor_name': 'Maria Santos',
        'donor_email': 'maria@example.com',
        'donor_contact': '',
        'nonprofit': nonprofits[1],
        'contract': 'vault',
        'interval': 'weekly',
        'payout_mode': 'smart',
        'explorer_url': 'https://chipnet.imaginary.cash/tx/def456tx0002',
    },
    {
        'txid': 'ghi789tx0003',
        'recipient': nonprofits[2].bch_address,
        'amount': Decimal('0.025'),
        'coin': 'BCH',
        'cause': nonprofits[2].name,
        'message': '',
        'donor_name': '',
        'donor_email': 'donor3@example.com',
        'donor_contact': '',
        'nonprofit': nonprofits[2],
        'contract': 'recurring',
        'interval': 'daily',
        'payout_mode': 'smart',
        'explorer_url': 'https://chipnet.imaginary.cash/tx/ghi789tx0003',
    },
]

created_donations = []
for d in donations_data:
    donation = Donation.objects.create(**d)
    created_donations.append(donation)
    print(f"  Created Donation: {donation}")

# Seed Payout Approvals
payouts_data = [
    {
        'donation_ref': 'VAULT-001',
        'donation': created_donations[0],
        'donor_email': 'juan@example.com',
        'donor_name': 'Juan dela Cruz',
        'recipient_address': nonprofits[0].bch_address,
        'vault_address': 'bchtest:qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy',
        'payout_amount_satoshis': 500000,
        'coin': 'BCH',
        'interval_label': 'monthly',
        'interval_blocks': 4320,
        'cycle_number': 1,
        'total_cycles': 6,
        'due_at': timezone.now() + timedelta(days=30),
        'approval_token_hash': hashlib.sha256(secrets.token_bytes(32)).hexdigest(),
        'approval_expires_at': timezone.now() + timedelta(hours=24),
        'status': 'pending',
        'idempotency_key': 'VAULT-001-cycle-1',
    },
    {
        'donation_ref': 'VAULT-002',
        'donation': created_donations[1],
        'donor_email': 'maria@example.com',
        'donor_name': 'Maria Santos',
        'recipient_address': nonprofits[1].bch_address,
        'vault_address': 'bchtest:qp4aadjrpu73d2wxwkxkcrt6gqxgu6a7usxfm96fst',
        'payout_amount_satoshis': 1000000,
        'coin': 'BCH',
        'interval_label': 'weekly',
        'interval_blocks': 1008,
        'cycle_number': 2,
        'total_cycles': 4,
        'due_at': timezone.now() + timedelta(days=7),
        'approval_token_hash': hashlib.sha256(secrets.token_bytes(32)).hexdigest(),
        'approval_expires_at': timezone.now() + timedelta(hours=24),
        'status': 'approved',
        'idempotency_key': 'VAULT-002-cycle-2',
    },
    {
        'donation_ref': 'VAULT-003',
        'donation': created_donations[2],
        'donor_email': 'donor3@example.com',
        'donor_name': 'Anonymous',
        'recipient_address': nonprofits[2].bch_address,
        'vault_address': 'bchtest:qpwngrc5j8d7vvz0a0mn0z5yak4axf8mvqnkzgd4n8',
        'payout_amount_satoshis': 250000,
        'coin': 'BCH',
        'interval_label': 'daily',
        'interval_blocks': 144,
        'cycle_number': 1,
        'total_cycles': 30,
        'due_at': timezone.now() + timedelta(days=1),
        'approval_token_hash': hashlib.sha256(secrets.token_bytes(32)).hexdigest(),
        'approval_expires_at': timezone.now() + timedelta(hours=24),
        'status': 'executed',
        'txid': 'executed_tx_abc999',
        'idempotency_key': 'VAULT-003-cycle-1',
    },
]

for p in payouts_data:
    payout = PayoutApproval.objects.create(**p)
    print(f"  Created PayoutApproval: {payout.donation_ref} [{payout.status}]")

print(f"\n  Total Donations: {Donation.objects.count()}")
print(f"  Total Payout Approvals: {PayoutApproval.objects.count()}")
print("  Done!")
