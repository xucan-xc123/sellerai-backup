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

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, g
from flask_cors import CORS
import requests

# ── App & CORS ──────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)

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

# ── Timezone helper ─────────────────────────────────────────────────────────
TZ = timezone(timedelta(hours=8))   # Asia/Shanghai


def now_iso() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


# ── Request logging middleware ───────────────────────────────────────────────
@app.before_request
def log_request():
    g.start = time.perf_counter()
    logger.info("→ %s %s | ip=%s", request.method, request.path, request.remote_addr)


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

LISTING_SYSTEM_PROMPT = """You are an expert Amazon listing copywriter. Given a Chinese product description, generate a complete Amazon listing in JSON format with these exact keys:
- "title": under 200 characters, include main keyword at front
- "bullets": array of 5 bullet points, each under 500 characters, start with CAPS BENEFIT then explain
- "description": full HTML product description, 500-1000 words, use <p><b><ul><li> tags
- "keywords": array of 10-15 backend search terms, comma separated
- "category_hints": best Amazon category path

Rules:
- Write in native American English
- Focus on BENEFITS not features
- Include emotional triggers
- Optimize for Amazon A9 algorithm

Return ONLY valid JSON, no markdown fences, no extra text."""

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

    logger.info("Generate listing — input length: %d chars", len(desc))

    try:
        result = call_llm(LISTING_SYSTEM_PROMPT, desc, temperature=temperature)
        return jsonify(result)
    except json.JSONDecodeError as exc:
        logger.error("JSON parse failed: %s", exc)
        return jsonify({"error": "LLM returned invalid JSON.", "detail": str(exc)}), 502
    except RuntimeError as exc:
        logger.error("LLM call failed: %s", exc)
        return jsonify({"error": str(exc)}), 502
    except Exception as exc:
        logger.error("Unexpected error: %s\n%s", exc, traceback.format_exc())
        return jsonify({"error": "Internal server error.", "detail": str(exc)}), 500


@app.route("/api/listing-score", methods=["POST"])
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
        return jsonify({"error": "Internal server error.", "detail": str(exc)}), 500


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
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    logger.info("Starting SellerAI backend on port %d (debug=%s)", port, debug)
    app.run(host="0.0.0.0", port=port, debug=debug)
