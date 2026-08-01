"""
SellerAI Backend — Flask API for Amazon Listing Generation & Scoring
Powered by DeepSeek with automatic SiliconFlow fallback.
"""

import os
import json
import time
import logging
import traceback
from datetime import datetime, timezone, timedelta
from functools import wraps
import hmac

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, g
from flask_cors import CORS
import requests

from scorer import score_listing  # MOAT #2: heuristic AI-search scorer

# ── App & CORS ──────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app, origins=list(ALLOWED_ORIGINS), methods=["GET", "POST", "OPTIONS"])

# ── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("sellerai")

# ── Config from env ─────────────────────────────────────────────────────────
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"

SILICONFLOW_API_KEY = os.environ.get("SILICONFLOW_API_KEY", "")
SILICONFLOW_URL = "https://api.siliconflow.cn/v1/chat/completions"
SILICONFLOW_MODEL = "deepseek-ai/DeepSeek-V3"

TIMEOUT_SECONDS = 15
MAX_RETRIES = 1                     # one retry on 5xx
RETRY_DELAY = 1.0                   # seconds
# ── Security: auth & rate limiting ─────────────────────────────────────
BACKEND_API_KEY = os.environ.get("BACKEND_API_KEY", "")

ALLOWED_ORIGINS_RAW = os.environ.get("ALLOWED_ORIGINS", "")
ALLOWED_ORIGINS = set(o.strip() for o in ALLOWED_ORIGINS_RAW.split(",") if o.strip()
) if ALLOWED_ORIGINS_RAW else set()

MAX_DESCRIPTION_LEN = int(os.environ.get("MAX_DESCRIPTION_LEN", "4000"))
RATE_LIMIT_WINDOW_MS = 10 * 60 * 1000
RATE_LIMIT_MAX = int(os.environ.get("RATE_LIMIT_MAX", "20"))

_rate_store = {}

def _prune_rate_store():
    if len(_rate_store) <= 10000:
        return
    now = time.time() * 1000
    expired = [k for k, v in _rate_store.items() if now > v["reset_at"]]
    for k in expired:
        del _rate_store[k]

def _check_rate_limit(ip):
    now = time.time() * 1000
    entry = _rate_store.get(ip)
    if not entry or now > entry["reset_at"]:
        _rate_store[ip] = {"count": 1, "reset_at": now + RATE_LIMIT_WINDOW_MS}
        _prune_rate_store()
        return True, 0
    if entry["count"] >= RATE_LIMIT_MAX:
        return False, int((entry["reset_at"] - now) // 1000) + 1
    entry["count"] += 1
    return True, 0

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not BACKEND_API_KEY:
            return jsonify({"error": "Server misconfigured: API key not set."}), 503
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return {"error": "Missing or invalid Authorization header."}, 401
        token = auth.replace("Bearer ", "").strip()
        if not hmac.compare_digest(token, BACKEND_API_KEY):
            return {"error": "Invalid API key."}, 403
        return f(*args, **kwargs)
    return decorated

def get_client_ip():
    fwd = request.headers.get("X-Forwarded-For", "")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.remote_addr or "unknown"


# ── Timezone helper ─────────────────────────────────────────────────────────
TZ = timezone(timedelta(hours=8))   # Asia/Shanghai


def now_iso() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


# ── MOAT #3: data-flywheel base ──────────────────────────────────────────
# Append one PII-free JSONL record per generation to data/flywheel.log. This
# lays the foundation for later "train on real outcomes" work. Contains only
# shape/length metadata + a non-reversible digest of the input — never raw text.
# Cost ~= 0 (local append). Failures never break a generation.
FLYWHEEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
FLYWHEEL_LOG = os.path.join(FLYWHEEL_DIR, "flywheel.log")


def _digest(s: str) -> str:
    """Fast non-cryptographic FNV-1a digest so records correlate without
    ever persisting the raw input. Not reversible."""
    h = 0x811C9DC5
    for ch in (s or ""):
        h ^= ord(ch) & 0xFF
        h = (h * 0x01000193) & 0xFFFFFFFF
    return format(h, "08x")


def log_flywheel(rec: dict) -> None:
    try:
        os.makedirs(FLYWHEEL_DIR, exist_ok=True)
        line = json.dumps({"ts": now_iso(), "event": "generate", **rec}, ensure_ascii=False)
        with open(FLYWHEEL_LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception as exc:  # never let telemetry break a request
        logger.warning("flywheel log failed: %s", exc)


# ── Request logging middleware ───────────────────────────────────────────────
@app.before_request
def log_request():
    g.start = time.perf_counter()
    logger.info("→ %s %s | ip=%s", request.method, request.path, get_client_ip())
    allowed, retry_after = _check_rate_limit(get_client_ip())
    if not allowed:
        return jsonify({"error": "Too many requests, please try again later."}), 429, {"Retry-After": str(retry_after)}


@app.after_request
def log_response(response):
    elapsed_ms = (time.perf_counter() - g.get("start", time.perf_counter())) * 1000
    logger.info(
        "← %s %s → %d  %.0fms",
        request.method,
        request.path,
        response.status_code,
        elapsed_ms,
    )
    return response


# ── System Prompts ──────────────────────────────────────────────────────────

# ── MOAT #1: multi-platform engine ──
# Listings are no longer Amazon-only. `platform` selects the field
# constraints + AI-search engine; `target_site` selects the locale/language.
# Keep PLATFORMS in sync with sellerai-frontend/lib/platforms.ts and route.ts.
PLATFORMS = {
    "amazon": {
        "label": "Amazon",
        "engine": "Amazon Rufus / A9",
        "title_max_len": 200,
        "guidance": (
            "Title up to 200 chars leading with the primary keyword; exactly 5 "
            "benefit-first bullet points (CAPS benefit then explanation); backend "
            "search terms; optimize for the A9 algorithm and Rufus semantic retrieval."
        ),
    },
    "ebay": {
        "label": "eBay",
        "engine": "eBay Cassini",
        "title_max_len": 80,
        "guidance": (
            "Title MUST be <= 80 chars, keyword-dense with brand + model + key aspects "
            "(no 5-bullet block — eBay has none). Fill 'bullets' as concise item-specific "
            "highlights. Optimize for the Cassini engine: relevance, item specifics/aspects, "
            "sell-through signals."
        ),
    },
    "walmart": {
        "label": "Walmart",
        "engine": "Walmart Search",
        "title_max_len": 100,
        "guidance": (
            "Title 50-75 chars ideal (<=100): Brand + Product + defining attributes. "
            "Provide rich 'key features' as bullets and complete attributes. Optimize "
            "for Walmart search relevance and content quality score."
        ),
    },
    "shopify": {
        "label": "Shopify",
        "engine": "Google / SEO",
        "title_max_len": 70,
        "guidance": (
            "SEO-first: product title <=60-70 chars, a meta-description-friendly summary, "
            "structured benefit bullets, and a brand-voice description. Optimize for "
            "Google organic search and on-store SEO."
        ),
    },
    "tiktok": {
        "label": "TikTok Shop",
        "engine": "TikTok Relevance",
        "title_max_len": 60,
        "guidance": (
            "Short punchy hook title <=60 chars with a scroll-stopping benefit; include "
            "trend/hashtag-style keywords; bullets should be snappy social selling points. "
            "Optimize for TikTok's relevance/discovery feed and impulse conversion."
        ),
    },
    "etsy": {
        "label": "Etsy",
        "engine": "Etsy Search",
        "title_max_len": 140,
        "guidance": (
            "Long-tail descriptive title <=140 chars front-loading buyer search phrases "
            "(occasion/recipient/style/material). No 5-bullet block — use 'bullets' as key "
            "highlights and provide up to 13 tags in 'keywords'. Include a handmade/story "
            "angle. Optimize for Etsy search."
        ),
    },
}
DEFAULT_PLATFORM = "amazon"


def normalize_platform(code):
    return code if isinstance(code, str) and code in PLATFORMS else DEFAULT_PLATFORM


# ── Phase 0 i18n: source-language + target-site (locale) dual routing ──
# The old LISTING_SYSTEM_PROMPT assumed Chinese input -> English US output.
# Now both variables are dynamic. Defaults keep backward compat.
SUPPORTED_SITES = {
    "en-US": "Amazon.com (United States) — write all copy in native American English",
    "en-GB": "Amazon.co.uk (United Kingdom) — write all copy in native British English",
    "de-DE": "Amazon.de (Germany) — write all copy in native German",
    "fr-FR": "Amazon.fr (France) — write all copy in native French",
    "es-ES": "Amazon.es (Spain) — write all copy in native Spanish",
    "es-MX": "Amazon.com.mx (Mexico) — write all copy in native Spanish",
    "it-IT": "Amazon.it (Italy) — write all copy in native Italian",
    "ja-JP": "Amazon.co.jp (Japan) — write all copy in native Japanese",
    "nl-NL": "Amazon.nl (Netherlands) — write all copy in native Dutch",
    "pt-BR": "Amazon.com.br (Brazil) — write all copy in native Portuguese",
    "ca-EN": "Amazon.ca (Canada) — write all copy in native English",
    "in-EN": "Amazon.in (India) — write all copy in native English",
    "au-EN": "Amazon.com.au (Australia) — write all copy in native English",
    "ae-EN": "Amazon.ae (UAE) — write all copy in native English",
}
DEFAULT_SITE = "en-US"
# Default source language is now "any language" — the tool accepts input in
# any language and detects it automatically (global-seller repositioning).
DEFAULT_SOURCE_LANG = "any language"


def normalize_site(code):
    return code if isinstance(code, str) and code in SUPPORTED_SITES else DEFAULT_SITE


def build_listing_prompt(platform, source_lang, target_site, rufus_mode=False):
    """Build the listing system prompt from a platform + source language + target
    marketplace locale. rufus_mode appends the platform AI-search guidance — a
    differentiation point free official tools don't offer."""
    plat = PLATFORMS.get(platform, PLATFORMS[DEFAULT_PLATFORM])
    site_desc = SUPPORTED_SITES.get(target_site, SUPPORTED_SITES[DEFAULT_SITE])
    src_raw = (source_lang or "").strip()
    # "auto" or empty => let the model auto-detect the input language.
    src = src_raw if src_raw and src_raw.lower() != "auto" else DEFAULT_SOURCE_LANG
    rufus_block = ""
    rufus_key = ""
    if rufus_mode:
        rufus_key = '\n- "rufus_faq": array of 5 shopper questions + answers (only when AI-search mode is on)'
        rufus_block = (
            "\n\nAI-SEARCH OPTIMIZATION (" + plat["engine"] + " — the platform's AI shopping/discovery layer):\n"
            "- Anticipate the natural-language questions shoppers ask Rufus "
            "(e.g. \"Is this good for...?\", \"What's the difference between...?\") "
            "and answer them inside the copy.\n"
            "- Use clear entities, specific use-cases, and semantic keyword variations "
            "so Rufus can confidently retrieve and cite this listing.\n"
            "- Keep bullet points scannable and fact-dense so AI summarizers parse them cleanly."
        )
    return (
        f"You are an expert {plat['label']} listing copywriter. The seller will give you a "
        f"product description written in {src}. Generate a complete, "
        f"publication-ready {plat['label']} listing for {site_desc}.\n\n"
        f"PLATFORM RULES ({plat['label']} — engine: {plat['engine']}):\n{plat['guidance']}\n\n"
        "Return ONLY valid JSON (no markdown fences, no extra text) with these exact keys:\n"
        f'- "title": at most {plat["title_max_len"]} characters, lead with the main keyword, in the target marketplace\'s language\n'
        '- "bullets": array of 5 bullet points (each under 500 chars), start with a CAPS BENEFIT then explain, in the target language\n'
        '- "description": full HTML product description, 500-1000 words, use <p><b><ul><li> tags, in the target language\n'
        '- "keywords": array of localized search terms/tags (localized for the target marketplace)\n'
        f'- "category_hints": best {plat["label"]} category path for the target marketplace'
        f"{rufus_key}\n"
        "Rules:\n"
        f"- Write in the NATIVE language of the target marketplace ({site_desc}).\n"
        f"- Preserve the product's real specs, materials, and use-cases from the source description ({src}).\n"
        "- Focus on BENEFITS, not just features.\n"
        "- Include emotional triggers and localize idioms for the target market.\n"
        f"- Optimize for the {plat['engine']} search algorithm of that marketplace."
        f"{rufus_block}\n\n"
        "Return ONLY valid JSON."
    )

SCORING_SYSTEM_PROMPT = """You are an expert Amazon listing analyst. Score the provided Amazon listing on 8 dimensions. Each dimension scores 1-100. Return ONLY a JSON object (no markdown, no extra text) with these exact keys:

{
  "overall_score": <weighted-average-integer>,
  "dimensions": {
    "title_optimization":     {"score": <int>, "comment": "<brief Chinese diagnostic>"},
    "bullet_points_quality":  {"score": <int>, "comment": "<brief Chinese diagnostic>"},
    "description_richness":   {"score": <int>, "comment": "<brief Chinese diagnostic>"},
    "keyword_coverage":       {"score": <int>, "comment": "<brief Chinese diagnostic>"},
    "a9_visibility":          {"score": <int>, "comment": "<brief Chinese diagnostic>"},
    "conversion_potential":   {"score": <int>, "comment": "<brief Chinese diagnostic>"},
    "competitiveness":        {"score": <int>, "comment": "<brief Chinese diagnostic>"},
    "emotional_appeal":       {"score": <int>, "comment": "<brief Chinese diagnostic>"}
  }
}

Rules:
- Title optimization: keyword placement, length, readability, brand inclusion
- Bullet points quality: benefit-driven, scannable, CAPS leads, length
- Description richness: HTML usage, storytelling, keyword density, length
- Keyword coverage: backend terms, LSI keywords, search volume alignment
- A9 visibility: overall Amazon search algorithm friendliness
- Conversion potential: how likely a shopper is to buy after reading
- Competitiveness: how this listing stacks up against top competitors in category
- Emotional appeal: use of emotional triggers, pain-point resonance

Always respond in Chinese for the "comment" field inside each dimension."""


# ── LLM Call (with fallback) ────────────────────────────────────────────────

def _call_api(url: str, headers: dict, payload: dict, timeout: int) -> requests.Response:
    """Low-level HTTP POST to an OpenAI-compatible chat endpoint."""
    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    return resp


def _extract_json(resp: requests.Response) -> dict:
    """Extract JSON from a chat completion response. Strips markdown fences if any."""
    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    content = content.strip()
    # Strip ```json ... ``` fences
    if content.startswith("```"):
        content = content.split("\n", 1)[-1]
        if content.endswith("```"):
            content = content[:-3]
    content = content.strip()
    return json.loads(content)


def _get_key(name: str) -> str:
    """Get API key: runtime env var first, then .env, then module-level fallback."""
    return os.environ.get(name) or ""


def call_llm(system_prompt: str, user_message: str, temperature: float = 0.7) -> dict:
    """
    Call DeepSeek API → fallback to SiliconFlow on failure.
    Returns the parsed JSON response.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    ds_key = _get_key("DEEPSEEK_API_KEY")
    sf_key = _get_key("SILICONFLOW_API_KEY")

    # ── Primary: DeepSeek ───────────────────────────────────────────────
    if ds_key:
        primary_url = f"{DEEPSEEK_BASE_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {ds_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": DEEPSEEK_MODEL,
            "messages": messages,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
        }

        for attempt in range(MAX_RETRIES + 1):
            try:
                logger.info("DeepSeek attempt %d/%d", attempt + 1, MAX_RETRIES + 1)
                resp = _call_api(primary_url, headers, payload, TIMEOUT_SECONDS)
                if resp.status_code < 500:
                    return _extract_json(resp)
                logger.warning("DeepSeek returned %d, attempt %d", resp.status_code, attempt + 1)
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
            except Exception as exc:
                logger.warning("DeepSeek error (attempt %d): %s", attempt + 1, exc)
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                else:
                    logger.warning("DeepSeek exhausted, falling back to SiliconFlow")
                    break

    # ── Fallback: SiliconFlow ───────────────────────────────────────────
    if sf_key:
        headers = {
            "Authorization": f"Bearer {sf_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": SILICONFLOW_MODEL,
            "messages": messages,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
        }

        for attempt in range(MAX_RETRIES + 1):
            try:
                logger.info("SiliconFlow attempt %d/%d", attempt + 1, MAX_RETRIES + 1)
                resp = _call_api(SILICONFLOW_URL, headers, payload, TIMEOUT_SECONDS)
                if resp.status_code < 500:
                    return _extract_json(resp)
                logger.warning("SiliconFlow returned %d, attempt %d", resp.status_code, attempt + 1)
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
            except Exception as exc:
                logger.warning("SiliconFlow error (attempt %d): %s", attempt + 1, exc)
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)

    # ── No API key at all ───────────────────────────────────────────────
    if not ds_key and not sf_key:
        raise RuntimeError("Neither DEEPSEEK_API_KEY nor SILICONFLOW_API_KEY is configured.")

    raise RuntimeError("All LLM providers failed after retries.")


# ── Routes ──────────────────────────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "timestamp": now_iso(),
        "version": "1.0.0",
        "providers": {
            "deepseek": bool(DEEPSEEK_API_KEY),
            "siliconflow": bool(SILICONFLOW_API_KEY),
        },
    })


@app.route("/api/generate-listing", methods=["POST"])
@require_api_key
def generate_listing():
    """
    Generate an Amazon listing from a Chinese product description.

    Request JSON:
        {"description": "<Chinese product description>"}

    Response JSON:
        The structured listing with title, bullets, description, keywords, category_hints.
    """
    body = request.get_json(silent=True)
    if not body or "description" not in body:
        return jsonify({"error": "Missing 'description' in request body."}), 400

    desc = body["description"].strip()
    if not desc:
        return jsonify({"error": "'description' cannot be empty."}), 400

    temperature = float(body.get("temperature", 0.7))

    # MOAT #1 + Phase 0 i18n: read platform/source/target (defaults keep old behavior).
    platform = normalize_platform(body.get("platform"))
    source_lang = body.get("sourceLang") or DEFAULT_SOURCE_LANG
    target_site = normalize_site(body.get("targetSite"))
    rufus_mode = bool(body.get("rufusOptimize", False))
    system_prompt = build_listing_prompt(platform, source_lang, target_site, rufus_mode)

    logger.info(
        "Generate listing — input length: %d chars, platform=%s, src=%s, site=%s, rufus=%s",
        len(desc), platform, source_lang, target_site, rufus_mode,
    )

    try:
        result = call_llm(system_prompt, desc, temperature=temperature)
        # MOAT #3 — data flywheel: PII-free telemetry to data/flywheel.log.
        log_flywheel({
            "platform": platform,
            "sourceLang": source_lang,
            "targetSite": target_site,
            "rufusOptimize": rufus_mode,
            "inputChars": len(desc),
            "inputDigest": _digest(desc),
            "outTitleLen": len(result.get("title", "")) if isinstance(result, dict) else 0,
            "outBullets": len(result.get("bullets", []) or []) if isinstance(result, dict) else 0,
            "outKeywords": len(result.get("keywords", []) or []) if isinstance(result, dict) else 0,
            "outHasFaq": bool(isinstance(result, dict) and result.get("rufus_faq")),
        })
        return jsonify(result)
    except json.JSONDecodeError as exc:
        logger.error("JSON parse failed: %s", exc)
        return jsonify({"error": "LLM returned invalid JSON.", "detail": str(exc)}), 502
    except RuntimeError as exc:
        logger.error("LLM call failed: %s", exc)
        return jsonify({"error": str(exc)}), 502
    except Exception as exc:
        logger.error("Unexpected error: %s\n%s", exc, traceback.format_exc())
        return jsonify({"error": "Internal server error."}), 500


@app.route("/api/ai-search-score", methods=["POST"])
@require_api_key
def ai_search_score():
    """MOAT #2 — Platform AI-search friendliness score for a generated listing.

    Pure heuristic (no LLM call, no key, 0 cost). Request JSON:
        {"platform": "amazon", "title": "...", "bullets": [...],
         "description": "...", "keywords": [...], "rufus_faq": [...]}
    """
    body = request.get_json(silent=True) or {}
    if not body.get("title") and not body.get("bullets") and not body.get("description"):
        return jsonify({"error": "Provide at least a title, bullets, or description."}), 400
    try:
        return jsonify(score_listing(body))
    except Exception as exc:
        logger.error("ai-search-score failed: %s\n%s", exc, traceback.format_exc())
        return jsonify({"error": "Scoring failed."}), 500


@app.route("/api/listing-score", methods=["POST"])
@require_api_key
def listing_score():
    """
    Score an existing Amazon listing across 8 quality dimensions.

    Request JSON:
        {"listing": "<full listing text>"}

    Response JSON:
        {"overall_score": int, "dimensions": {...}}
    """
    body = request.get_json(silent=True)
    if not body or "listing" not in body:
        return jsonify({"error": "Missing 'listing' in request body."}), 400

    listing_text = body["listing"].strip()
    if not listing_text:
        return jsonify({"error": "'listing' cannot be empty."}), 400

    temperature = float(body.get("temperature", 0.3))

    logger.info("Score listing — input length: %d chars", len(listing_text))

    try:
        result = call_llm(SCORING_SYSTEM_PROMPT, listing_text, temperature=temperature)
        return jsonify(result)
    except json.JSONDecodeError as exc:
        logger.error("JSON parse failed: %s", exc)
        return jsonify({"error": "LLM returned invalid JSON.", "detail": str(exc)}), 502
    except RuntimeError as exc:
        logger.error("LLM call failed: %s", exc)
        return jsonify({"error": str(exc)}), 502
    except Exception as exc:
        logger.error("Unexpected error: %s\n%s", exc, traceback.format_exc())
        return jsonify({"error": "Internal server error."}), 500


# ── Error handlers ──────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(_e):
    return jsonify({"error": "Not found."}), 404


@app.errorhandler(405)
def method_not_allowed(_e):
    return jsonify({"error": "Method not allowed."}), 405


@app.errorhandler(500)
def server_error(_e):
    return jsonify({"error": "Internal server error."}), 500


# ── Main ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    FLASK_DEBUG = False  # Production — never enable debug mode / Werkzeug debugger
    logger.info("Starting SellerAI backend on port %d (debug=False)", port)
    app.run(host="127.0.0.1", port=port, debug=False)
