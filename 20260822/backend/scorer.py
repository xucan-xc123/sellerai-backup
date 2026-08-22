"""
SellerAI — Platform AI-Search Friendliness Scorer (MOAT #2), backend twin.

Mirrors sellerai-frontend/lib/scoreListing.ts. Pure, rule-based heuristic —
no external model calls, no keys, offline-safe, 0 cost. Scores a generated
listing for how well it will perform in each platform's AI / semantic search
layer (Amazon Rufus/A9, eBay Cassini, Walmart, Shopify/Google, TikTok, Etsy).

The data flywheel (data/flywheel.log) will later let us calibrate these weights
against real ranking / CTR outcomes.
"""

import re

# Platform field constraints + AI-search engine. Keep in sync with
# sellerai-frontend/lib/platforms.ts and app.py PLATFORMS.
PLATFORM_CONSTRAINTS = {
    "amazon":  {"label": "Amazon",       "engine": "Amazon Rufus / A9",   "title_max_len": 200, "title_ideal_min": 120, "uses_bullets": True,  "keyword_ideal": 12},
    "ebay":    {"label": "eBay",         "engine": "eBay Cassini",        "title_max_len": 80,  "title_ideal_min": 60,  "uses_bullets": False, "keyword_ideal": 10},
    "walmart": {"label": "Walmart",      "engine": "Walmart Search",      "title_max_len": 100, "title_ideal_min": 50,  "uses_bullets": True,  "keyword_ideal": 10},
    "shopify": {"label": "Shopify",      "engine": "Google / SEO",        "title_max_len": 70,  "title_ideal_min": 40,  "uses_bullets": True,  "keyword_ideal": 8},
    "tiktok":  {"label": "TikTok Shop",  "engine": "TikTok Relevance",    "title_max_len": 60,  "title_ideal_min": 25,  "uses_bullets": True,  "keyword_ideal": 8},
    "etsy":    {"label": "Etsy",         "engine": "Etsy Search",         "title_max_len": 140, "title_ideal_min": 70,  "uses_bullets": False, "keyword_ideal": 13},
}
DEFAULT_PLATFORM = "amazon"

QUESTION_CUES = ["how", "what", "which", "is it", "does", "can", "will", "why",
                 "best for", "good for", "difference", "compatible", "suitable"]
USECASE_CUES = ["for", "ideal for", "perfect for", "use", "designed", "great for",
                "works with", "suitable", "whether", "if you"]


def _status(score, mx):
    if mx <= 0:
        return "good"
    r = score / mx
    return "good" if r >= 0.8 else "warning" if r >= 0.5 else "bad"


def _grade(score):
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    if score >= 40: return "D"
    return "F"


def _strip_html(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


def score_listing(inp: dict) -> dict:
    """inp keys: platform, title, bullets[], description, keywords[],
    rufus_faq[], primary_keyword (optional)."""
    plat = PLATFORM_CONSTRAINTS.get(inp.get("platform"), PLATFORM_CONSTRAINTS[DEFAULT_PLATFORM])

    title = (inp.get("title") or "").strip()
    title_len = len(title)
    title_lower = title.lower()
    bullets = [b.strip() for b in (inp.get("bullets") or []) if b and b.strip()]
    desc_text = _strip_html(inp.get("description") or "")
    keywords = [k.lower().strip() for k in (inp.get("keywords") or []) if k and k.strip()]
    primary = (inp.get("primary_keyword") or (keywords[0] if keywords else "")).lower().strip()
    faq_len = len(inp.get("rufus_faq") or []) if isinstance(inp.get("rufus_faq"), list) else 0

    blob = " ".join([title_lower, " ".join(bullets).lower(), desc_text.lower()])
    factors = []

    # Factor 1: Title length fit (max 18)
    if title_len == 0:
        ts, td = 0, "Title is empty."
    elif title_len > plat["title_max_len"]:
        ts, td = 6, "Title is %d chars — over %s's ~%d limit; may be truncated in AI results. Trim it." % (title_len, plat["label"], plat["title_max_len"])
    elif title_len >= plat["title_ideal_min"]:
        ts, td = 18, "Title length (%d) sits in %s's sweet spot (%d-%d)." % (title_len, plat["label"], plat["title_ideal_min"], plat["title_max_len"])
    else:
        ts, td = 11, "Title (%d chars) is shorter than the ideal %d+ for %s. Add qualified keywords/attributes." % (title_len, plat["title_ideal_min"], plat["label"])
    factors.append({"key": "title_fit", "label": "Title length fit", "score": ts, "max": 18, "status": _status(ts, 18), "detail": td})

    # Factor 2: Primary keyword placement (max 16)
    if not primary:
        ks, kd = 8, "No primary keyword detected — provide one or ensure keywords are populated."
    else:
        idx = title_lower.find(primary)
        if idx == 0:
            ks, kd = 16, 'Primary keyword "%s" leads the title — optimal for %s.' % (primary, plat["engine"])
        elif 0 < idx <= 40:
            ks, kd = 12, "Primary keyword appears early (char %d). Move it to the front for max weight." % idx
        elif idx > 40:
            ks, kd = 7, "Primary keyword is buried at char %d. AI engines weight leading terms — move it forward." % idx
        else:
            ks, kd = 2, 'Primary keyword "%s" is missing from the title. Add it, ideally at the start.' % primary
    factors.append({"key": "keyword_placement", "label": "Primary keyword placement", "score": ks, "max": 16, "status": _status(ks, 16), "detail": kd})

    # Factor 3: Keyword coverage (max 14)
    kw_count = len(keywords)
    covered = sum(1 for k in keywords if k in blob)
    cover_ratio = (covered / kw_count) if kw_count else 0
    count_part = 7 if kw_count >= plat["keyword_ideal"] else 4 if kw_count >= (plat["keyword_ideal"] + 1) // 2 else 2 if kw_count > 0 else 0
    spread_part = 7 if cover_ratio >= 0.6 else 4 if cover_ratio >= 0.3 else 2 if cover_ratio > 0 else 0
    cov = count_part + spread_part
    factors.append({"key": "keyword_coverage", "label": "Keyword coverage", "score": cov, "max": 14, "status": _status(cov, 14),
                    "detail": "%d/%d target keywords, %d woven into copy (%d%%). %s" % (
                        kw_count, plat["keyword_ideal"], covered, round(cover_ratio * 100),
                        ("Add %d more localized keywords." % (plat["keyword_ideal"] - kw_count)) if kw_count < plat["keyword_ideal"] else "Good keyword volume.")})

    # Factor 4: Semantic / natural-language richness (max 16)
    uc = sum(1 for c in USECASE_CUES if c in blob)
    qc = sum(1 for c in QUESTION_CUES if c in blob)
    uc_part = 8 if uc >= 4 else 5 if uc >= 2 else 2 if uc >= 1 else 0
    qc_part = 8 if qc >= 3 else 4 if qc >= 1 else 0
    sem = uc_part + qc_part
    factors.append({"key": "semantic_richness", "label": "Semantic / natural-language richness", "score": sem, "max": 16, "status": _status(sem, 16),
                    "detail": "%d use-case cues + %d question-style cues found. %s" % (
                        uc, qc, "Strong natural-language surface for AI retrieval." if sem >= 12
                        else 'Add "who/when/why it\'s for" phrasing and buyer questions so %s can match conversational queries.' % plat["engine"])})

    # Factor 5: Structure fit (max 14)
    if plat["uses_bullets"]:
        b_count = len(bullets)
        bullet_part = 8 if b_count >= 5 else 5 if b_count >= 3 else 2 if b_count >= 1 else 0
        desc_part = 6 if len(desc_text) >= 500 else 4 if len(desc_text) >= 200 else 2 if desc_text else 0
        sts = bullet_part + desc_part
        std = "%d bullets + %d-char description. %s%s" % (
            b_count, len(desc_text), ("Fill all 5 bullets. " if b_count < 5 else ""),
            ("Expand description to 500+ chars." if len(desc_text) < 500 else "Solid structure."))
    else:
        sts = 14 if len(desc_text) >= 800 else 10 if len(desc_text) >= 400 else 6 if len(desc_text) >= 150 else 3 if desc_text else 0
        std = "%s doesn't use 5-bullet blocks — description is %d chars. %s" % (
            plat["label"], len(desc_text),
            "Aim for 800+ chars of specifics + item aspects/tags." if len(desc_text) < 800 else "Rich description — good.")
    factors.append({"key": "structure_fit", "label": "Structure fit", "score": sts, "max": 14, "status": _status(sts, 14), "detail": std})

    # Factor 6: AI answerability (max 12)
    if faq_len >= 4:
        fs, fd = 12, "%d Q&A pairs — excellent answer surface for %s." % (faq_len, "Rufus" if plat["label"] == "Amazon" else "AI search")
    elif faq_len >= 1:
        fs, fd = 7, "%d Q&A pairs. Add more shopper questions (aim for 5) to boost AI-citation odds." % faq_len
    elif qc >= 2:
        fs, fd = 5, "No explicit FAQ, but copy answers some implicit questions. Add a dedicated Q&A block."
    else:
        fs, fd = 0, "No AI-answerable Q&A content. Enable AI-search mode to generate shopper Q&A — this is where %s pulls answers from." % plat["engine"]
    factors.append({"key": "ai_answerability", "label": "AI answerability (Q&A surface)", "score": fs, "max": 12, "status": _status(fs, 12), "detail": fd})

    # Factor 7: Readability / anti-stuffing (max 10)
    rs, rd = 10, "Clean, readable copy — no stuffing detected."
    if re.search(r"[A-Z]{6,}", title):
        rs -= 3; rd = "Long ALL-CAPS runs in title hurt AI parsing — use title case."
    if re.search(r"(.)\1{3,}", title):
        rs -= 3; rd = "Character stuffing detected in title — remove it."
    if any(len(k) >= 3 and blob.count(k) > 5 for k in keywords):
        rs -= 4; rd = "A keyword is over-repeated (stuffing). AI search penalizes this — vary phrasing."
    rs = max(0, rs)
    factors.append({"key": "readability", "label": "Readability / anti-stuffing", "score": rs, "max": 10, "status": _status(rs, 10), "detail": rd})

    earned = sum(f["score"] for f in factors)
    possible = sum(f["max"] for f in factors)
    ai_score = round((earned / possible) * 100)
    grade = _grade(ai_score)

    suggestions = [f["detail"] for f in sorted(
        [f for f in factors if f["status"] != "good"],
        key=lambda f: f["score"] / f["max"])][:4]
    if not suggestions:
        suggestions = ["Listing is well-tuned for %s. Ship it and let the data flywheel refine further." % plat["engine"]]

    if ai_score >= 80:
        headline = "Strong AI-search fit for %s (%s)." % (plat["label"], plat["engine"])
    elif ai_score >= 60:
        headline = "Decent AI-search fit for %s, but %d quick wins remain." % (plat["label"], len(suggestions))
    else:
        headline = "Weak AI-search fit for %s — fix the flagged factors to get discovered by %s." % (plat["label"], plat["engine"])

    return {
        "platform": inp.get("platform", DEFAULT_PLATFORM) if inp.get("platform") in PLATFORM_CONSTRAINTS else DEFAULT_PLATFORM,
        "platform_label": plat["label"],
        "engine": plat["engine"],
        "ai_search_score": ai_score,
        "grade": grade,
        "headline": headline,
        "factors": factors,
        "suggestions": suggestions,
    }
