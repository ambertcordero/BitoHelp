from django.core.management.base import BaseCommand
from django.db import transaction

from donations.models import Donation
from payouts.models import PayoutApproval
from users.models import WalletUser


class Command(BaseCommand):
    help = (
        'Backfill WalletUser records from historical Donations and '
        'PayoutApproval records.  Idempotent — safe to run multiple times.'
    )

    def handle(self, *args, **options):
        addresses = set()

        # 1) Collect wallet addresses from Donations
        donation_addrs = (
            Donation.objects
            .exclude(wallet_address='')
            .values_list('wallet_address', flat=True)
            .distinct()
        )
        for addr in donation_addrs:
            normalized = (addr or '').lower().strip()
            if normalized:
                addresses.add(normalized)

        # Also try the contract (vault) field as a donor-side address
        vault_addrs = (
            Donation.objects
            .exclude(contract='')
            .values_list('contract', flat=True)
            .distinct()
        )
        for addr in vault_addrs:
            normalized = (addr or '').lower().strip()
            if normalized:
                addresses.add(normalized)

        # 2) Collect from PayoutApproval via linked donation wallet_address
        linked_addrs = (
            PayoutApproval.objects
            .filter(donation__isnull=False)
            .exclude(donation__wallet_address='')
            .values_list('donation__wallet_address', flat=True)
            .distinct()
        )
        for addr in linked_addrs:
            normalized = (addr or '').lower().strip()
            if normalized:
                addresses.add(normalized)

        # Also collect vault_address from PayoutApproval directly
        payout_vault_addrs = (
            PayoutApproval.objects
            .exclude(vault_address='')
            .values_list('vault_address', flat=True)
            .distinct()
        )
        for addr in payout_vault_addrs:
            normalized = (addr or '').lower().strip()
            if normalized:
                addresses.add(normalized)

        self.stdout.write(f'Found {len(addresses)} unique wallet addresses to backfill.')

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for addr in addresses:
                _, created = WalletUser.objects.update_or_create(
                    wallet_address=addr,
                    defaults={},
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

            # Backfill wallet_address on Donations that have a contract
            # but no wallet_address (historical records).
            backfilled_addr = 0
            for donation in Donation.objects.filter(wallet_address='').exclude(contract=''):
                donation.wallet_address = donation.contract.lower().strip()
                donation.save(update_fields=['wallet_address'])
                backfilled_addr += 1

            # Also backfill the wallet_user FK on Donations that have
            # a wallet_address but no wallet_user linked yet.
            linked = 0
            for user in WalletUser.objects.all():
                count = (
                    Donation.objects
                    .filter(wallet_address=user.wallet_address, wallet_user__isnull=True)
                    .update(wallet_user=user)
                )
                linked += count

        self.stdout.write(self.style.SUCCESS(
            f'Done.  Created: {created_count}  |  Already existed: {updated_count}  |  '
            f'Donation addresses backfilled: {backfilled_addr}  |  '
            f'Donations linked to users: {linked}'
        ))
