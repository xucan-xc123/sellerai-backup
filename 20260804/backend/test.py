"""
SellerAI Backend — Integration Test

Starts Flask in a background thread, then sends test requests.
Requires: DEEPSEEK_API_KEY (and optionally SILICONFLOW_API_KEY) in environment.
"""

import os
import sys
import time
import json
import threading

import requests

# Ensure we can import app from the same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app

BASE_URL = "http://127.0.0.1:8000"


def start_server():
    """Run Flask in a daemon thread."""
    t = threading.Thread(target=lambda: app.run(host="127.0.0.1", port=8000, debug=False), daemon=True)
    t.start()
    # Give it a moment to boot
    time.sleep(2)


def test_health():
    print("\n── Testing GET /api/health ──")
    resp = requests.get(f"{BASE_URL}/api/health")
    assert resp.status_code == 200, f"Health failed: {resp.status_code}"
    data = resp.json()
    assert data["status"] == "ok"
    print(f"  ✓ status={data['status']}")
    print(f"  ✓ providers: {json.dumps(data['providers'], indent=2)}")


def test_generate_listing():
    if not os.environ.get("DEEPSEEK_API_KEY") and not os.environ.get("SILICONFLOW_API_KEY"):
        print("\n── SKIP POST /api/generate-listing (no API key configured) ──")
        return

    print("\n── Testing POST /api/generate-listing ──")
    payload = {
        "description": (
            "一款便携式蓝牙音箱，支持防水防尘IPX7等级，内置3600mAh电池续航12小时，"
            "支持TWS串联立体声，重量仅350g，适合户外露营和家庭使用。"
        ),
        "temperature": 0.7,
    }
    resp = requests.post(f"{BASE_URL}/api/generate-listing", json=payload, timeout=60)
    assert resp.status_code == 200, f"Generate failed: {resp.status_code} body={resp.text[:500]}"
    data = resp.json()
    required_keys = {"title", "bullets", "description", "keywords", "category_hints"}
    missing = required_keys - set(data.keys())
    assert not missing, f"Missing keys: {missing}"
    assert len(data["bullets"]) == 5, f"Expected 5 bullets, got {len(data['bullets'])}"
    assert len(data["keywords"]) >= 10, f"Expected >=10 keywords, got {len(data['keywords'])}"
    assert len(data["title"]) <= 200, f"Title too long: {len(data['title'])} chars"
    print(f"  ✓ title: {data['title'][:80]}...")
    print(f"  ✓ bullets: {len(data['bullets'])} items")
    print(f"  ✓ keywords: {len(data['keywords'])} terms")
    print(f"  ✓ category_hints: {data['category_hints']}")


def test_listing_score():
    if not os.environ.get("DEEPSEEK_API_KEY") and not os.environ.get("SILICONFLOW_API_KEY"):
        print("\n── SKIP POST /api/listing-score (no API key configured) ──")
        return

    print("\n── Testing POST /api/listing-score ──")
    payload = {
        "listing": (
            "Portable Bluetooth Speaker - Wireless, Waterproof, 12H Battery\n\n"
            "CRYSTAL CLEAR SOUND: Experience 360° immersive audio with dual drivers.\n"
            "WATERPROOF DESIGN: IPX7 rated, take it to the pool or beach worry-free.\n"
            "MASSIVE BATTERY LIFE: 12 hours of playtime keeps the music going all day.\n"
            "ULTRA PORTABLE: Weighs only 350g with included carabiner clip.\n"
            "TWS PAIRING: Connect two speakers for true stereo sound.\n\n"
            "<p>This portable Bluetooth speaker delivers room-filling sound...</p>"
        ),
        "temperature": 0.3,
    }
    resp = requests.post(f"{BASE_URL}/api/listing-score", json=payload, timeout=60)
    assert resp.status_code == 200, f"Score failed: {resp.status_code} body={resp.text[:500]}"
    data = resp.json()
    assert "overall_score" in data, "Missing overall_score"
    assert "dimensions" in data, "Missing dimensions"
    assert len(data["dimensions"]) == 8, f"Expected 8 dimensions, got {len(data['dimensions'])}"
    print(f"  ✓ overall_score: {data['overall_score']}")
    for dim, info in data["dimensions"].items():
        print(f"    {dim}: score={info['score']} comment={info['comment']}")


def test_validation():
    print("\n── Testing input validation ──")

    # Missing field
    resp = requests.post(f"{BASE_URL}/api/generate-listing", json={})
    assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
    print(f"  ✓ missing description → 400: {resp.json()['error']}")

    # Empty field
    resp = requests.post(f"{BASE_URL}/api/generate-listing", json={"description": ""})
    assert resp.status_code == 400
    print(f"  ✓ empty description → 400: {resp.json()['error']}")

    # 404
    resp = requests.get(f"{BASE_URL}/api/nope")
    assert resp.status_code == 404
    print(f"  ✓ unknown route → 404")


def test_fallback_config():
    print("\n── Checking API key configuration ──")
    ds = bool(os.environ.get("DEEPSEEK_API_KEY"))
    sf = bool(os.environ.get("SILICONFLOW_API_KEY"))
    print(f"  DEEPSEEK_API_KEY: {'✓ set' if ds else '✗ missing'}")
    print(f"  SILICONFLOW_API_KEY: {'✓ set' if sf else '✗ missing'}")
    if not ds and not sf:
        print("  ⚠  No API keys configured — LLM tests will be skipped.")
    elif ds:
        print("  ℹ  Primary provider: DeepSeek")
        if sf:
            print("  ℹ  Fallback provider: SiliconFlow (auto)")
        else:
            print("  ⚠  No fallback configured — set SILICONFLOW_API_KEY for redundancy.")


def main():
    print("=" * 60)
    print("  SellerAI Backend — Integration Tests")
    print("=" * 60)

    # Load .env manually if present (simple key=value parser)
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.isfile(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    os.environ[key.strip()] = val.strip().strip('"').strip("'")

    start_server()

    try:
        test_health()
        test_validation()
        test_fallback_config()
        test_generate_listing()
        test_listing_score()

        print("\n" + "=" * 60)
        print("  ✓ All tests completed!")
        print("=" * 60)
    except AssertionError as exc:
        print(f"\n  ✗ TEST FAILED: {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"\n  ✗ ERROR: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
