"""Tiny drawing language used to redraw the course schematics natively.

A redrawing is authored in PDF points, relative to the top-left corner of
the raster image it replaces (the same box as in the original page), so
that it can be compared pixel for pixel with the original.

    @figure("c038_3#0", drop=["Résistance R"])
    def chaleur(f):
        f.rect(20, 20, 60, 24)
        f.text(50, 36, "Résistance R", anchor="c")

The symbol helpers follow the conventions of the course (resistor = box,
capacitor = two plates, inductor = loops...).
"""
from __future__ import annotations

import math
import re

REGISTRY: dict[str, "Fig"] = {}

BLACK = "#000000"
RED = "#ff0000"
BLUE = "#000080"
GREY = "#808080"
LIGHT = "#c0c0c0"
PURPLE = "#800080"


_BOXES = None


def _box(key):
    """Size (pt) of the raster `key` in the original page."""
    global _BOXES
    if _BOXES is None:
        import json
        import os
        path = os.path.join(os.path.dirname(__file__), "build", "rasters.json")
        with open(path, encoding="utf-8") as fh:
            log = json.load(fh)
        _BOXES = {}
        for fid, e in log.items():
            for i, r in enumerate(e["rasters"]):
                _BOXES[f"{fid}#{i}"] = (r["box"][2], r["box"][3])
    return _BOXES[key]


def figure(key, drop=(), px=3.0):
    """Registers a redrawing.  Coordinates, line widths and font sizes are
    given in pixels of the 3x crop of the original raster (tools/raster_sheet.py
    crops), i.e. 1 pt = 3 units; they are scaled back to points on placement."""
    def deco(fn):
        bw, bh = _box(key)
        f = Fig(key, bw * px, bh * px)
        f.lw = 0.75 * px
        f.size = 9.0 * px
        f.u = px
        f.drop_texts = set(drop)
        fn(f)
        REGISTRY[key] = f
        return fn
    return deco


def empty(key):
    """A raster whose content is drawn by another redrawing."""
    f = Fig(key, 1, 1)
    REGISTRY[key] = f
    return f


def _r(v):
    return round(v, 2)


class Fig:
    def __init__(self, key, w=None, h=None):
        self.key = key
        self.w = w
        self.h = h
        self.ops: list[dict] = []
        self.top: list[dict] = []
        self.drop_texts: set[str] = set()
        self.lw = 0.75          # default line width
        self.font = "serif"
        self.size = 9.0
        self.u = 3.0            # crop pixels per point

    # -- placement --------------------------------------------------------
    def place(self, x, y, w, h):
        sx = (w / self.w) if self.w else 1.0
        sy = (h / self.h) if self.h else 1.0
        return [self._xf(op, x, y, sx, sy) for op in self.ops]

    def overlay(self, x, y, w, h):
        sx = (w / self.w) if self.w else 1.0
        sy = (h / self.h) if self.h else 1.0
        return [self._xf(op, x, y, sx, sy) for op in self.top]

    @property
    def W(self):
        return self.w

    @property
    def H(self):
        return self.h

    @staticmethod
    def _xf(op, x, y, sx, sy):
        op = dict(op)
        if "p" in op:
            toks = re.findall(r"[MLHVCQZ]|-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", op["p"])
            out = []
            cmd = None
            axis = 0
            for t in toks:
                if t.isalpha():
                    cmd = t
                    axis = 0
                    out.append(t)
                    continue
                v = float(t)
                if cmd == "H":
                    v = x + v * sx
                elif cmd == "V":
                    v = y + v * sy
                else:
                    v = (x + v * sx) if axis % 2 == 0 else (y + v * sy)
                    axis += 1
                if out and not out[-1].isalpha():
                    out.append(" ")
                out.append(str(_r(v)))
            op["p"] = "".join(out)
            if "w" in op:
                op["w"] = _r(op["w"] * min(sx, sy))
            if "d" in op:
                op["d"] = [_r(v * min(sx, sy)) for v in op["d"]]
        elif "t" in op or "R" in op:
            op["x"] = _r(x + op["x"] * sx)
            op["y"] = _r(y + op["y"] * sy)
            op["z"] = _r(op["z"] * min(sx, sy))
        elif "img" in op:
            op["x"] = _r(x + op["x"] * sx)
            op["y"] = _r(y + op["y"] * sy)
            op["w"] = _r(op["w"] * sx)
            op["h"] = _r(op["h"] * sy)
        return op

    # -- primitives -------------------------------------------------------
    def _style(self, op, stroke, fill, w, dash, cap, join, eo=False):
        if stroke:
            op["s"] = stroke
            op["w"] = _r(self.lw if w is None else w)
            if dash:
                op["d"] = list(dash)
            if cap:
                op["c"] = cap
            if join:
                op["j"] = join
        if fill:
            op["f"] = fill
            if eo:
                op["eo"] = 1
        return op

    def path(self, d, stroke=BLACK, fill=None, w=None, dash=None, cap="r", join="r", top=False, eo=False):
        op = self._style({"p": d}, stroke, fill, w, dash, cap, join, eo)
        (self.top if top else self.ops).append(op)
        return op

    def line(self, *pts, stroke=BLACK, w=None, dash=None, cap="r", top=False):
        pts = _flat(pts)
        d = "M%s %s" % (_r(pts[0][0]), _r(pts[0][1])) + "".join("L%s %s" % (_r(x), _r(y)) for x, y in pts[1:])
        return self.path(d, stroke=stroke, w=w, dash=dash, cap=cap, top=top)

    def poly(self, *pts, stroke=BLACK, fill=None, w=None, dash=None, top=False):
        pts = _flat(pts)
        d = "M%s %s" % (_r(pts[0][0]), _r(pts[0][1])) + "".join("L%s %s" % (_r(x), _r(y)) for x, y in pts[1:]) + "Z"
        return self.path(d, stroke=stroke, fill=fill, w=w, dash=dash, top=top)

    def rect(self, x, y, w, h, stroke=BLACK, fill=None, lw=None, dash=None, top=False):
        d = f"M{_r(x)} {_r(y)}H{_r(x + w)}V{_r(y + h)}H{_r(x)}Z"
        return self.path(d, stroke=stroke, fill=fill, w=lw, dash=dash, cap=None, join=None, top=top)

    def ellipse(self, cx, cy, rx, ry, stroke=BLACK, fill=None, lw=None, dash=None, top=False):
        k = 0.5522847498
        d = (f"M{_r(cx + rx)} {_r(cy)}"
             f"C{_r(cx + rx)} {_r(cy + k * ry)} {_r(cx + k * rx)} {_r(cy + ry)} {_r(cx)} {_r(cy + ry)}"
             f"C{_r(cx - k * rx)} {_r(cy + ry)} {_r(cx - rx)} {_r(cy + k * ry)} {_r(cx - rx)} {_r(cy)}"
             f"C{_r(cx - rx)} {_r(cy - k * ry)} {_r(cx - k * rx)} {_r(cy - ry)} {_r(cx)} {_r(cy - ry)}"
             f"C{_r(cx + k * rx)} {_r(cy - ry)} {_r(cx + rx)} {_r(cy - k * ry)} {_r(cx + rx)} {_r(cy)}Z")
        return self.path(d, stroke=stroke, fill=fill, w=lw, dash=dash, top=top)

    def circle(self, cx, cy, r, **kw):
        return self.ellipse(cx, cy, r, r, **kw)

    def arc(self, cx, cy, rx, ry, a0, a1, stroke=BLACK, w=None, dash=None, n=None, fill=None, close=False):
        """Elliptic arc, angles in degrees (0 = east, 90 = south, screen coordinates)."""
        n = n or max(8, int(abs(a1 - a0) / 6))
        pts = [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
        if close or fill:
            return self.poly(pts, stroke=stroke, fill=fill, w=w, dash=dash)
        return self.line(pts, stroke=stroke, w=w, dash=dash)

    def curve(self, fn, x0, x1, n=120, stroke=BLACK, w=None, dash=None, cap="r"):
        pts = [(x0 + (x1 - x0) * i / n, fn(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
        return self.line(pts, stroke=stroke, w=w, dash=dash, cap=cap)

    def pcurve(self, fn, t0, t1, n=120, stroke=BLACK, w=None, dash=None, fill=None):
        pts = [fn(t0 + (t1 - t0) * i / n) for i in range(n + 1)]
        if fill:
            return self.poly(pts, stroke=stroke, fill=fill, w=w, dash=dash)
        return self.line(pts, stroke=stroke, w=w, dash=dash)

    def text(self, x, y, s, size=None, family=None, bold=False, italic=False, color=BLACK,
             anchor="l", va="base", rot=0, underline=False, top=False):
        op = {"t": s, "x": _r(x), "y": _r(y), "z": _r(size or self.size)}
        fam = family or self.font
        if fam != "serif":
            op["F"] = fam
        if bold:
            op["b"] = 1
        if italic:
            op["i"] = 1
        if underline:
            op["u"] = 1
        if color and color != BLACK:
            op["s"] = color
        if rot:
            op["r"] = rot
        a = {"l": 0, "c": 1, "r": 2}[anchor]
        if a:
            op["a"] = a
        v = {"base": 0, "middle": 1, "top": 2}[va]
        if v:
            op["va"] = v
        (self.top if top else self.ops).append(op)
        return op

    def image(self, name, x, y, w, h):
        self.ops.append({"img": name, "x": _r(x), "y": _r(y), "w": _r(w), "h": _r(h)})

    # -- arrows -------------------------------------------------------------
    def head(self, x, y, angle, size=None, stroke=BLACK, filled=True, open_=False, w=None, top=False):
        """Arrow head with its tip at (x, y) pointing towards `angle` (deg)."""
        size = size or 4.0 * self.u
        a = math.radians(angle)
        half = math.radians(22)
        p1 = (x - size * math.cos(a - half), y - size * math.sin(a - half))
        p2 = (x - size * math.cos(a + half), y - size * math.sin(a + half))
        if open_:
            return self.line(p1, (x, y), p2, stroke=stroke, w=w, top=top)
        return self.poly(p1, (x, y), p2, stroke=stroke, fill=stroke if filled else None, w=w if w else 0.5, top=top)

    def arrow(self, x1, y1, x2, y2, stroke=BLACK, w=None, size=None, open_=False, both=False, dash=None, top=False):
        size = size or 4.0 * self.u
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        back = 0 if open_ else size * 0.6
        ex = x2 - back * math.cos(math.radians(ang))
        ey = y2 - back * math.sin(math.radians(ang))
        sx, sy = x1, y1
        if both:
            sx = x1 + back * math.cos(math.radians(ang))
            sy = y1 + back * math.sin(math.radians(ang))
        self.line((sx, sy), (ex, ey), stroke=stroke, w=w, dash=dash, top=top)
        self.head(x2, y2, ang, size, stroke, open_=open_, w=w, top=top)
        if both:
            self.head(x1, y1, ang + 180, size, stroke, open_=open_, w=w, top=top)

    # -- electronic symbols ------------------------------------------------
    def resistor(self, x1, y1, x2, y2, length=None, width=None, label=None, size=None, fill=None, lw=None,
                 label_pos="in", **tk):
        """Rectangle resistor between two points (leads included)."""
        ux, uy, L = _unit(x1, y1, x2, y2)
        width = width or 7.0 * self.u
        length = length or min(L * 0.6, 26 * self.u)
        a = (L - length) / 2
        p1 = (x1 + ux * a, y1 + uy * a)
        p2 = (x1 + ux * (L - a), y1 + uy * (L - a))
        self.line((x1, y1), p1, w=lw)
        self.line(p2, (x2, y2), w=lw)
        nx, ny = -uy, ux
        hw = width / 2
        pts = [(p1[0] + nx * hw, p1[1] + ny * hw), (p2[0] + nx * hw, p2[1] + ny * hw),
               (p2[0] - nx * hw, p2[1] - ny * hw), (p1[0] - nx * hw, p1[1] - ny * hw)]
        self.poly(pts, fill=fill, w=lw)
        if label:
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            sz = size or self.size
            if label_pos == "in":
                if abs(ux) >= abs(uy):
                    self.text(cx, cy, label, size=sz, anchor="c", va="middle", **tk)
                else:
                    self.text(cx, cy, label, size=sz, anchor="c", va="middle", rot=-90, **tk)
            else:
                dx, dy = label_pos
                self.text(cx + dx, cy + dy, label, size=sz, **tk)

    def capacitor(self, x1, y1, x2, y2, gap=None, plate=None, lw=None, plate_w=None, polar=False, variable=False):
        gap = gap or 3.0 * self.u
        plate = plate or 10.0 * self.u
        ux, uy, L = _unit(x1, y1, x2, y2)
        a = (L - gap) / 2
        p1 = (x1 + ux * a, y1 + uy * a)
        p2 = (x1 + ux * (L - a), y1 + uy * (L - a))
        self.line((x1, y1), p1, w=lw)
        self.line(p2, (x2, y2), w=lw)
        nx, ny = -uy, ux
        h = plate / 2
        pw = plate_w or max(1.0, (lw or self.lw) * 1.6)
        self.line((p1[0] + nx * h, p1[1] + ny * h), (p1[0] - nx * h, p1[1] - ny * h), w=pw, cap=None)
        if polar:
            # curved (negative) plate
            self.line((p2[0] + nx * h, p2[1] + ny * h), (p2[0] - nx * h, p2[1] - ny * h), w=pw * 2.2, cap=None)
        else:
            self.line((p2[0] + nx * h, p2[1] + ny * h), (p2[0] - nx * h, p2[1] - ny * h), w=pw, cap=None)
        if variable:
            cx, cy = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            k = 8 * self.u
            self.arrow(cx - k, cy + k, cx + k, cy - k, size=3 * self.u)

    def inductor(self, x1, y1, x2, y2, turns=4, length=None, height=None, lw=None, side=1, core=False):
        """Coil drawn as half-loops ("ꟷmmmꟷ") between two points."""
        ux, uy, L = _unit(x1, y1, x2, y2)
        height = height or 5.0 * self.u
        length = length or min(L * 0.7, turns * 7 * self.u)
        a = (L - length) / 2
        p1 = (x1 + ux * a, y1 + uy * a)
        self.line((x1, y1), p1, w=lw)
        self.line((x1 + ux * (L - a), y1 + uy * (L - a)), (x2, y2), w=lw)
        nx, ny = -uy * side, ux * side
        step = length / turns
        pts = []
        for t in range(turns):
            for i in range(13):
                ang = math.pi * i / 12
                along = t * step + step / 2 - math.cos(ang) * step / 2
                out = math.sin(ang) * height
                pts.append((p1[0] + ux * along - nx * out, p1[1] + uy * along - ny * out))
        self.line(pts, w=lw)
        if core:
            for k in (1.8 * self.u + height, 3.0 * self.u + height):
                self.line((p1[0] + nx * k, p1[1] + ny * k),
                          (p1[0] + ux * length + nx * k, p1[1] + uy * length + ny * k), w=lw)

    def coil_loops(self, x1, y1, x2, y2, turns=4, radius=4.0, lw=None, side=1):
        """Coil drawn as overlapping loops (as in transformers)."""
        ux, uy, L = _unit(x1, y1, x2, y2)
        nx, ny = -uy * side, ux * side
        step = L / (turns + 0.4)
        pts = []
        n = 24
        for i in range(turns * n + 1):
            t = i / n
            ang = 2 * math.pi * t
            along = step * 0.2 + step * t + radius * 0.55 * (1 - math.cos(ang)) * 0 + step * 0.5 * math.sin(ang) * 0
            along = step * (t + 0.2) - radius * 0.9 * math.sin(ang)
            out = radius * (1 - math.cos(ang)) * 0.5 * 2
            pts.append((x1 + ux * along - nx * out, y1 + uy * along - ny * out))
        self.line(pts, w=lw)

    def diode(self, x1, y1, x2, y2, size=None, lw=None, fill=BLACK, zener=False, bar=True):
        """Diode pointing from (x1,y1) [anode] to (x2,y2) [cathode]."""
        size = size or 8.0 * self.u
        ux, uy, L = _unit(x1, y1, x2, y2)
        a = (L - size) / 2
        p1 = (x1 + ux * a, y1 + uy * a)
        p2 = (x1 + ux * (L - a), y1 + uy * (L - a))
        self.line((x1, y1), p1, w=lw)
        self.line(p2, (x2, y2), w=lw)
        nx, ny = -uy, ux
        h = size * 0.55
        self.poly((p1[0] + nx * h, p1[1] + ny * h), (p1[0] - nx * h, p1[1] - ny * h), p2, fill=fill, w=lw)
        if bar:
            self.line((p2[0] + nx * h, p2[1] + ny * h), (p2[0] - nx * h, p2[1] - ny * h), w=(lw or self.lw) * 1.4, cap=None)
            if zener:
                self.line((p2[0] + nx * h, p2[1] + ny * h), (p2[0] + nx * h - ux * 2.5 * self.u, p2[1] + ny * h - uy * 2.5 * self.u), w=lw)
                self.line((p2[0] - nx * h, p2[1] - ny * h), (p2[0] - nx * h + ux * 2.5 * self.u, p2[1] - ny * h + uy * 2.5 * self.u), w=lw)

    def ground(self, x, y, width=None, kind="bar", lw=None, rot=0):
        """Ground symbol whose connection point is (x, y), pointing down."""
        width = width or 10.0 * self.u
        if kind == "bar":
            self.rect(x - width / 2, y, width, width * 0.28, fill=BLACK, stroke=None)
        elif kind == "lines":
            for i, k in enumerate((1.0, 0.65, 0.3)):
                yy = y + i * 2.2 * self.u
                self.line((x - width / 2 * k, yy), (x + width / 2 * k, yy), w=lw)
        elif kind == "chassis":
            self.line((x - width / 2, y), (x + width / 2, y), w=lw)
            for i in range(4):
                xx = x - width / 2 + i * width / 3
                self.line((xx, y), (xx - 2.5 * self.u, y + 3.5 * self.u), w=lw)

    def antenna(self, x, y, h=None, spread=None, lw=None):
        """Antenna symbol (Y shape) with its foot at (x, y)."""
        h = h or 14.0 * self.u
        spread = spread or 5.0 * self.u
        self.line((x, y), (x, y - h), w=lw)
        self.line((x - spread, y - h - spread * 0.9), (x, y - h * 0.62), (x + spread, y - h - spread * 0.9), w=lw)
        self.line((x, y - h), (x, y - h - spread * 0.9), w=lw)

    def battery(self, x1, y1, x2, y2, gap=None, long_=None, short=None, lw=None, thick=None):
        """Cell between two points: long thin plate (+) on the (x1,y1) side."""
        gap = gap or 3.0 * self.u
        long_ = long_ or 12.0 * self.u
        short = short or 6.0 * self.u
        thick = thick or 2.4 * self.u
        ux, uy, L = _unit(x1, y1, x2, y2)
        a = (L - gap) / 2
        p1 = (x1 + ux * a, y1 + uy * a)
        p2 = (x1 + ux * (L - a), y1 + uy * (L - a))
        self.line((x1, y1), p1, w=lw)
        self.line(p2, (x2, y2), w=lw)
        nx, ny = -uy, ux
        self.line((p1[0] + nx * long_ / 2, p1[1] + ny * long_ / 2), (p1[0] - nx * long_ / 2, p1[1] - ny * long_ / 2), w=lw, cap=None)
        self.line((p2[0] + nx * short / 2, p2[1] + ny * short / 2), (p2[0] - nx * short / 2, p2[1] - ny * short / 2), w=thick, cap=None)

    def meter(self, cx, cy, r, label, size=None, lw=None, **tk):
        self.circle(cx, cy, r, lw=lw)
        self.text(cx, cy, label, size=size or r * 1.1, anchor="c", va="middle", **tk)

    def lamp(self, cx, cy, r, lw=None, cross=True):
        self.circle(cx, cy, r, lw=lw)
        if cross:
            d = r * 0.7071
            self.line((cx - d, cy - d), (cx + d, cy + d), w=lw)
            self.line((cx - d, cy + d), (cx + d, cy - d), w=lw)

    def block(self, x, y, w, h, label=None, size=None, lw=None, fill=None, **tk):
        self.rect(x, y, w, h, lw=lw, fill=fill)
        if label:
            lines = label.split("\n")
            sz = size or self.size
            n = len(lines)
            for i, ln in enumerate(lines):
                yy = y + h / 2 + (i - (n - 1) / 2) * sz * 1.15
                self.text(x + w / 2, yy, ln, size=sz, anchor="c", va="middle", **tk)

    def triangle_amp(self, x, y, w, h, label=None, size=None, lw=None, fill=None, **tk):
        """Amplifier triangle pointing right; (x, y) = top-left of its box."""
        self.poly((x, y), (x + w, y + h / 2), (x, y + h), lw=lw, fill=fill)
        if label:
            self.text(x + w * 0.38, y + h / 2, label, size=size or self.size, anchor="c", va="middle", **tk)

    def speaker(self, x, y, h=None, lw=None):
        """Loudspeaker connected at its left side (x, y = centre)."""
        h = h or 12.0 * self.u
        self.rect(x, y - h * 0.22, h * 0.25, h * 0.44, fill=BLACK, stroke=None)
        self.poly((x + h * 0.25, y - h * 0.22), (x + h * 0.6, y - h * 0.5), (x + h * 0.6, y + h * 0.5),
                  (x + h * 0.25, y + h * 0.22), w=lw)

    def transistor(self, cx, cy, r=None, kind="npn", lw=None, facing=1, circle=True, lead=None):
        """Bipolar transistor; base on the left (facing=1) or right (-1).
        Returns the base, collector and emitter connection points."""
        r = r or 10.0 * self.u
        if circle:
            self.circle(cx, cy, r, lw=lw)
        f = facing
        bx = cx - f * r * 0.35
        self.line((bx, cy - r * 0.5), (bx, cy + r * 0.5), w=(lw or self.lw) * 2.2, cap=None)
        lead = lead or r * 1.0
        base = (cx - f * (r + lead * 0.4), cy)
        self.line(base, (bx, cy), w=lw)
        c_end = (cx + f * r * 0.45, cy - r * 0.85)
        e_end = (cx + f * r * 0.45, cy + r * 0.85)
        self.line((bx, cy - r * 0.22), c_end, w=lw)
        self.line((bx, cy + r * 0.22), e_end, w=lw)
        if kind == "npn":
            ang = math.degrees(math.atan2(e_end[1] - (cy + r * 0.22), e_end[0] - bx))
            mx = bx + (e_end[0] - bx) * 0.8
            my = cy + r * 0.22 + (e_end[1] - cy - r * 0.22) * 0.8
            self.head(mx, my, ang, size=r * 0.42, w=lw)
        else:
            ang = math.degrees(math.atan2((cy + r * 0.22) - e_end[1], bx - e_end[0]))
            mx = bx + (e_end[0] - bx) * 0.3
            my = cy + r * 0.22 + (e_end[1] - cy - r * 0.22) * 0.3
            self.head(mx, my, ang, size=r * 0.42, w=lw)
        return base, (c_end[0], cy - r * 1.4), (e_end[0], cy + r * 1.4)

    def sine(self, x0, x1, yc, amp, periods, phase=0.0, stroke=RED, w=None, n=None, dash=None):
        n = n or int(60 * max(1, periods))
        return self.curve(lambda x: yc - amp * math.sin(phase + 2 * math.pi * periods * (x - x0) / (x1 - x0)),
                          x0, x1, n=n, stroke=stroke, w=w, dash=dash)

    def axes(self, x0, y0, x1, y1, origin=None, stroke=BLACK, w=None, size=None, xlabel=None, ylabel=None,
             label_size=None, **tk):
        """Axes with arrows: horizontal from x0 to x1 at origin y, vertical
        from y0 (bottom) to y1 (top) at origin x."""
        ox, oy = origin if origin else (x0, y0)
        self.arrow(x0, oy, x1, oy, stroke=stroke, w=w, size=size)
        self.arrow(ox, y0, ox, y1, stroke=stroke, w=w, size=size)
        if xlabel:
            self.text(x1 + 2 * self.u, oy + 3 * self.u, xlabel, size=label_size, **tk)
        if ylabel:
            self.text(ox + 3 * self.u, y1 + 2 * self.u, ylabel, size=label_size, va="top", **tk)

    def dot(self, x, y, r=None, fill=BLACK):
        self.circle(x, y, r or 1.4 * self.u, stroke=None, fill=fill)


def _flat(pts):
    if len(pts) == 1 and isinstance(pts[0], (list, tuple)) and pts[0] and isinstance(pts[0][0], (list, tuple)):
        return list(pts[0])
    return list(pts)


def _unit(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1.0
    return dx / L, dy / L, L


# ---------------------------------------------------------------------------
# Text measurement (same Liberation fonts as the application)
# ---------------------------------------------------------------------------

_FONT_FILES = {
    ("serif", False, False): "LiberationSerif-Regular.ttf",
    ("serif", True, False): "LiberationSerif-Bold.ttf",
    ("serif", False, True): "LiberationSerif-Italic.ttf",
    ("serif", True, True): "LiberationSerif-BoldItalic.ttf",
    ("sans", False, False): "LiberationSans-Regular.ttf",
    ("sans", True, False): "LiberationSans-Bold.ttf",
    ("sans", False, True): "LiberationSans-Italic.ttf",
    ("sans", True, True): "LiberationSans-BoldItalic.ttf",
}
_FONT_CACHE = {}


def text_width(s, size, family="serif", bold=False, italic=False):
    import os
    from PIL import ImageFont
    key = (family, bool(bold), bool(italic), round(size * 4))
    font = _FONT_CACHE.get(key)
    if font is None:
        path = os.path.join(os.path.dirname(__file__), "..", "fonts", _FONT_FILES[(family, bool(bold), bool(italic))])
        font = ImageFont.truetype(path, max(1, int(round(size * 4))))
        _FONT_CACHE[key] = font
    total = 0.0
    for part, level in _runs(s):
        w = font.getlength(part) / 4.0
        total += w * (0.7 if level else 1.0)
    return total


def _runs(s):
    out = []
    buf = ""
    i = 0
    while i < len(s):
        c = s[i]
        if c in "_^" and i + 1 < len(s) and s[i + 1] == "{":
            j = s.find("}", i + 2)
            if j > 0:
                if buf:
                    out.append((buf, 0))
                    buf = ""
                out.append((s[i + 2:j], 1))
                i = j + 1
                continue
        buf += c
        i += 1
    if buf:
        out.append((buf, 0))
    return out


def _rich(self, x, y, parts, size=None, family=None, anchor="l", color=BLACK, top=False, **common):
    """Line made of several styled parts laid out by the renderer:
    parts = [(text, {"b":1, "i":1, "u":1, "color": ..}), ...] or plain strings."""
    size = size or self.size
    fam = family or self.font
    runs = []
    for p in parts:
        t, st = (p, {}) if isinstance(p, str) else p
        r = {"t": t}
        for k in ("b", "i", "u"):
            if st.get(k):
                r[k] = 1
        c = st.get("color", color)
        if c and c != BLACK:
            r["s"] = c
        runs.append(r)
    op = {"R": runs, "x": _r(x), "y": _r(y), "z": _r(size)}
    if fam != "serif":
        op["F"] = fam
    a = {"l": 0, "c": 1, "r": 2}[anchor]
    if a:
        op["a"] = a
    if common.get("rot"):
        op["r"] = common["rot"]
    (self.top if top else self.ops).append(op)
    return op


Fig.rich = _rich


def _spline(self, pts, n=12, stroke=BLACK, w=None, dash=None, closed=False, fill=None, cap="r"):
    """Smooth curve through the points (Catmull-Rom)."""
    P = list(pts)
    if closed:
        P = [P[-1]] + P + [P[0], P[1]]
    else:
        P = [P[0]] + P + [P[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(P[-2])
    if closed or fill:
        return self.poly(out, stroke=stroke, fill=fill, w=w, dash=dash)
    return self.line(out, stroke=stroke, w=w, dash=dash, cap=cap)


Fig.spline = _spline


def _fit(self, x0, x1, y, s, family=None, bold=False, italic=False, max_size=None, **kw):
    """Text whose ink spans x0..x1 (as measured on the original): the font
    size is derived from the measured width."""
    fam = family or self.font
    w1 = text_width(s, 10.0, fam, bold, italic)
    size = 10.0 * (x1 - x0) / w1 if w1 else self.size
    if max_size:
        size = min(size, max_size)
    return self.text(x0, y, s, size=size, family=fam, bold=bold, italic=italic, **kw)


Fig.fit = _fit
