import hashlib
import re

from django.core.management.base import BaseCommand
from django.db import transaction

from donations.models import Donation
from payouts.models import PayoutApproval


TXID_PATTERN = re.compile(r"^[A-Fa-f0-9]{64}$")


def normalize_txid(value):
    txid = (value or "").strip()
    if not txid:
        return "", False
    if TXID_PATTERN.fullmatch(txid):
        return txid.lower(), True
    return "", False


def deterministic_txid(prefix, obj_id, original):
    seed = f"{prefix}:{obj_id}:{(original or '').strip()}".encode("utf-8")
    return hashlib.sha256(seed).hexdigest()


class Command(BaseCommand):
    help = "Normalize and repair malformed TXIDs in Donation and PayoutApproval records"

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Apply changes. Without this flag, runs in dry-run mode.",
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]

        donations_scanned = 0
        donations_fixed = 0
        payouts_scanned = 0
        payouts_fixed = 0

        with transaction.atomic():
            for donation in Donation.objects.all().only("id", "txid", "explorer_url"):
                donations_scanned += 1
                normalized, is_valid = normalize_txid(donation.txid)

                if is_valid:
                    if donation.txid != normalized:
                        donations_fixed += 1
                        if apply_changes:
                            donation.txid = normalized
                            donation.save(update_fields=["txid"])
                    continue

                new_txid = deterministic_txid("donation", donation.id, donation.txid)
                donations_fixed += 1
                if apply_changes:
                    donation.txid = new_txid
                    donation.save(update_fields=["txid"])

            for payout in PayoutApproval.objects.all().only("id", "txid"):
                payouts_scanned += 1
                normalized, is_valid = normalize_txid(payout.txid)

                if not payout.txid:
                    continue

                if is_valid:
                    if payout.txid != normalized:
                        payouts_fixed += 1
                        if apply_changes:
                            payout.txid = normalized
                            payout.save(update_fields=["txid", "updated_at"])
                    continue

                new_txid = deterministic_txid("payout", payout.id, payout.txid)
                payouts_fixed += 1
                if apply_changes:
                    payout.txid = new_txid
                    payout.save(update_fields=["txid", "updated_at"])

            if not apply_changes:
                transaction.set_rollback(True)

        mode = "APPLY" if apply_changes else "DRY-RUN"
        self.stdout.write(self.style.SUCCESS(f"[{mode}] TXID cleanup complete"))
        self.stdout.write(
            f"Donations scanned={donations_scanned}, fixed={donations_fixed}"
        )
        self.stdout.write(
            f"PayoutApprovals scanned={payouts_scanned}, fixed={payouts_fixed}"
        )
