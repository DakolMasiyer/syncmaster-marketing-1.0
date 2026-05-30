import json
import re
from pathlib import Path

METRICS_PATH = Path(__file__).resolve().parents[1] / "metrics.json"


def _load_metrics():
    if METRICS_PATH.exists():
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    return {"current": "", "snapshots": {}}


def _snapshot_for(post):
    metrics = _load_metrics()
    snapshots = metrics.get("snapshots", {})
    date = post.get("date", "")
    month_key = date[:7]
    return snapshots.get(month_key) or snapshots.get(metrics.get("current", "")) or {}


def _substitute(patterns, text):
    updated = text
    for pattern, replacement in patterns:
        updated = re.sub(pattern, replacement, updated, flags=re.MULTILINE)
    return updated


def apply_live_metrics(body, post):
    """
    Replace hardcoded operational numbers in body copy with month-appropriate
    values from carousel/metrics.json.
    """
    snapshot = _snapshot_for(post)
    if not snapshot:
        return body

    month_key = post.get("date", "")[:7]
    patterns = []

    if month_key == "2026-06":
        patterns = [
            (r"20 applications\. 6 vetted\.", f"{snapshot['applications_received']} applications. {snapshot['composers_vetted']} vetted."),
            (r"Of 20 applications in Month 1: 6 passed all six criteria\.", f"Of {snapshot['applications_received']} applications in Month 1: {snapshot['composers_vetted']} passed all six criteria."),
            (r"⏱ Fastest turnaround \(brief to delivery\): 48 hours", f"⏱ Fastest turnaround (brief to delivery): {snapshot['fastest_turnaround_hours']} hours"),
            (r"20 applications reviewed", f"{snapshot['applications_received']} applications reviewed"),
            (r"✅ 6 composers vetted", f"✅ {snapshot['composers_vetted']} composers vetted"),
            (r"🎵 11 tracks pitched to supervisors", f"🎵 {snapshot['tracks_pitched']} tracks pitched to supervisors"),
            (r"⏱ Fastest brief response: 48 hours", f"⏱ Fastest brief response: {snapshot['fastest_turnaround_hours']} hours"),
        ]
    elif month_key == "2026-07":
        patterns = [
            (r"Of 31 applications, 9 are in the active catalogue\.", f"Of {snapshot['applications_received']} applications, {snapshot['composers_active']} are in the active catalogue."),
            (r"9 composers\. 61 tracks\. 5 briefs handled\. 2 placements confirmed across 2 months\. 22-hour average brief-to-delivery turnaround\.", f"{snapshot['composers_active']} composers. {snapshot['tracks_in_pool']} tracks. {snapshot['briefs_handled']} briefs handled. {snapshot['placements_confirmed']} placements confirmed across 2 months. {snapshot['average_turnaround_hours']}-hour average brief-to-delivery turnaround."),
            (r"Brief-response time is down\. Month 1 average: 31 hours\. Month 2 average: 22 hours\.", f"Brief-response time is down. Month 1 average: 31 hours. Month 2 average: {snapshot['average_turnaround_hours']} hours."),
            (r"⏱ Fastest turnaround: 11 hours(?: \(brief to full delivery\))?", f"⏱ Fastest turnaround: {snapshot['fastest_turnaround_hours']} hours"),
            (r"Average time from brief receipt to first delivery: 22 hours\.", f"Average time from brief receipt to first delivery: {snapshot['average_turnaround_hours']} hours."),
            (r"📋 3 briefs handled", f"📋 {snapshot['briefs_handled']} briefs handled"),
            (r"✅ 9 composers in the active catalogue", f"✅ {snapshot['composers_active']} composers in the active catalogue"),
            (r"🎵 61 one-stop tracks", f"🎵 {snapshot['tracks_in_pool']} one-stop tracks"),
            (r"⏱ 22h average brief-to-delivery turnaround", f"⏱ {snapshot['average_turnaround_hours']}h average brief-to-delivery turnaround"),
            (r"→ 2 placements confirmed total", f"→ {snapshot['placements_confirmed']} placements confirmed total"),
            (r"→ 5 briefs handled", f"→ {snapshot['briefs_handled']} briefs handled"),
            (r"→ 9 composers in the active catalogue", f"→ {snapshot['composers_active']} composers in the active catalogue"),
            (r"5 briefs handled\.", f"{snapshot['briefs_handled']} briefs handled."),
            (r"2 placements confirmed across 2 months\.", f"{snapshot['placements_confirmed']} placements confirmed across 2 months."),
        ]
    elif month_key == "2026-08":
        patterns = [
            (r"47 applications\. 12 composers\. 9 briefs\. 31 tracks submitted\. 3 confirmed placements\.", f"{snapshot['applications_received']} applications. {snapshot['composers_active']} composers. {snapshot['briefs_handled']} briefs. {snapshot['tracks_submitted']} tracks submitted. {snapshot['placements_confirmed']} confirmed placements."),
            (r"1/ 47 applications received since June 1\.", f"1/ {snapshot['applications_received']} applications received since June 1."),
            (r"2/ 9 briefs handled in 90 days\.", f"2/ {snapshot['briefs_handled']} briefs handled in 90 days."),
            (r"3/ Median response time: 18 hours from brief receipt to track delivery\.", f"3/ Median response time: {snapshot['median_response_hours']} hours from brief receipt to track delivery."),
            (r"Fastest: 11 hours\.", f"Fastest: {snapshot['fastest_turnaround_hours']} hours."),
            (r"→ 47 applications total", f"→ {snapshot['applications_received']} applications total"),
            (r"→ 12 composers active", f"→ {snapshot['composers_active']} composers active"),
            (r"→ 9 briefs handled", f"→ {snapshot['briefs_handled']} briefs handled"),
            (r"→ 3 confirmed placements", f"→ {snapshot['placements_confirmed']} confirmed placements"),
            (r"→ 47 applications reviewed", f"→ {snapshot['applications_received']} applications reviewed"),
            (r"→ 12 composers passed vetting", f"→ {snapshot['composers_active']} composers passed vetting"),
            (r"→ 94 tracks entered the active pool", f"→ {snapshot['tracks_in_pool']} tracks entered the active pool"),
            (r"94 tracks in the active pool\.", f"{snapshot['tracks_in_pool']} tracks in the active pool."),
            (r"12 active composers \(2 applications under vetting\)\.", f"{snapshot['composers_active']} active composers (2 applications under vetting)."),
            # ── Additional Month 3 Bullet lists and article variations ──
            (r"— 47 applications received", f"— {snapshot['applications_received']} applications received"),
            (r"— 12 composers vetted, cleared, active", f"— {snapshot['composers_active']} composers vetted, cleared, active"),
            (r"— 9 briefs handled", f"— {snapshot['briefs_handled']} briefs handled"),
            (r"— 31 tracks submitted across those briefs", f"— {snapshot['tracks_submitted']} tracks submitted across those briefs"),
            (r"— 3 confirmed placements", f"— {snapshot['placements_confirmed']} confirmed placements"),
            (r"— Fastest brief response: 11 hours", f"— Fastest brief response: {snapshot['fastest_turnaround_hours']} hours"),
            (r"Active composers: 12", f"Active composers: {snapshot['composers_active']}"),
            (r"Catalogues fully documented: 12", f"Catalogues fully documented: {snapshot['composers_active']}"),
            (r"Tracks in active submission pool: 94", f"Tracks in active submission pool: {snapshot['tracks_in_pool']}"),
            (r"We've handled 9 briefs in 90 days\.", f"We've handled {snapshot['briefs_handled']} briefs in 90 days."),
            (r"vetted 12 African composers", f"vetted {snapshot['composers_active']} African composers"),
            (r"three confirmed sync placements", f"{snapshot['placements_confirmed']} confirmed sync placements"),
            (r"three confirmed placements", f"{snapshot['placements_confirmed']} confirmed placements"),
            (r"Three placements\. 90 days\.", f"{snapshot['placements_confirmed']} placements. 90 days."),
            (r"Three placements confirmed\.", f"{snapshot['placements_confirmed']} placements confirmed."),
            (r"3 confirmed placements entering August: 3", f"3 confirmed placements entering August: {snapshot['placements_confirmed']}"),
            (r"3 confirmed placements across 2 months\.", f"{snapshot['placements_confirmed']} confirmed placements across 2 months."),
            (r"three placements across 90 days", f"{snapshot['placements_confirmed']} placements across 90 days"),
            (r"three placements over 90 days", f"{snapshot['placements_confirmed']} placements over 90 days"),
        ]

    return _substitute(patterns, body)
