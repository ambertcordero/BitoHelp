import json
import logging
import re
from decimal import Decimal

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count

from openai import OpenAI
from decouple import config as decouple_config

from donations.models import Donation
from nonprofits.models import Nonprofit
from payouts.models import PayoutApproval
from users.models import WalletUser

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """\
You are Krypto, a friendly and knowledgeable AI assistant for CrypToCare \
(also known as BiToHelp).

CrypToCare is a blockchain-powered donation platform that enables \
cryptocurrency donations (specifically Bitcoin Cash / BCH) to verified \
nonprofit organizations.

Users can browse nonprofits by category, donate BCH directly to verified \
charities, track their donation history, and manage payout approvals.

Key features: direct BCH donations, recurring donation schedules via \
CashScript smart contracts, payout approval system with email verification, \
real-time donation tracking, and a donor profile page.

Categories of nonprofits: Animals, Poverty Alleviation, Children & Youth, \
Housing & Community Humanitarian Aid, Environment & Conservation.

IMPORTANT — WALLET CONNECTION:
Before a user/donor can donate, they MUST first connect their wallet using \
WalletConnect. The wallet-connect toggle switch is in the top navigation bar \
(header). When toggled on it opens the WalletConnect modal where the user \
scans a QR code or selects their wallet app. Only after a successful wallet \
connection can the user proceed to make donations on the /#/donate page.

IMPORTANT — DATA ACCESS:
You have access to the platform's database through tools. You can look up \
donations, nonprofits, wallet users, payout approvals, and aggregate stats. \
Use these tools whenever the user asks about specific data, numbers, or \
analytics — never guess numbers.

IMPORTANT — CHARTS & GRAPHS:
When the user asks for a chart, graph, or visual breakdown, FIRST call the \
relevant data tools to get real numbers, then include a chart spec in your \
reply using exactly this format (one block per chart):

[CHART]{"type":"bar","title":"Chart Title","labels":["A","B"],"datasets":[{"label":"Series","data":[10,20]}]}[/CHART]

Supported types: bar, pie, doughnut, line.
Never invent numbers — always fetch data via tools first.

RULES:
1. ONLY answer questions related to CrypToCare, cryptocurrency donations, \
BCH, blockchain philanthropy, and this platform. For anything else politely \
decline: "I'm specifically here to help with CrypToCare and BCH donations! \
Is there anything about our platform I can help you with?"
2. Include clickable dApp links when giving directions:
   /#/  /#/donate  /#/donor  /#/charities  /#/dashboard
   /#/mission  /#/about  /#/contact  /#/wallet-users
"""

# ---------------------------------------------------------------------------
# OpenAI tool definitions
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_donation_stats",
            "description": "Aggregate donation statistics: total count, total BCH, breakdowns by cause and coin.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_recent_donations",
            "description": "Most recent donations with txid, amount, cause, recipient, donor, timestamp.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of donations to return (default 10, max 50)",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_donations_by_wallet",
            "description": "All donations made by a specific wallet address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "wallet_address": {
                        "type": "string",
                        "description": "BCH wallet address of the donor",
                    }
                },
                "required": ["wallet_address"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_nonprofits",
            "description": "List nonprofits, optionally filtered by category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Category filter",
                        "enum": [
                            "animals",
                            "poverty",
                            "children_youth",
                            "housing_humanitarian",
                            "environment",
                        ],
                    },
                    "verified_only": {
                        "type": "boolean",
                        "description": "Only verified nonprofits (default true)",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_wallet_profile",
            "description": "Wallet user profile with donation history and summary stats.",
            "parameters": {
                "type": "object",
                "properties": {
                    "wallet_address": {
                        "type": "string",
                        "description": "BCH wallet address",
                    }
                },
                "required": ["wallet_address"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_payout_approvals",
            "description": "Payout approval records, optionally filtered by status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Filter by status",
                        "enum": [
                            "pending",
                            "approved",
                            "executed",
                            "expired",
                            "failed",
                        ],
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results (default 20, max 50)",
                    },
                },
                "required": [],
            },
        },
    },
]

# ---------------------------------------------------------------------------
# Tool execution helpers
# ---------------------------------------------------------------------------

class _DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


def _execute_tool(name, args):
    """Run a tool against the Django ORM and return a JSON-safe dict."""
    try:
        if name == "get_donation_stats":
            total = Donation.objects.count()
            total_amount = Donation.objects.aggregate(s=Sum("amount"))["s"] or 0
            by_cause = list(
                Donation.objects.values("cause")
                .annotate(count=Count("id"), total=Sum("amount"))
                .order_by("-count")
            )
            by_coin = list(
                Donation.objects.values("coin")
                .annotate(count=Count("id"), total=Sum("amount"))
                .order_by("-count")
            )
            return {
                "total_donations": total,
                "total_amount_bch": total_amount,
                "by_cause": by_cause,
                "by_coin": by_coin,
            }

        elif name == "get_recent_donations":
            limit = min(args.get("limit", 10), 50)
            qs = Donation.objects.select_related("nonprofit").order_by("-timestamp")[:limit]
            return {
                "donations": [
                    {
                        "txid": d.txid,
                        "amount": d.amount,
                        "coin": d.coin,
                        "cause": d.cause,
                        "recipient": d.recipient,
                        "donor_name": d.donor_name or "Anonymous",
                        "timestamp": d.timestamp.isoformat() if d.timestamp else None,
                        "nonprofit": d.nonprofit.name if d.nonprofit else None,
                    }
                    for d in qs
                ]
            }

        elif name == "get_donations_by_wallet":
            addr = args.get("wallet_address", "").strip().lower()
            qs = Donation.objects.filter(wallet_address=addr).order_by("-timestamp")
            return {
                "wallet_address": addr,
                "count": qs.count(),
                "total_amount": qs.aggregate(s=Sum("amount"))["s"] or 0,
                "donations": [
                    {
                        "txid": d.txid,
                        "amount": d.amount,
                        "cause": d.cause,
                        "recipient": d.recipient,
                        "timestamp": d.timestamp.isoformat() if d.timestamp else None,
                    }
                    for d in qs[:50]
                ],
            }

        elif name == "get_nonprofits":
            qs = Nonprofit.objects.all()
            if args.get("category"):
                qs = qs.filter(category=args["category"])
            if args.get("verified_only", True):
                qs = qs.filter(verified=True)
            return {
                "nonprofits": [
                    {
                        "id": n.id,
                        "name": n.name,
                        "category": n.category,
                        "bch_address": n.bch_address,
                        "verified": n.verified,
                        "total_donations": n.total_donations,
                        "donation_count": n.donation_count,
                    }
                    for n in qs
                ]
            }

        elif name == "get_wallet_profile":
            addr = args.get("wallet_address", "").strip().lower()
            try:
                user = WalletUser.objects.get(wallet_address=addr)
            except WalletUser.DoesNotExist:
                return {"error": f"No wallet user found for {addr}"}
            donations = Donation.objects.filter(wallet_address=addr).order_by("-timestamp")
            total_donated = donations.aggregate(s=Sum("amount"))["s"] or 0
            return {
                "wallet_address": addr,
                "display_name": user.display_name,
                "created_at": user.created_at.isoformat(),
                "last_connected_at": user.last_connected_at.isoformat(),
                "total_donated_bch": total_donated,
                "donation_count": donations.count(),
                "recent_donations": [
                    {
                        "amount": d.amount,
                        "cause": d.cause,
                        "recipient": d.recipient,
                        "timestamp": d.timestamp.isoformat() if d.timestamp else None,
                    }
                    for d in donations[:10]
                ],
            }

        elif name == "get_payout_approvals":
            qs = PayoutApproval.objects.all()
            if args.get("status"):
                qs = qs.filter(status=args["status"])
            limit = min(args.get("limit", 20), 50)
            qs = qs.order_by("-due_at")[:limit]
            return {
                "payouts": [
                    {
                        "id": p.id,
                        "donation_ref": p.donation_ref,
                        "recipient_address": p.recipient_address,
                        "payout_amount_satoshis": p.payout_amount_satoshis,
                        "status": p.status,
                        "due_at": p.due_at.isoformat(),
                        "approved_at": p.approved_at.isoformat() if p.approved_at else None,
                        "executed_at": p.executed_at.isoformat() if p.executed_at else None,
                    }
                    for p in qs
                ]
            }

        else:
            return {"error": f"Unknown tool: {name}"}

    except Exception as exc:
        logger.exception("Tool execution error: %s", name)
        return {"error": str(exc)}


def _extract_charts(text):
    """Pull [CHART]{...}[/CHART] blocks out of the AI reply.

    Returns (cleaned_text, list_of_chart_dicts).
    """
    charts = []

    def _replacer(match):
        try:
            charts.append(json.loads(match.group(1)))
        except json.JSONDecodeError:
            pass
        return ""

    cleaned = re.sub(r"\[CHART\]\s*(.*?)\s*\[/CHART\]", _replacer, text, flags=re.DOTALL)
    return cleaned.strip(), charts


# ---------------------------------------------------------------------------
# Public view
# ---------------------------------------------------------------------------

def _get_api_key():
    return decouple_config("OPENAI_API_KEY", default="")


@csrf_exempt
@require_POST
def chat_view(request):
    api_key = _get_api_key()
    if not api_key:
        return JsonResponse(
            {"error": "OpenAI API key is not configured on the server."},
            status=503,
        )

    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    message = body.get("message", "").strip()
    if not message:
        return JsonResponse({"error": "Message is required."}, status=400)

    history = body.get("history", [])

    client = OpenAI(api_key=api_key)

    # Build messages list for OpenAI Chat Completions
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for entry in history:
        role = entry.get("role", "user")
        text = entry.get("content", "")
        if text and role in ("user", "assistant"):
            messages.append({"role": role, "content": text})
    messages.append({"role": "user", "content": message})

    try:
        reply = ""
        # Tool-calling loop — max 5 round-trips to prevent runaway calls
        for _ in range(5):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=TOOLS,
            )
            choice = response.choices[0]

            if choice.message.tool_calls:
                messages.append(choice.message)
                for tc in choice.message.tool_calls:
                    try:
                        fn_args = json.loads(tc.function.arguments) if tc.function.arguments else {}
                    except json.JSONDecodeError:
                        fn_args = {}
                    result = _execute_tool(tc.function.name, fn_args)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": json.dumps(result, cls=_DecimalEncoder),
                        }
                    )
            else:
                reply = choice.message.content or ""
                break

        cleaned_reply, charts = _extract_charts(reply)
    except Exception as exc:
        logger.exception("OpenAI API call failed")
        return JsonResponse(
            {"error": f"AI service error: {exc}"},
            status=502,
        )

    return JsonResponse({"reply": cleaned_reply, "charts": charts})
