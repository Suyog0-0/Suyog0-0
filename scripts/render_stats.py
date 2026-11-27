#!/usr/bin/env python3
"""Fetch public GitHub contribution data and render glass streak cards (dark + light SVG)."""
import os, re, sys, json, datetime as dt, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glasskit import *

USER = os.environ.get("GH_USER", "Suyog0-0")
OUTDIR = os.environ.get("STATS_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "stats"))
UA = {"User-Agent": "Mozilla/5.0 (readme-stats)"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    tok = os.environ.get("GITHUB_TOKEN")
    if tok and "api.github.com" in url: req.add_header("Authorization", "Bearer " + tok)
    with urllib.request.urlopen(req, timeout=30) as r: return r.read().decode("utf-8", "ignore")

def year_days(y):
    html_ = get("https://github.com/users/%s/contributions?from=%d-01-01&to=%d-12-31" % (USER, y, y))
    tips = {}
    for m in re.finditer(r'<tool-tip[^>]*?for="([^"]+)"[^>]*>([^<]*)</tool-tip>', html_):
        t = m.group(2).strip(); n = re.match(r"(\d[\d,]*) contribution", t)
        tips[m.group(1)] = int(n.group(1).replace(",", "")) if n else 0
    days = {}
    for m in re.finditer(r"<td\b[^>]*>", html_):
        tag = m.group(0); d = re.search(r'data-date="(\d{4}-\d{2}-\d{2})"', tag)
        if not d: continue
        i = re.search(r'\bid="([^"]+)"', tag); lvl = re.search(r'data-level="(\d)"', tag)
        cnt = tips.get(i.group(1)) if i else None
        if cnt is None: cnt = 1 if (lvl and lvl.group(1) != "0") else 0
        days[d.group(1)] = cnt
    return days

def collect():
    today = dt.date.today(); days = {}
    try:
        created = json.loads(get("https://api.github.com/users/" + USER))["created_at"][:10]
        start = int(created[:4])
    except Exception:
        created = None; start = today.year - 6
    for y in range(start, today.year + 1):
        try: days.update(year_days(y))
        except Exception as e: print("warn", y, e, file=sys.stderr)
    if created is None:
        nz = sorted(d for d, v in days.items() if v > 0)
        created = nz[0] if nz else today.isoformat()
    days = {k: v for k, v in days.items() if k <= today.isoformat()}
    return created, days, today

def compute(created, days, today):
    total = sum(days.values()); dates = sorted(days)
    longest = (0, None, None); run = 0; start = None; prev = None
    for d in dates:
        dd = dt.date.fromisoformat(d)
        if days[d] > 0:
            if prev and (dd - prev).days == 1 and run > 0: run += 1
            else: run = 1; start = dd
            if run > longest[0]: longest = (run, start, dd)
        else: run = 0
        prev = dd
    cur = (0, None, None); d = today
    if days.get(d.isoformat(), 0) == 0: d -= dt.timedelta(days=1)
    end = d; n = 0
    while days.get(d.isoformat(), 0) > 0: n += 1; d -= dt.timedelta(days=1)
    if n: cur = (n, d + dt.timedelta(days=1), end)
    return dict(total=total, since=created, current=cur, longest=longest)

def fmt(d): return d.strftime("%b %-d") if d else ""
def span(t): return ("%s – %s" % (fmt(t[1]), fmt(t[2]))) if t[0] else "No active streak"

def card(stats, t):
    P = PAL[t]; body = ''; cw, ch = 250, 178
    total = "{:,}".format(stats['total']); cur, lon = stats['current'], stats['longest']
    since = dt.date.fromisoformat(stats['since'])
    # card 1
    g = glass(0, 0, cw, ch, P, 22, sweep=True)
    g += squircle_icon(22, 22, 38, 'bars', P['acc'], P)
    num, w = odo_number(total, 24, 106, 44, P['text'], 0.5); g += num
    g += '<text x="24" y="134" font-size="13.5" font-weight="600" fill="%s">Total contributions</text>' % P['muted']
    g += '<text x="24" y="154" font-size="11.5" fill="%s">Since %s</text>' % (P['faint'], since.strftime("%b %Y"))
    body += fade(g, 0.1, 0, 0)
    # card 2 (current streak, ring)
    g = glass(0, 0, cw, ch, P, 22, sweep=True, spin=True)
    R = 46; C = 2 * 3.14159265 * R; frac = min(1.0, cur[0] / max(lon[0], 1)) if cur[0] else 0
    g += '<circle cx="125" cy="72" r="%d" stroke="%s" stroke-opacity="%s" stroke-width="8"/>' % (R, P['ln'], .14)
    g += ('<circle cx="125" cy="72" r="%d" stroke="url(#ringg)" stroke-width="8" stroke-linecap="round" stroke-dasharray="0 %.1f" transform="rotate(-90 125 72)">'
          '<animate attributeName="stroke-dasharray" from="0 %.1f" to="%.1f %.1f" dur="1.8s" begin=".5s" fill="freeze" calcMode="spline" keySplines=".16 1 .3 1" keyTimes="0;1"/></circle>'
          ) % (R, C, C, max(frac * C, 0.1), C)
    g += glyph('flame', 113, 36, 24, P['warn'], 1.7)
    s = str(cur[0]); num, w = odo_number(s, 125 - (len(s) * 36 * .6) / 2, 86, 36, P['text'], 0.6); g += num
    g += '<text x="125" y="102" text-anchor="middle" font-size="11" font-weight="600" letter-spacing="1" fill="%s">DAYS</text>' % P['faint']
    g += '<text x="125" y="146" text-anchor="middle" font-size="13.5" font-weight="700" fill="%s">Current streak</text>' % P['text']
    g += '<text x="125" y="164" text-anchor="middle" font-size="11.5" fill="%s">%s</text>' % (P['faint'], span(cur))
    body += fade(g, 0.22, 270, 0)
    # card 3
    g = glass(0, 0, cw, ch, P, 22, sweep=True)
    g += squircle_icon(22, 22, 38, 'trophy', P['warn'], P)
    s = str(lon[0]); num, w = odo_number(s, 24, 106, 44, P['text'], 0.7); g += num
    g += '<text x="%s" y="106" font-size="18" font-weight="600" fill="%s">days</text>' % (24 + w + 8, P['faint'])
    g += '<text x="24" y="134" font-size="13.5" font-weight="600" fill="%s">Longest streak</text>' % P['muted']
    g += '<text x="24" y="154" font-size="11.5" fill="%s">%s</text>' % (P['faint'], span(lon))
    body += fade(g, 0.34, 540, 0)
    defs = '<linearGradient id="ringg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (P['warn'], P['acc3'])
    return page(790, ch, P, body, defs=defs, blobs=[(120, 60, 180, 'b1', .36, 60, 30, 17), (700, 150, 200, 'b2', .34, -60, -20, 20)])

def main():
    created, days, today = collect(); stats = compute(created, days, today)
    os.makedirs(OUTDIR, exist_ok=True)
    for t in ("dark", "light"):
        open(os.path.join(OUTDIR, "streak-%s.svg" % t), "w", encoding="utf-8").write(card(stats, t))
    print(json.dumps({k: (v if not isinstance(v, tuple) else [str(x) for x in v]) for k, v in stats.items()}))

if __name__ == "__main__":
    main()
