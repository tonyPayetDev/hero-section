#!/usr/bin/env python3
"""Light beat-grid analysis (numpy only): onset envelope -> tempo (autocorr + fine comb),
phase, downbeat phase (low-band energy on beats), per-bar RMS and energy jumps (drops)."""
import sys, json, os
import numpy as np

SR = 16000
HOP = 160          # 100 fps
NFFT = 1024
FPS = SR / HOP


def load(path):
    return np.fromfile(path, dtype=np.float32)


def stft_mag(x):
    n = 1 + (len(x) - NFFT) // HOP
    idx = np.arange(NFFT)[None, :] + HOP * np.arange(n)[:, None]
    win = np.hanning(NFFT).astype(np.float32)
    out = np.empty((n, NFFT // 2 + 1), dtype=np.float32)
    for a in range(0, n, 2000):  # chunked to keep memory small
        out[a:a + 2000] = np.abs(np.fft.rfft(x[idx[a:a + 2000]] * win, axis=1))
    return out


def analyse(path, bpm_lo=70, bpm_hi=180, meter=4):
    x = load(path)
    dur = len(x) / SR
    M = stft_mag(x)
    L = np.log1p(100 * M)
    flux = np.maximum(0, np.diff(L, axis=0)).sum(1)
    flux = np.concatenate([[0], flux])
    # low band (< 150 Hz) energy for kick / downbeat
    fb = np.fft.rfftfreq(NFFT, 1 / SR)
    low = M[:, fb < 150].sum(1)
    lowflux = np.concatenate([[0], np.maximum(0, np.diff(np.log1p(100 * low)))])
    # normalise onset envelope (remove local mean)
    k = int(FPS * 0.5)
    env = flux - np.convolve(flux, np.ones(k) / k, mode="same")
    env = np.maximum(env, 0)
    env /= env.max() + 1e-9
    # autocorrelation tempo
    e = env - env.mean()
    ac = np.correlate(e, e, mode="full")[len(e) - 1:]
    lags = np.arange(len(ac))
    lo, hi = int(FPS * 60 / bpm_hi), int(FPS * 60 / bpm_lo)
    # weight towards 120 bpm (log-gaussian) to fight octave errors
    bpms = 60 * FPS / np.maximum(lags[lo:hi], 1)
    w = np.exp(-0.5 * (np.log2(bpms / 120) / 0.9) ** 2)
    lag = lo + int(np.argmax(ac[lo:hi] * w))
    # fine tempo + phase by comb over interpolated envelope
    t_env = np.arange(len(env)) / FPS + (NFFT / 2) / SR  # frame centre
    best = None
    for period in np.linspace(lag / FPS * 0.985, lag / FPS * 1.015, 301):
        nb = int((dur - 1) / period)
        for ph in np.arange(0, period, 0.005):
            tb = ph + period * np.arange(nb)
            tb = tb[tb < t_env[-1]]
            s = np.interp(tb, t_env, env).mean()
            if best is None or s > best[0]:
                best = (s, period, ph)
    _, period, ph = best
    bpm = 60 / period
    beats = ph + period * np.arange(int((dur - ph) / period) + 1)
    beats = beats[beats < dur]
    # downbeat phase: which beat mod meter carries most low-band onset energy
    lf = lowflux / (lowflux.max() + 1e-9)
    scores = []
    for m in range(meter):
        tb = beats[m::meter]
        scores.append(float(np.interp(tb, t_env, lf).mean()))
    m0 = int(np.argmax(scores))
    downbeats = beats[m0::meter]
    # per-bar RMS (dB)
    rms = np.sqrt(np.convolve(x.astype(np.float64) ** 2, np.ones(HOP) / HOP, mode="same")[::HOP] + 1e-12)
    t_r = np.arange(len(rms)) / FPS
    bars = []
    for i, d in enumerate(downbeats):
        e_ = downbeats[i + 1] if i + 1 < len(downbeats) else dur
        sel = (t_r >= d) & (t_r < e_)
        lsel = (t_env >= d) & (t_env < e_)
        db = 20 * np.log10(rms[sel].mean() + 1e-9) if sel.any() else -120
        ldb = 20 * np.log10(low[lsel].mean() + 1e-9) if lsel.any() else -120
        bars.append((round(float(d), 3), round(float(db), 1), round(float(ldb), 1)))
    # jumps: bar RMS rise >= 3 dB vs mean of previous 2 bars, or low band rise >= 6 dB
    jumps = []
    for i in range(2, len(bars)):
        prev = np.mean([bars[i - 1][1], bars[i - 2][1]])
        prevl = np.mean([bars[i - 1][2], bars[i - 2][2]])
        if bars[i][1] - prev >= 3 or bars[i][2] - prevl >= 6:
            jumps.append((bars[i][0], round(bars[i][1] - prev, 1), round(bars[i][2] - prevl, 1)))
    return {
        "file": os.path.basename(path), "duration": round(dur, 3), "bpm": round(bpm, 3),
        "beat_period": round(period, 5), "first_beat": round(float(beats[0]), 3),
        "meter": meter, "downbeat_offset_beats": m0, "first_downbeat": round(float(downbeats[0]), 3),
        "bar_len": round(period * meter, 4), "downbeat_scores": [round(s, 3) for s in scores],
        "comb_strength": round(float(best[0]), 3),
        "bars_db": bars, "jumps": jumps,
    }


if __name__ == "__main__":
    path = sys.argv[1]
    meter = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    lo = float(sys.argv[3]) if len(sys.argv) > 3 else 70
    hi = float(sys.argv[4]) if len(sys.argv) > 4 else 180
    r = analyse(path, lo, hi, meter)
    out = os.path.splitext(path)[0] + ".grid.json"
    json.dump(r, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in r.items() if k not in ("bars_db",)}, ensure_ascii=False))
