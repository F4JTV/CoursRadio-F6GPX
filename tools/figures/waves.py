"""Oscillogram helpers shared by the modulation figures."""
import math

from figdsl import BLACK, LIGHT


def am(f, x0, x1, yc, amp, periods=12, env_periods=2.0, depth=0.55, phase=0.6, grey=True, stroke=BLACK, w=None):
    def env(x):
        t = (x - x0) / (x1 - x0)
        return amp * (1 - depth * 0.5 + depth * 0.5 * math.sin(2 * math.pi * env_periods * t + phase))
    if grey:
        n = 80
        top = [(x0 + (x1 - x0) * i / n, yc - env(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
        bot = [(x, yc + (yc - y)) for x, y in reversed(top)]
        f.poly(top + bot, stroke=None, fill=LIGHT)
    f.curve(lambda x: yc - env(x) * math.sin(2 * math.pi * periods * (x - x0) / (x1 - x0)), x0, x1,
            n=periods * 24, stroke=stroke, w=w)


def burst(f, x0, x1, yc, amp, periods, grey=True, stroke=BLACK, w=None):
    """Constant-amplitude carrier between x0 and x1 (CW element)."""
    if grey:
        f.rect(x0, yc - amp, x1 - x0, 2 * amp, stroke=None, fill=LIGHT)
    f.curve(lambda x: yc - amp * math.sin(2 * math.pi * periods * (x - x0) / (x1 - x0)), x0, x1,
            n=max(24, int(periods * 24)), stroke=stroke, w=w)


def fm(f, x0, x1, yc, amp, periods=9, dev=0.35, grey=True, stroke=BLACK, w=None):
    if grey:
        f.rect(x0, yc - amp, x1 - x0, 2 * amp, stroke=None, fill=LIGHT)
    L = x1 - x0

    def y(x):
        t = (x - x0) / L
        phase = 2 * math.pi * periods * t + dev * periods * math.sin(2 * math.pi * 1.5 * t) / 1.5
        return yc - amp * math.sin(phase)
    f.curve(y, x0, x1, n=periods * 30, stroke=stroke, w=w)


def ssb(f, x0, x1, yc, amp, blobs, stroke=BLACK, w=None):
    """BLU: bursts whose amplitude follows the voice (list of (centre, width, height))."""
    def env(x):
        v = 0.06 * amp
        for c, wd, h in blobs:
            v = max(v, h * math.exp(-((x - c) / (wd / 2.2)) ** 2))
        return v
    n = 120
    top = [(x0 + (x1 - x0) * i / n, yc - env(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
    bot = [(x, yc + (yc - y)) for x, y in reversed(top)]
    f.poly(top + bot, stroke=None, fill=LIGHT)
    periods = (x1 - x0) / 14.0
    f.curve(lambda x: yc - env(x) * math.sin(2 * math.pi * periods * (x - x0) / (x1 - x0)), x0, x1,
            n=int(periods * 24), stroke=stroke, w=w)
