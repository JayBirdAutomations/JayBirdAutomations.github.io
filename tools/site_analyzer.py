"""
Jaybird Automations — Website Quality Analyzer
Analyzes a business's website to identify AI service opportunities.

This tool is a SALES WEAPON: "I analyzed your website and found these improvements..."

USAGE:
  python site_analyzer.py --url https://example.com
  python site_analyzer.py --file ../output/leads_las_vegas_nv_20260408.xlsx
  python site_analyzer.py --url https://example.com --verbose

OUTPUT:
  Prints a score card and saves detailed report to output/
"""

import os
import sys
import re
import time
import argparse
import requests
from bs4 import BeautifulSoup
from datetime import datetime

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


# Known chatbot/live chat script signatures
CHATBOT_SIGNATURES = [
    "tidio", "intercom", "drift", "zendesk", "hubspot", "crisp",
    "livechat", "tawk", "olark", "freshchat", "chaport", "botpress",
    "kommunicate", "landbot", "manychat", "chatfuel", "dialogflow",
    "watson-assistant", "ada-embed", "gorgias",
]

# Known analytics signatures
ANALYTICS_SIGNATURES = [
    "google-analytics", "googletagmanager", "gtag", "ga.js", "analytics.js",
    "facebook.net/en_US/fbevents", "pixel", "hotjar", "mixpanel",
    "segment.com", "plausible", "matomo", "clicky",
]


def analyze_website(url, verbose=False):
    """Analyze a website and return a detailed report."""
    report = {
        "url": url,
        "analyzed_at": datetime.now().isoformat(),
        "loads": False,
        "is_https": url.startswith("https"),
        "load_time_ms": 0,
        "has_mobile_viewport": False,
        "has_chatbot": False,
        "chatbot_provider": "",
        "has_contact_form": False,
        "has_analytics": False,
        "analytics_provider": "",
        "has_schema_markup": False,
        "has_social_meta": False,
        "has_ssl": False,
        "title": "",
        "description": "",
        "issues": [],
        "opportunities": [],
        "score": 0,
    }

    # Ensure URL has scheme
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
        report["url"] = url

    try:
        start = time.time()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        load_time = (time.time() - start) * 1000
        report["loads"] = True
        report["load_time_ms"] = round(load_time)
        report["has_ssl"] = resp.url.startswith("https")
        report["is_https"] = resp.url.startswith("https")
    except requests.exceptions.SSLError:
        report["issues"].append("SSL certificate error — site not secure")
        report["opportunities"].append("SSL/HTTPS setup needed — critical for trust and SEO")
        # Try HTTP fallback
        try:
            url_http = url.replace("https://", "http://")
            resp = requests.get(url_http, headers=headers, timeout=15)
            report["loads"] = True
        except Exception:
            report["issues"].append("Website does not load at all")
            report["score"] = 1
            return report
    except requests.exceptions.ConnectionError:
        report["issues"].append("Website does not load — connection refused")
        report["score"] = 1
        return report
    except requests.exceptions.Timeout:
        report["issues"].append("Website took over 15 seconds to load")
        report["score"] = 2
        return report
    except Exception as e:
        report["issues"].append(f"Error loading website: {str(e)}")
        report["score"] = 1
        return report

    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    # ─── Title & Meta ─────────────────────────────────────────────
    title_tag = soup.find("title")
    report["title"] = title_tag.get_text(strip=True) if title_tag else ""
    if not report["title"]:
        report["issues"].append("Missing page title — hurts SEO")

    meta_desc = soup.find("meta", attrs={"name": "description"})
    report["description"] = meta_desc["content"] if meta_desc and meta_desc.get("content") else ""
    if not report["description"]:
        report["issues"].append("Missing meta description — hurts SEO")

    # ─── Mobile Viewport ─────────────────────────────────────────
    viewport = soup.find("meta", attrs={"name": "viewport"})
    report["has_mobile_viewport"] = viewport is not None
    if not viewport:
        report["issues"].append("No mobile viewport tag — site may not be mobile-friendly")
        report["opportunities"].append("Mobile optimization needed — 60%+ of web traffic is mobile")

    # ─── HTTPS Check ──────────────────────────────────────────────
    if not report["is_https"]:
        report["issues"].append("Site is not using HTTPS — browsers show 'Not Secure' warning")
        report["opportunities"].append("HTTPS migration needed — critical for trust and Google ranking")

    # ─── Load Time ────────────────────────────────────────────────
    if report["load_time_ms"] > 3000:
        report["issues"].append(f"Slow load time ({report['load_time_ms']}ms) — visitors leave after 3 seconds")
        report["opportunities"].append("Site speed optimization could reduce bounce rate")

    # ─── Chatbot Detection ────────────────────────────────────────
    html_lower = html.lower()
    for sig in CHATBOT_SIGNATURES:
        if sig in html_lower:
            report["has_chatbot"] = True
            report["chatbot_provider"] = sig
            break
    if not report["has_chatbot"]:
        report["opportunities"].append("NO AI chatbot — missing 24/7 lead capture and customer support")

    # ─── Contact Form ─────────────────────────────────────────────
    forms = soup.find_all("form")
    for form in forms:
        inputs = form.find_all("input")
        input_types = [i.get("type", "").lower() for i in inputs]
        input_names = [i.get("name", "").lower() for i in inputs]
        if "email" in input_types or any("email" in n for n in input_names):
            report["has_contact_form"] = True
            break
    if not report["has_contact_form"]:
        report["issues"].append("No contact form found — losing potential leads")
        report["opportunities"].append("Contact form + AI chatbot would capture leads 24/7")

    # ─── Analytics ────────────────────────────────────────────────
    for sig in ANALYTICS_SIGNATURES:
        if sig in html_lower:
            report["has_analytics"] = True
            report["analytics_provider"] = sig
            break
    if not report["has_analytics"]:
        report["issues"].append("No analytics tracking — can't measure what you can't track")
        report["opportunities"].append("Analytics setup (Google Analytics) for visitor insights")

    # ─── Schema Markup ────────────────────────────────────────────
    schemas = soup.find_all("script", attrs={"type": "application/ld+json"})
    report["has_schema_markup"] = len(schemas) > 0
    if not report["has_schema_markup"]:
        report["issues"].append("No structured data (schema markup) — missing rich search results")
        report["opportunities"].append("Schema markup for better Google search visibility")

    # ─── Social Meta (Open Graph / Twitter) ───────────────────────
    og = soup.find("meta", attrs={"property": "og:title"})
    tw = soup.find("meta", attrs={"name": "twitter:card"})
    report["has_social_meta"] = og is not None or tw is not None
    if not report["has_social_meta"]:
        report["issues"].append("No social media meta tags — shared links look plain")

    # ─── Calculate Score ──────────────────────────────────────────
    score = 10
    deductions = {
        "loads": 0,  # Already handled above
        "is_https": -2,
        "has_mobile_viewport": -1,
        "has_chatbot": -2,
        "has_contact_form": -1,
        "has_analytics": -1,
        "has_schema_markup": -1,
        "has_social_meta": -0.5,
    }
    for key, penalty in deductions.items():
        if not report.get(key):
            score += penalty

    if report["load_time_ms"] > 3000:
        score -= 1
    if not report["title"]:
        score -= 0.5
    if not report["description"]:
        score -= 0.5

    report["score"] = max(1, min(10, round(score)))

    # Add overall opportunity summary
    if not report["has_chatbot"]:
        report["opportunities"].insert(0, "AI CHATBOT: Biggest opportunity — 24/7 lead capture, instant responses, automated follow-up")

    return report


def print_report(report):
    """Print a formatted report card."""
    score = report["score"]
    grade_map = {10: "A+", 9: "A", 8: "B+", 7: "B", 6: "C+", 5: "C", 4: "D", 3: "D-", 2: "F", 1: "F"}
    grade = grade_map.get(score, "F")

    print(f"\n{'='*60}")
    print(f"  WEBSITE ANALYSIS: {report['url']}")
    print(f"  Score: {score}/10 (Grade: {grade})")
    print(f"  {'GREAT TARGET' if score <= 5 else 'GOOD TARGET' if score <= 7 else 'ALREADY OPTIMIZED'}")
    print(f"{'='*60}")

    print(f"\n  Title: {report['title'][:60] or 'MISSING'}")
    print(f"  Load Time: {report['load_time_ms']}ms {'(SLOW)' if report['load_time_ms'] > 3000 else '(OK)'}")
    print(f"  HTTPS: {'Yes' if report['is_https'] else 'NO'}")
    print(f"  Mobile-Ready: {'Yes' if report['has_mobile_viewport'] else 'NO'}")
    print(f"  Chatbot: {'Yes (' + report['chatbot_provider'] + ')' if report['has_chatbot'] else 'NO'}")
    print(f"  Contact Form: {'Yes' if report['has_contact_form'] else 'NO'}")
    print(f"  Analytics: {'Yes (' + report['analytics_provider'] + ')' if report['has_analytics'] else 'NO'}")
    print(f"  Schema Markup: {'Yes' if report['has_schema_markup'] else 'NO'}")
    print(f"  Social Meta: {'Yes' if report['has_social_meta'] else 'NO'}")

    if report["issues"]:
        print(f"\n  ISSUES FOUND ({len(report['issues'])}):")
        for i, issue in enumerate(report["issues"], 1):
            print(f"  {i}. {issue}")

    if report["opportunities"]:
        print(f"\n  AI SERVICE OPPORTUNITIES ({len(report['opportunities'])}):")
        for i, opp in enumerate(report["opportunities"], 1):
            print(f"  {i}. {opp}")

    print(f"\n{'='*60}\n")


def analyze_from_excel(filepath):
    """Analyze all websites from a leads Excel file."""
    if not HAS_PANDAS:
        print("ERROR: pandas is required for Excel processing. Run: pip install pandas openpyxl")
        sys.exit(1)

    df = pd.read_excel(filepath)
    if "website" not in df.columns:
        print("ERROR: Excel file must have a 'website' column")
        sys.exit(1)

    results = []
    websites = df["website"].dropna().unique()
    print(f"\nAnalyzing {len(websites)} websites...\n")

    for i, url in enumerate(websites, 1):
        if not url or str(url).strip() == "":
            continue
        print(f"[{i}/{len(websites)}] Analyzing: {url}")
        report = analyze_website(str(url).strip())
        print_report(report)
        results.append(report)
        time.sleep(1)  # Be respectful

    # Save results
    if results:
        output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        outpath = os.path.join(output_dir, f"site_analysis_{timestamp}.xlsx")

        results_df = pd.DataFrame(results)
        results_df.to_excel(outpath, index=False, sheet_name="Analysis")
        print(f"\nResults saved to: {outpath}")
        print(f"Total analyzed: {len(results)}")
        print(f"No chatbot: {len([r for r in results if not r['has_chatbot']])}")
        print(f"Score 5 or below (great targets): {len([r for r in results if r['score'] <= 5])}")


def main():
    parser = argparse.ArgumentParser(description="Jaybird Website Analyzer — Find AI service opportunities")
    parser.add_argument("--url", type=str, help="Single website URL to analyze")
    parser.add_argument("--file", type=str, help="Excel file with 'website' column to batch analyze")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    args = parser.parse_args()

    if args.url:
        report = analyze_website(args.url, verbose=args.verbose)
        print_report(report)
    elif args.file:
        analyze_from_excel(args.file)
    else:
        print("Usage:")
        print("  python site_analyzer.py --url https://example.com")
        print("  python site_analyzer.py --file ../output/leads.xlsx")
        sys.exit(1)


if __name__ == "__main__":
    main()
