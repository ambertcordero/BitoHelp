import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from openai import OpenAI
from decouple import config as decouple_config

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are Krypto, a friendly and knowledgeable AI assistant for CrypToCare "
    "(also known as BiToHelp).\n\n"
    "CrypToCare is a blockchain-powered donation platform that enables cryptocurrency "
    "donations (specifically Bitcoin Cash / BCH) to verified nonprofit organizations.\n\n"
    "The platform is built with Vue 3 (Quasar Framework) on the frontend and Django "
    "REST Framework on the backend.\n\n"
    "Users can browse nonprofits by category, donate BCH directly to verified charities, "
    "track their donation history, and manage payout approvals.\n\n"
    "Key features: direct BCH donations, recurring donation schedules via CashScript "
    "smart contracts, payout approval system with email verification, real-time donation "
    "tracking, and a donor profile page.\n\n"
    "Categories of nonprofits: Animals, Poverty Alleviation, Children & Youth, "
    "Housing & Community Humanitarian Aid, Environment & Conservation.\n\n"
    "The donor page shows a connected wallet's donation history and transaction records.\n\n"
    "You are helpful, concise, and enthusiastic about cryptocurrency philanthropy. "
    "If you don't know something, say so honestly.\n\n"
    "IMPORTANT RULES:\n"
    "1. You must ONLY answer questions related to CrypToCare/BiToHelp, cryptocurrency "
    "donations, BCH, blockchain philanthropy, and how to use this platform. "
    "If a user asks about anything unrelated (e.g. coding help, general knowledge, "
    "weather, sports, politics, personal advice, other apps), politely decline and "
    "redirect them back to CrypToCare topics. Say something like: "
    "'I'm specifically here to help with CrypToCare and BCH donations! "
    "Is there anything about our platform I can help you with?'\n"
    "2. When giving directions or guidance about CrypToCare pages, include the "
    "relevant dApp page links using this exact format so they become clickable:\n"
    "   - Home page: /#/\n"
    "   - Donate page: /#/donate\n"
    "   - Donor profile: /#/donor\n"
    "   - Charities/nonprofits list: /#/charities\n"
    "   - Dashboard: /#/dashboard\n"
    "   - Mission page: /#/mission\n"
    "   - About page: /#/about\n"
    "   - Contact page: /#/contact\n"
    "For example, if someone asks how to donate, mention they can go to /#/donate."
)


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

    # Append the new user message
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        reply = response.choices[0].message.content
    except Exception as exc:
        logger.exception("OpenAI API call failed")
        return JsonResponse(
            {"error": f"AI service error: {exc}"},
            status=502,
        )

    return JsonResponse({"reply": reply})
