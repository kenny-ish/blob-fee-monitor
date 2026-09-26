"""EIP-4844 blob fee market monitor."""
import argparse
import json
import sys
import time
import urllib.request

BLOB_GAS = 131_072
BARS = "▁▂▃▄▅▆▇█"


def rpc(url, method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "User-Agent": "blob-fee-monitor"})
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.load(r)
    if "error" in resp:
        raise RuntimeError(resp["error"].get("message"))
    return resp["result"]


def sparkline(values):
    lo, hi = min(values), max(values)
    if hi == lo:
        return BARS[0] * len(values)
    return "".join(BARS[int((v - lo) / (hi - lo) * (len(BARS) - 1))] for v in values)


def summarize(history):
    fees = [int(x, 16) for x in history.get("baseFeePerBlobGas") or []]
    ratios = history.get("blobGasUsedRatio") or []
    if not fees:
        return None
    past = fees[:-1] or fees
    return {"next": fees[-1], "min": min(past), "max": max(past), "avg": sum(past) / len(past),
            "util": sum(ratios) / len(ratios) if ratios else 0.0, "series": past}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--blocks", type=int, default=50)
    ap.add_argument("--watch", type=int, metavar="SECONDS")
    ap.add_argument("--rpc", default="https://ethereum-rpc.publicnode.com")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    while True:
        s = summarize(rpc(a.rpc, "eth_feeHistory", [hex(a.blocks), "latest", []]))
        if s is None:
            print("this chain returns no blob fee data")
            return
        wei = lambda v: f"{v:,.0f} wei" if v < 10**6 else f"{v / 1e9:,.4f} gwei"
        print(time.strftime("%H:%M:%S"),
              f"next blob base fee {wei(s['next'])}  (window min {wei(s['min'])}, avg {wei(s['avg'])}, max {wei(s['max'])})")
        print(f"         blob space used {s['util']:.1%} of max   1 blob = {s['next'] * BLOB_GAS / 1e18:.10f} ETH")
        print(f"         {sparkline(s['series'])}  (last {len(s['series'])} blocks)")
        if not a.watch:
            break
        time.sleep(a.watch)


if __name__ == "__main__":
    main()
