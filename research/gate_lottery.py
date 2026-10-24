"""GATE M1 — after publication, among US common stocks, is a stock that just had a lottery-like
one-day spike a worse buy, per unit of market risk, than a typical stock next month?

The last untested eligible candidate on the literature short-list (research/LITERATURE.md): Bali,
Cakici & Whitelaw (2011) — stocks with an extreme one-day gain last month earn low returns next
month. The long-only use is a NEGATIVE SCREEN (do not buy right after the spike), so the gated
series is the avoid leg, not the long-short, and it is judged by its CAPM alpha: lottery stocks
carry more market beta, and a raw comparison would score the window's market return instead of
the stock-specific drag. The bar is pre-registered in FINDINGS [GATE M1]; this module must not be
run before that entry is committed.

Data (official, free): Jensen, Kelly & Pedersen, Global Factor Data (jkpfactors.com), USA, monthly.
Portfolios: the three terciles underlying the `rmax1_21d` factor (the largest daily return over
the formation month), capped value-weighted (market cap winsorized at the NYSE 80th percentile);
pf 1 = low, 2 = middle, 3 = high; breakpoints set on stocks above the NYSE 20th percentile; return
month t+1; universe common stocks (CRSP share code 10/11/12) on NYSE/AMEX/NASDAQ, primary listing
— no ETFs, the flaw that ruled out Open Source Asset Pricing's MaxRet decile files.
Market: the same library's USA `mkt` factor, value-weighted excess return. Returns are excess of
the T-bill; differences between terciles cancel it.

  avoid_t  = pf 2 − pf 3     a typical stock minus a spiked one (GATED, by its CAPM alpha)
  spread_t = pf 1 − pf 3     the published long-short form (terciles)
  low_t    = pf 1 − pf 2     descriptive only

  python3 -m research.gate_lottery          # download, verify, evaluate the window, print
Stdlib only. Nothing is written to disk.
"""
import csv
import hashlib
import io
import math
import statistics
import sys
import urllib.request
import zipfile

from research.gate_reversal import expected_months, nw_t

BASE = "https://jkpfactors-data.s3.amazonaws.com/public/"
PF_URL = BASE + "portfolios/%5Busa%5D_%5Brmax1_21d%5D_%5Bmonthly%5D_%5Bvw_cap%5D.zip"
MKT_URL = BASE + "%5Busa%5D_%5Bmkt%5D_%5Bmonthly%5D_%5Bvw%5D.zip"
# The exact files, by MD5 (S3 ETag, Last-Modified 2026-08-04) — a changed file is refused.
PF_MD5 = "2cac794c7f22fd4cffdbc83806c2e1ce"
MKT_MD5 = "4cfedead71640b65c9150b4e9e241416"
CHAR = "rmax1_21d"
# ---- Pre-registered in FINDINGS [GATE M1]; change none of these after the first run. ----
START, END = 201103, 202512     # first return month formed after the JFE issue (Feb 2011) → the
                                # library's last month
PREMISE = (196207, 200512)      # the paper's sample, 522 months
PREMISE_MIN_MONTHS = 400
WP_ERA = (200601, 201102)       # out of sample but before the journal issue — descriptive only
NW_LAGS = 3
ALPHA = 0.05                    # a SCREEN, as [GATE R1]: a PASS licenses only a tested component of
                                # the next pre-registration, whose bar carries the correction


def fetch(url: str, md5: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        blob = r.read()
    got = hashlib.md5(blob).hexdigest()
    if got != md5:
        raise SystemExit(f"GATE M1 refuses: {url} is not the pre-registered file (md5 {got}, "
                         f"expected {md5}) — nothing was read; amend before running")
    return blob


def read_csv(blob: bytes) -> list[dict]:
    """Rows of the zip's single CSV member. PURE."""
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if len(names) != 1:
            raise ValueError(f"expected one CSV in the zip, found {names!r}")
        text = z.read(names[0]).decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def _pick(cols, *options):
    for o in options:
        if o in cols:
            return o
    raise ValueError(f"none of {options} in columns {sorted(cols)!r}")


def _ym(s: str) -> int:
    d = s.replace("-", "").replace("/", "").strip()
    return int(d[:6])


def _keep(rec: dict, cols, weighting: str) -> bool:
    """Drop rows for another country, characteristic, weighting or frequency, when the file
    carries those columns; anything left that still collides on a key is refused downstream."""
    want = {"excntry": ("usa",), "location": ("usa",), "characteristic": (CHAR, "mkt"),
            "name": (CHAR, "mkt"), "weighting": (weighting,), "freq": ("monthly", "m")}
    return all(rec[c].strip().lower() in want[c] for c in want if c in cols)


def to_pct(values: list[float]) -> float:
    """×100 for decimal returns, ×1 for a file already in percent: a median |monthly return| above
    0.5 cannot be decimal. PURE."""
    return 1.0 if statistics.median(abs(v) for v in values) > 0.5 else 100.0


def parse_pfs(rows: list[dict]) -> tuple[dict[int, dict[int, float]], dict, dict]:
    """({YYYYMM: {pf: ret %}}, {YYYYMM: {pf: median signal}}, {YYYYMM: {pf: n}}). PURE."""
    cols = set(rows[0]) if rows else set()
    dcol, rcol = _pick(cols, "eom", "date"), _pick(cols, "ret_vw_cap", "ret")
    ncol = next((c for c in ("n", "n_stocks") if c in cols), None)
    rets, sig, n = {}, {}, {}
    for rec in rows:
        if not _keep(rec, cols, "vw_cap") or rec[rcol] in ("", "NA"):
            continue
        ym, pf = _ym(rec[dcol]), int(float(rec["pf"]))
        if pf in rets.get(ym, {}):
            raise ValueError(f"two rows for {ym} pf {pf} — the file stacks series the parser "
                             f"cannot tell apart; refusing")
        rets.setdefault(ym, {})[pf] = float(rec[rcol])
        if "signal" in cols and rec["signal"] not in ("", "NA"):
            sig.setdefault(ym, {})[pf] = float(rec["signal"])
        if ncol and rec[ncol] not in ("", "NA"):
            n.setdefault(ym, {})[pf] = int(float(rec[ncol]))
    if not rets:
        raise ValueError("no portfolio rows")
    k = to_pct([v for p in rets.values() for v in p.values()])
    return {ym: {pf: v * k for pf, v in p.items()} for ym, p in rets.items()}, sig, n


def parse_mkt(rows: list[dict]) -> dict[int, float]:
    """{YYYYMM: market excess return %}. PURE."""
    cols = set(rows[0]) if rows else set()
    dcol, rcol = _pick(cols, "eom", "date"), _pick(cols, "ret", "mkt_vw_exc")
    out: dict[int, float] = {}
    for r in rows:
        if not _keep(r, cols, "vw") or r[rcol] in ("", "NA"):
            continue
        ym = _ym(r[dcol])
        if ym in out:
            raise ValueError(f"two market rows for {ym}; refusing")
        out[ym] = float(r[rcol])
    if not out:
        raise ValueError("no market rows")
    k = to_pct(list(out.values()))
    return {ym: v * k for ym, v in out.items()}


def series(rets: dict[int, dict[int, float]]) -> tuple[dict, dict, dict]:
    """(avoid, spread, low) per month in %, for months carrying all three terciles. PURE."""
    avoid, spread, low = {}, {}, {}
    for ym, p in rets.items():
        if all(k in p for k in (1, 2, 3)):
            avoid[ym], spread[ym], low[ym] = p[2] - p[3], p[1] - p[3], p[1] - p[2]
    return avoid, spread, low


def capm(y: list[float], x: list[float], lags: int = NW_LAGS) -> dict:
    """OLS y = a + b·x with a Newey-West (Bartlett, n-divisor) HAC s.e. on a; one-sided p for
    a > 0 by the normal approximation. PURE."""
    n = len(y)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((v - mx) ** 2 for v in x)
    b = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / sxx
    a = my - b * mx
    e = [yi - a - b * xi for xi, yi in zip(x, y)]
    # (X'X)^-1 for X = [1, x], and S = Σ_l w_l Σ_t g_t g_{t-l}' (+ transpose), g_t = e_t·[1, x_t]
    sx, sxx0 = sum(x), sum(v * v for v in x)
    det = n * sxx0 - sx * sx
    inv = ((sxx0 / det, -sx / det), (-sx / det, n / det))
    g = [(ei, ei * xi) for ei, xi in zip(e, x)]
    s = [[0.0, 0.0], [0.0, 0.0]]
    for l in range(0, lags + 1):
        w = 1.0 if l == 0 else 2 * (1 - l / (lags + 1))
        for i in range(2):
            for j in range(2):
                acc = sum(g[t][i] * g[t - l][j] for t in range(l, n))
                if l:
                    acc = (acc + sum(g[t - l][i] * g[t][j] for t in range(l, n))) / 2
                s[i][j] += w * acc
    # V = inv · S · inv; only V[0][0] (Var a) is needed
    row = [inv[0][0] * s[0][k] + inv[0][1] * s[1][k] for k in range(2)]
    var_a = row[0] * inv[0][0] + row[1] * inv[1][0]
    se = math.sqrt(max(var_a, 0.0))
    t = a / se if se > 0 else float("inf")
    return {"alpha": a, "beta": b, "se": se, "t": t,
            "p": 0.5 * (1 - math.erf(t / math.sqrt(2))), "resid_sd": statistics.pstdev(e)}


def evaluate(avoid: dict, spread: dict, mkt: dict, start: int = START, end: int = END) -> dict:
    """The window's statistics and the four window conditions. PURE. (The fifth, the premise,
    is checked by `premise` on the paper's own sample.)
    (1) avoid CAPM alpha > 0 at one-sided HAC p ≤ ALPHA; (2) the market-adjusted avoid series
    (full-window beta) has a positive mean in both halves by month count; (3) ... with the single
    best month removed; (4) the spread's CAPM alpha > 0 (sign only)."""
    months = sorted(ym for ym in avoid if start <= ym <= end and ym in mkt and ym in spread)
    y, x = [avoid[ym] for ym in months], [mkt[ym] for ym in months]
    c = capm(y, x)
    adj = [yi - c["beta"] * xi for yi, xi in zip(y, x)]
    h = len(adj) // 2
    trimmed = sorted(adj)[:-1]
    k5 = max(1, round(0.05 * len(adj)))
    cs = capm([spread[ym] for ym in months], x)
    checks = {"alpha_significant": c["alpha"] > 0 and c["p"] <= ALPHA,
              "both_halves": statistics.mean(adj[:h]) > 0 and statistics.mean(adj[h:]) > 0,
              "not_one_month": statistics.mean(trimmed) > 0,
              "spread_alpha_sign": cs["alpha"] > 0}
    raw_m, _, raw_t, _ = nw_t(y, NW_LAGS)
    return {"n": len(y), "first": months[0], "last": months[-1], "capm": c, "spread": cs,
            "half1": (months[0], months[h - 1], statistics.mean(adj[:h])),
            "half2": (months[h], months[-1], statistics.mean(adj[h:])),
            "trimmed": statistics.mean(trimmed), "trimmed5": statistics.mean(sorted(adj)[:-k5]),
            "k5": k5, "raw_mean": raw_m, "raw_t": raw_t, "median_adj": statistics.median(adj),
            "pos": sum(v > 0 for v in adj) / len(adj), "checks": checks,
            "verdict": "PASS" if all(checks.values()) else "FAIL"}


def premise(avoid: dict, mkt: dict, start: int = PREMISE[0], end: int = PREMISE[1]) -> dict:
    """The effect must exist in THIS construction over the paper's own sample: avoid CAPM alpha
    > 0 (sign only), on at least PREMISE_MIN_MONTHS months. PURE."""
    months = sorted(ym for ym in avoid if start <= ym <= end and ym in mkt)
    if len(months) < PREMISE_MIN_MONTHS:
        raise ValueError(f"premise window has {len(months)} months (< {PREMISE_MIN_MONTHS})")
    c = capm([avoid[ym] for ym in months], [mkt[ym] for ym in months])
    return {"n": len(months), "first": months[0], "last": months[-1], "capm": c,
            "holds": c["alpha"] > 0}


def mde80(resid_sd: float, n: int, z_alpha: float = 1.6449) -> float:
    """The alpha detectable with 80% power at one-sided ALPHA, from a residual SD — approximate:
    it ignores autocorrelation and the beta's own estimation error. PURE."""
    return (z_alpha + 0.8416) * resid_sd / math.sqrt(n)


def check_order(sig: dict, rets: dict, months: list[int], premise_months: list[int]) -> str:
    """pf 3 must be the HIGH-rmax tercile; a mix-up would invert the verdict, so a violation
    raises. From the file's own median-signal column when it carries one; otherwise pf 3 must be
    the more volatile tercile over the paper's sample (MAX is a volatility proxy). PURE."""
    have = [ym for ym in months if ym in sig and all(k in sig[ym] for k in (1, 3))]
    if have:
        bad = [ym for ym in have if not sig[ym][3] > sig[ym][1]]
        if bad:
            raise ValueError(f"pf 3 is not the high-{CHAR} tercile in {len(bad)} month(s), "
                             f"e.g. {bad[0]}")
        return f"verified in {len(have)} of {len(months)} months (median signal pf 3 > pf 1)"
    sd = {k: statistics.pstdev(rets[ym][k] for ym in premise_months) for k in (1, 3)}
    if not sd[3] > sd[1]:
        raise ValueError(f"no signal column and pf 3 is not the more volatile tercile "
                         f"(SD {sd[3]:.2f} vs {sd[1]:.2f}); refusing")
    return f"no signal column; pf 3 SD {sd[3]:.2f}% > pf 1 SD {sd[1]:.2f}% over the premise window"


def check_alignment(rets: dict, mkt: dict, months: list[int]) -> float:
    """The portfolio and market files must be dated by the same return month: the middle tercile's
    beta on the same-month market must sit in [0.5, 1.5] and beat its beta on the market one month
    either side. A one-month shift would turn "alpha" into the raw mean, silently. PURE."""
    def beta(shift: int) -> float:
        ms = expected_months(months[0], months[-1])
        pairs = [(rets[ms[i]][2], mkt[ms[i + shift]]) for i in range(len(ms))
                 if 0 <= i + shift < len(ms) and ms[i] in rets and 2 in rets[ms[i]]
                 and ms[i + shift] in mkt]
        return capm([p for p, _ in pairs], [m for _, m in pairs])["beta"]
    b0, lag, lead = beta(0), beta(-1), beta(1)
    if not (0.5 <= b0 <= 1.5 and b0 > abs(lag) and b0 > abs(lead)):
        raise ValueError(f"files look misaligned: pf 2 beta {b0:.2f} same month, {lag:.2f} / "
                         f"{lead:.2f} one month either side; refusing")
    return b0


def _alpha_line(label: str, c: dict, n: int) -> str:
    return (f"  {label}: n={n} CAPM alpha {c['alpha']:+.3f}%/mo (HAC t={c['t']:.2f}, one-sided "
            f"p={c['p']:.4f}) beta {c['beta']:+.2f} · residual SD {c['resid_sd']:.2f}%")


def run(argv: list[str]) -> int:
    pblob, mblob = fetch(PF_URL, PF_MD5), fetch(MKT_URL, MKT_MD5)
    rets, sig, n = parse_pfs(read_csv(pblob))
    mkt = parse_mkt(read_csv(mblob))
    avoid, spread, low = series(rets)
    window = expected_months(START, END)
    missing = [ym for ym in window if ym not in avoid or ym not in mkt]
    if missing:
        raise SystemExit(f"GATE M1 refuses to print a verdict: {len(missing)} window month(s) "
                         f"missing ({missing[:3]}…) — the series is incomplete")
    pmonths = [ym for ym in expected_months(*PREMISE) if ym in avoid and ym in mkt]
    order = check_order(sig, rets, window, pmonths)
    b_mid = check_alignment(rets, mkt, window)
    print(f"GATE M1 — lottery-stock avoidance, JKP USA {CHAR} terciles (capped VW): pf 2 − pf 3, "
          f"judged by CAPM alpha vs the VW market")
    print(f"  files: portfolios md5 {PF_MD5} ({len(pblob):,} B), market md5 {MKT_MD5} "
          f"({len(mblob):,} B) · portfolio months {min(rets)}–{max(rets)} · market "
          f"{min(mkt)}–{max(mkt)} · ordering {order} · pf 2 market beta {b_mid:.2f}")
    if max(rets) > END or max(mkt) > END:
        print(f"  note: the files run past the window end {END} ✗ — the window stops there as "
              f"pre-registered")
    pr = premise(avoid, mkt)
    print(_alpha_line(f"premise, paper's sample {pr['first']}–{pr['last']}", pr["capm"], pr["n"]))
    r = evaluate(avoid, spread, mkt)
    print(f"  power (approximate): at the premise residual SD, the 80%-power detectable alpha "
          f"over n={r['n']} is {mde80(pr['capm']['resid_sd'], r['n']):.2f}%/mo (window residual "
          f"SD gives "
          f"{mde80(r['capm']['resid_sd'], r['n']):.2f})")
    print(_alpha_line(f"pre-registered window {r['first']}–{r['last']}", r["capm"], r["n"]))
    print(f"  market-adjusted halves: {r['half1'][0]}–{r['half1'][1]} {r['half1'][2]:+.3f}% · "
          f"{r['half2'][0]}–{r['half2'][1]} {r['half2'][2]:+.3f}% · best month removed "
          f"{r['trimmed']:+.3f}% · spread (pf 1 − pf 3) alpha {r['spread']['alpha']:+.3f}% "
          f"(t={r['spread']['t']:.2f})")
    checks = {"premise": pr["holds"], **r["checks"]}
    marks = " · ".join(f"{k} {'✓' if v else '✗'}" for k, v in checks.items())
    verdict = "PASS" if all(checks.values()) else "FAIL"
    tag = "" if pr["holds"] else " (PREMISE ABSENT: no effect in this construction in-sample)"
    if verdict == "PASS" and r["raw_mean"] < 0:
        tag = " (risk-adjusted only: raw avoid was negative — the screen cost money in the window)"
    print(f"  bar: {marks}  →  VERDICT {verdict}{tag}")
    # Descriptive only, never part of the bar.
    lw = [low[ym] for ym in window]
    print(f"  descriptive: raw avoid mean {r['raw_mean']:+.3f}%/mo (NW t={r['raw_t']:.2f}) · "
          f"adjusted median {r['median_adj']:+.3f}% · positive {100 * r['pos']:.0f}% of months · "
          f"best {r['k5']} months removed {r['trimmed5']:+.3f}% · low leg (pf 1 − pf 2) mean "
          f"{statistics.mean(lw):+.3f}%")
    if n:
        print(f"  smallest pf 3 stock count in window: {min(n[ym].get(3, 0) for ym in window)}")
    wp = evaluate(avoid, spread, mkt, *WP_ERA)
    print(_alpha_line(f"descriptive, working-paper era {wp['first']}–{wp['last']}", wp["capm"],
                      wp["n"]))
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
