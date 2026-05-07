"""Simple command-line translator using LibreTranslate public API.

Usage:
    python translator.py "你好，世界" --source zh --target en
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

API_URL = "https://libretranslate.com/translate"


def translate(text: str, source: str = "auto", target: str = "en") -> str:
    """Translate text using LibreTranslate."""
    payload = urllib.parse.urlencode(
        {
            "q": text,
            "source": source,
            "target": target,
            "format": "text",
        }
    ).encode("utf-8")

    req = urllib.request.Request(API_URL, data=payload, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urllib.request.urlopen(req, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))

    if "translatedText" not in data:
        raise ValueError(f"Unexpected API response: {data}")

    return data["translatedText"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Translate text between languages.")
    parser.add_argument("text", help="Text to translate")
    parser.add_argument("--source", default="auto", help="Source language code (default: auto)")
    parser.add_argument("--target", default="en", help="Target language code (default: en)")
    args = parser.parse_args()

    try:
        result = translate(args.text, source=args.source, target=args.target)
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"Network error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
