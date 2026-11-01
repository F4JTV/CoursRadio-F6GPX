"""Chapter 1 (Ohm and Joule) figures."""
import math

from figdsl import BLACK, RED, figure

BLUE = "#0000ff"
NAVY = "#000080"
GREY = "#a6a6a6"
S = 31


@figure("c038_1#0")
def douze_formules(f):
    for y in (1, 39, 186):
        f.line((1, y), (1377, y), w=2)
    for x in (1, 139, 449, 759, 1067, 1377):
        f.line((x, 1), (x, 186), w=2)
    cx = [70, 294, 604, 913, 1222]
    base = [32, 69, 105, 141, 177]
    for x, s in zip(cx, ["Données", "P en watts", "U en volts", "I en ampères", "R en ohms"]):
        f.text(x, base[0], s, size=S, anchor="c")
    for y, s in zip(base[1:], ["P (W)", "U (V)", "I (A)", "R (Ω)"]):
        f.text(cx[0], y, s, size=S, anchor="c")
    cells = {
        (2, 1): ("R = U² / P", 0), (3, 1): ("R = P / I²", 0), (4, 1): ("I = √(P / R)", 0),
        (1, 2): ("I = P / U", 0), (3, 2): ("R = U / I", 0), (4, 2): ("P = U² / R", 1),
        (1, 3): ("U = P / I", 0), (2, 3): ("P = U . I", 1), (4, 3): ("P = R . I²", 1),
        (1, 4): ("U = √(P . R)", 0), (2, 4): ("I = U / R", 0), (3, 4): ("U = R . I", 1),
    }
    for (c, r), (s, bold) in cells.items():
        if bold:
            f.text(cx[c], base[r], s, size=S, bold=True, color=NAVY, anchor="c")
        else:
            f.text(cx[c], base[r], s, size=S, anchor="c")


@figure("c038_2#0")
def triangles(f):
    tri = [(6, 167, 86, 6, [("U", 86, 60), ("R", 58, 115), ("I", 118, 115)]),
           (328, 489, 408, 1, [("P", 408, 54), ("U", 380, 110), ("I", 440, 110)]),
           (651, 812, 731, 1, [("U²", 731, 60), ("P", 700, 115), ("R", 762, 115)]),
           (1000, 1161, 1080, 6, [("P", 1080, 54), ("R", 1048, 110), ("I²", 1112, 110)])]
    for x0, x1, xa, ya, labels in tri:
        f.poly((xa, ya), (x1, 140.5), (x0, 140.5), stroke=BLUE, w=3)
        for s, x, y in labels:
            f.text(x, y, s, size=S, anchor="c")


@figure("c038_3#0")
def resistance_chaleur(f):
    for i in range(7):
        x0 = 152 + i * 23
        pts = [(x0 + 5 * math.sin(t / 7.0 * 2 * math.pi), 2 + t) for t in range(0, 64, 2)]
        f.line(pts, stroke=GREY, w=1.6)
    f.text(112, 43, "Chaleur dégagée = Puissance P_{R}", size=S)
    f.rect(93, 83.5, 239, 83.5, stroke="#595959", lw=2.2)
    f.text(212, 135, "Résistance R", size=28, family="sans", anchor="c")
    f.line((12, 136), (93, 136), stroke="#808080", w=2.2)
    f.line((332, 135.5), (491, 135.5), w=2.6)
    f.line((390, 123), (406, 135.5), (390, 148), stroke=BLUE, w=2.4)
    f.text(335, 112, "Intensité I_{B}", size=S)
    f.text(18, 123, "+", size=40, color=RED)
    f.line((494, 141.5), (514, 141.5), stroke=RED, w=2.4)
    f.text(74, 170, "A", size=S, color=RED, anchor="c")
    f.text(363, 170, "B", size=S, color=RED, anchor="c")
    f.arrow(359, 193.5, 62, 193.5, stroke=BLUE, w=2.6, size=18)
    f.text(149, 222, "Tension U_{AB}", size=S)


@figure("c039_2#0")
def exemple_p(f):
    f.text(130, 30, "P = ?", size=30, family="sans", bold=True, anchor="c")
    f.rect(60.5, 67.5, 107, 43, lw=2.4)
    f.text(114, 100, "R = ?", size=30, family="sans", bold=True, anchor="c")
    f.line((0, 89.5), (61, 89.5), w=2)
    f.line((167, 88.5), (274, 88.5), w=2.4)
    f.text(187, 66, "0,05 A", size=30, family="sans")
    f.line((198, 72), (227, 88), (199, 104), stroke=BLUE, w=2.4)
    f.arrow(188, 132.5, 42, 132.5, stroke=BLUE, w=2.6, size=16)
    f.text(75, 176, "2 V", size=30, family="sans")


@figure("c039_3#0")
def exemple_q(f):
    f.rect(113, 5, 83, 41, lw=2.2)
    f.text(155, 36, "5 Ω", size=30, anchor="c")
    f.line((32, 26.5), (113, 26.5), w=2)
    f.line((196, 27), (298, 27), w=2)
    f.arrow(216, 68.5, 94, 68.5, stroke=BLUE, w=2.6, size=16)
    f.text(119, 96, "10 V", size=30, family="sans")
    f.text(11, 129, "Temps (t) = 30 secondes", size=26, family="sans")


def _triangle(f, x0, x1, xa, ya, yb, circle, labels):
    cx, cy, r = circle
    f.circle(cx, cy, r, stroke=None, fill="#c8c8c8")
    f.poly((xa, ya), (x1, yb), (x0, yb), stroke=BLUE, w=3)
    for s, x, y in labels:
        f.text(x, y, s, size=26, family="sans", anchor="c")


@figure("c039_4#0")
def triangle_p(f):
    _triangle(f, 6, 156, 81, 11, 136.5, (92, 52, 37), [("P", 81, 64), ("R", 50, 128), ("I²", 110, 128)])


@figure("c039_4#1")
def triangle_r(f):
    _triangle(f, 5, 154, 79, 4, 127, (44, 102, 37), [("P", 79, 48), ("R", 48, 112), ("I²", 108, 112)])


@figure("c040_2#0")
def code_couleur(f):
    f.line((0, 29), (65, 29), w=2.4)
    f.line((220, 28.5), (262, 28.5), w=2.4)
    f.rect(65.5, 7, 154, 44, fill="#c0c0c0", lw=2.6)
    for x0, x1, col in ((81, 95, "#0000ff"), (103, 116, "#ff0000"), (124, 137, "#993300")):
        f.rect(x0, 8.5, x1 - x0, 41, stroke=None, fill=col)
    for x, s in ((101, "Bleu"), (122, "Rouge"), (143, "Marron")):
        f.text(x, 58, s, size=23, family="sans", rot=-90, anchor="r")


def chevron(f, x, y, size=14, color=BLUE, w=2.4, back=None, line_from=None):
    """Open arrow head ">" with its tip at (x, y), optionally with a line."""
    if line_from is not None:
        f.line((line_from, y), (x, y), stroke=color, w=w)
    f.line((x - size * 1.8, y - size), (x, y), (x - size * 1.8, y + size), stroke=color, w=w)


@figure("c041_1#0")
def potentiometres(f):
    lw = 3
    # Montage 1: rheostat
    f.rect(56.5, 73.5, 104, 52, lw=lw)
    f.line((6, 99.5), (56.5, 99.5), w=lw)
    f.line((160.5, 99.5), (238, 99.5), w=lw)
    f.line((108.5, 33), (212.5, 33), (212.5, 99.5), w=lw)
    f.line((108.5, 33), (108.5, 58), w=lw)
    f.poly((100, 56), (117, 56), (108.5, 73), stroke=None, fill=BLACK)
    f.text(26, 88, "E", size=28, italic=True, color=RED)
    f.text(233, 88, "S", size=28, italic=True, color=RED)
    f.text(26, 161, "Montage 1", size=28, italic=True)
    # Montage 2: potentiometer
    f.rect(281.5, 44.5, 52, 78, lw=lw)
    f.line((307.5, 28), (307.5, 44.5), w=lw)
    f.line((307.5, 122.5), (307.5, 151), w=lw)
    f.rect(282, 150, 51, 8, stroke=None, fill=BLACK)
    f.line((410, 86.5), (350, 86.5), w=lw)
    f.poly((352, 78), (352, 95), (334, 86.5), stroke=None, fill=BLACK)
    f.text(298, 24, "E", size=28, italic=True, color=RED)
    f.text(380, 74, "S", size=28, italic=True, color=RED)
    f.text(340, 156, "Montage 2", size=28, italic=True)


@figure("c041_2#0")
def exemple_r220(f):
    f.rect(37.5, 7.5, 147, 55, lw=3)
    f.line((13, 38.5), (37.5, 38.5), w=2)
    f.line((184.5, 38.5), (208, 38.5), w=2)
    f.text(111, 49, "R = 220Ω", size=30, anchor="c")
    f.arrow(197, 70.5, 7, 70.5, stroke=BLUE, w=2.6, size=16)
    f.text(111, 100, "6 V", size=30, anchor="c")


@figure("c042_1#0")
def serie(f):
    lw = 3
    f.rect(48.5, 59.5, 96, 38, lw=lw)
    f.rect(263.5, 59.5, 96, 38, lw=lw)
    f.line((7, 81), (48.5, 81), w=lw)
    f.line((144.5, 82), (263.5, 82), w=lw)
    f.line((359.5, 83), (470, 83), w=lw)
    f.text(96, 90, "R1", size=28, anchor="c")
    f.text(311, 90, "R2", size=28, anchor="c")
    f.arrow(172, 30, 40, 30, stroke=BLUE, w=2.4, size=14)
    f.arrow(383, 30, 251, 30, stroke=BLUE, w=2.4, size=14)
    f.text(80, 22, "U_{R1}", size=28)
    f.text(291, 22, "U_{R2}", size=28)
    chevron(f, 212, 81.5, size=13, line_from=157)
    chevron(f, 450, 83, size=13, line_from=400)
    f.text(195, 61, "I_{R1}", size=28)
    f.text(406, 61, "I_{R2}", size=28)
    f.arrow(383, 145.5, 40, 145.5, stroke=BLUE, w=2.6, size=16)
    f.text(195, 177, "U_{t}", size=28)


@figure("c042_1#1")
def parallele(f):
    lw = 3
    f.rect(170, 10.5, 87, 44, lw=lw)
    f.rect(170, 119.5, 87, 44, lw=lw)
    f.line((172, 32), (61.5, 32), (61.5, 141.5), (172, 141.5), w=lw)
    f.line((257, 32.5), (300.5, 32.5), (300.5, 141.5), (257, 141.5), w=lw)
    f.line((4, 72.5), (61.5, 72.5), w=lw)
    f.line((300.5, 76), (408, 76), w=lw)
    f.text(213, 43, "R1", size=28, anchor="c")
    f.text(213, 152, "R2", size=28, anchor="c")
    chevron(f, 121, 33, size=14, line_from=64)
    chevron(f, 121, 142, size=14, line_from=62)
    chevron(f, 359, 76, size=15, line_from=300)
    f.text(64, 68, "I_{R1}", size=28)
    f.text(64, 133, "I_{R2}", size=28)
    f.text(348, 63, "I_{t}", size=28)
    f.arrow(332, 174, 36, 174, stroke=BLUE, w=2.6, size=16)
    f.text(92, 210, "U_{R1} = U_{R2} = U_{t}", size=28)


DARKRED = "#c00000"


@figure("c043_1#0")
def reseau_complexe(f):
    lw = 3.5
    k = dict(size=29, family="sans")
    f.rect(87.5, 5.5, 128, 43, lw=lw)
    f.rect(96.5, 101.5, 128, 43, lw=lw)
    f.rect(327, 49, 106.5, 42.5, lw=lw)
    f.text(151, 39, "A=100 Ω", anchor="c", **k)
    f.text(160, 135, "B= 150 Ω", anchor="c", **k)
    f.text(380, 84, "C=40 Ω", anchor="c", **k)
    f.line((89, 22.5), (61, 22.5), (61, 129.5), (98, 129.5), w=2.2)
    f.line((214, 21.5), (246, 21.5), (246, 129.5), (224, 129.5), w=2.2)
    f.line((8, 76.5), (61, 76.5), w=2.2)
    f.line((246, 76.5), (327, 76.5), w=2.2)
    f.line((433.5, 76.5), (459, 76.5), w=2.2)
    t = dict(size=28, family="sans")
    f.text(552, 33, "Étape 1 :", **t)
    f.text(757, 33, "R totale (ensemble AB)", **t)
    f.text(757, 70, "R_{AB} =", **t)
    f.text(890, 60, "150 x 100", anchor="c", **t)
    f.line((832, 63), (948, 63), w=2)
    f.text(890, 91, "150 + 100", anchor="c", **t)
    f.text(953, 60, "=", **t)
    f.text(1027, 60, "15000", anchor="c", **t)
    f.line((987, 63), (1067, 63), w=2)
    f.text(1027, 91, "250", anchor="c", **t)
    f.text(1072, 60, "= 60", **t)
    f.text(552, 124, "Étape 2 :", **t)
    f.text(757, 125, "R_{totale} (constitué du groupe AB et de C)", **t)
    f.text(865, 156, "= R_{AB} + 40 = 60+40 = ", **t)
    f.text(1169, 156, "100", anchor="r", color=DARKRED, **t)


@figure("c043_2#0")
def groupement_serie(f):
    k = dict(size=24, family="sans")
    f.rect(79.5, 14.5, 137, 52, lw=3)
    f.rect(261.5, 14.5, 137, 52, lw=3)
    for x0, x1 in ((35, 79.5), (216.5, 261.5), (398.5, 443)):
        f.line((x0, 40), (x1, 40), w=2)
    f.text(148, 50, "R1=80 Ω", anchor="c", **k)
    f.text(330, 50, "R2=20 Ω", anchor="c", **k)
    f.arrow(398, 78, 59, 78, stroke=BLUE, w=2.6, size=16)
    f.text(214, 102, "10 V", anchor="c", **k)


@figure("c043_3#0")
def groupement_parallele(f):
    k = dict(size=27, family="sans")
    f.line((26, 8.5), (315.5, 8.5), w=2)
    f.line((194.5, 8.5), (194.5, 28), w=2)
    f.line((315.5, 8.5), (315.5, 28), w=2)
    f.rect(169.5, 28.5, 73, 89, lw=3)
    f.rect(290.5, 28.5, 73, 89, lw=3)
    f.line((194.5, 118), (194.5, 142), w=2)
    f.line((315.5, 118), (315.5, 142), w=2)
    f.line((50, 142), (315.5, 142), w=2)
    f.arrow(73.5, 117, 73.5, 47, stroke=BLUE, w=3, size=18)
    f.text(4, 98, "10 V", **k)
    f.text(138, 85, "R1", **k)
    f.text(372, 85, "R2", **k)
    f.text(216, 73, "80 Ω", rot=-90, anchor="c", **k)
    f.text(337, 73, "20 Ω", rot=-90, anchor="c", **k)


@figure("c043_4#0")
def sept_resistances(f):
    k = dict(size=27, family="sans")
    f.line((9, 50.5), (494, 50.5), w=2)
    f.line((84, 205), (597, 205), w=2)
    for x in (32, 134, 237, 339, 441, 543):
        f.rect(x + 1.5, 76.5, 77, 103, lw=3)
        c = x + 40
        f.line((c + 12.5, 50.5), (c + 12.5, 76.5), w=2) if False else None
        f.text(c + 12, 128, "10 Ω", rot=-90, anchor="c", **k)
    for x in (84.5, 187.5, 289.5, 391.5, 493.5):
        f.line((x, 50.5), (x, 76.5), w=2)
        f.line((x, 179.5), (x, 205), w=2)
    f.line((597, 76.5), (597, 54.5), (672.5, 54.5), (672.5, 80.5), w=2)
    f.line((596.5, 179.5), (596.5, 205), w=2)
    f.rect(647.5, 80.5, 77, 102, lw=3)
    f.text(698, 132, "10 Ω", rot=-90, anchor="c", **k)
    f.line((672.5, 182.5), (672.5, 208), w=2)
    f.text(337, 31, "R_{T} = ?", size=29)


def _box(f, x0, y0, x1, y1, label=None, rot=-90, lw=4, size=28):
    f.rect(x0 + lw / 2, y0 + lw / 2, x1 - x0 - lw, y1 - y0 - lw, lw=lw)
    if label:
        f.text((x0 + x1) / 2, (y0 + y1) / 2, label, size=size, family="sans", rot=rot, anchor="c", va="middle")


def _gnd(f, x0, x1, y0, y1):
    f.rect(x0, y0, x1 - x0, y1 - y0, stroke=None, fill=BLACK)


@figure("c044_1#0")
def pont(f):
    for b in ((13, 62, 100, 176, "80 Ω"), (234, 62, 321, 176, "20 Ω"), (13, 228, 100, 341, "R2"),
              (234, 228, 321, 341, "4 Ω")):
        _box(f, *b)
    w = 2
    f.line((70.5, 62), (70.5, 38.5), (263.5, 38.5), (263.5, 62), w=w)
    f.line((153.5, 11), (153.5, 38.5), w=w)
    f.text(158, 22, "+", size=30)
    f.line((70.5, 176), (70.5, 228), w=w)
    f.line((263.5, 176), (263.5, 228), w=w)
    f.line((70.5, 201), (263.5, 203), w=w)
    chevron(f, 175, 202, size=8, w=2.2)
    f.text(142, 176, "I = 0", size=27, family="sans")
    f.line((70.5, 341), (70.5, 368.5), (263.5, 368.5), (263.5, 341), w=w)
    f.line((153.5, 368.5), (153.5, 389), w=w)
    _gnd(f, 126, 180, 388, 401)


@figure("c044_2#0")
def diviseur(f):
    for b in ((33, 42, 112, 147, "2 kΩ"), (33, 195, 112, 300, "3 kΩ"), (236, 195, 315, 300, "5 kΩ")):
        _box(f, *b)
    w = 2
    f.line((59.5, 12), (59.5, 42), w=w)
    f.line((59.5, 147), (59.5, 195), w=w)
    f.line((59.5, 171), (262.5, 171), (262.5, 195), w=w)
    chevron(f, 205, 171, size=8, w=2.2)
    f.line((59.5, 300), (59.5, 317), w=w)
    f.line((262.5, 300), (262.5, 317), w=w)
    _gnd(f, 35, 84, 316, 324)
    _gnd(f, 238, 287, 316, 324)
    f.arrow(131.5, 145, 131.5, 46, stroke=BLUE, w=3, size=18)
    f.text(139, 102, "U = 24 V", size=27, family="sans")
    f.text(307, 151, "I (mA) = ?", size=27, family="sans", bold=True, anchor="r")


@figure("c044_3#0")
def diviseur_r(f):
    for b in ((11, 78, 95, 189, "R"), (11, 238, 95, 349, "R1"), (227, 238, 311, 349, "100 Ω")):
        _box(f, *b)
    w = 2
    f.line((39.5, 0), (39.5, 78), w=w)
    f.line((29, 27), (39.5, 44), (50, 27), stroke=BLUE, w=2.4)
    f.line((39.5, 189), (39.5, 238), w=w)
    f.line((39.5, 221), (255.5, 221), (255.5, 238), w=w)
    f.line((39.5, 349), (39.5, 369), w=w)
    f.line((255.5, 349), (255.5, 369), w=w)
    _gnd(f, 13, 66, 368, 376)
    _gnd(f, 229, 281, 368, 376)
    f.arrow(213, 360, 213, 234, stroke=BLUE, w=3, size=18)
    f.text(61, 45, "I = 300 mA", size=27, family="sans")
    f.text(145, 311, "12 V", size=27, family="sans")


@figure("c044_4#0")
def reseau_mixte(f):
    for x0, y0, x1, y1, s in ((84, 145, 198, 203, "100"), (250, 62, 336, 120, "75"), (250, 200, 364, 259, "30"),
                              (388, 6, 503, 65, "150"), (388, 117, 503, 176, "250"), (388, 200, 503, 259, "80")):
        _box(f, x0, y0, x1, y1)
        f.text((x0 + x1) / 2, (y0 + y1) / 2, s, size=29, family="sans", anchor="c", va="middle")
    w = 2
    f.line((58, 174.5), (85, 174.5), w=w)
    f.line((197, 174.5), (223.5, 174.5), w=w)
    f.line((252, 91.5), (223.5, 91.5), (223.5, 229.5), (252, 229.5), w=w)
    f.line((334, 91.5), (362.5, 91.5), w=w)
    f.line((390, 35.5), (362.5, 35.5), (362.5, 146.5), (390, 146.5), w=w)
    f.line((501, 35.5), (528.5, 35.5), (528.5, 146.5), (501, 146.5), w=w)
    f.line((528.5, 91.5), (555.5, 91.5), (555.5, 229.5), (501, 229.5), w=w)
    f.line((362, 229.5), (390, 229.5), w=w)
    f.line((555.5, 174.5), (583, 174.5), w=w)


def _grey_arrow(f, pts, w=9, head=17, color="#c0c0c0"):
    f.line(pts[:-1] + [pts[-1]], stroke=color, w=w, cap="b")
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    a = math.atan2(y1 - y0, x1 - x0)
    tip = (x1 + head * 0.9 * math.cos(a), y1 + head * 0.9 * math.sin(a))
    f.poly([(x1 + head * 0.75 * math.cos(a + math.pi / 2), y1 + head * 0.75 * math.sin(a + math.pi / 2)), tip,
            (x1 + head * 0.75 * math.cos(a - math.pi / 2), y1 + head * 0.75 * math.sin(a - math.pi / 2))],
           stroke=None, fill=color)


def _chevron_at(f, x, y, ang, s=16, color="#0000ff", w=2.4):
    for da in (2.6, -2.6):
        f.line((x, y), (x + s * math.cos(ang + da), y + s * math.sin(ang + da)), stroke=color, w=w)


def _curved_arrow_shape():
    outer = [(613, 328), (590, 318), (572, 298), (562, 268), (559, 232), (563, 200), (573, 170), (585, 148), (595, 135)]
    head = [(595, 118), (614, 146), (595, 177), (595, 162)]
    inner = [(583, 180), (576, 205), (574, 232), (577, 262), (588, 285), (613, 305)]
    grey = [(574, 232), (577, 262), (588, 285), (613, 305), (613, 328), (590, 318), (572, 298), (562, 268), (559, 232)]
    return outer + head + inner, grey


@figure("c041_3#0")
def kirchhoff(f):
    from figdsl import RED as _RED
    NAVY_ = "#000080"
    BL = "#0000ff"
    it = dict(italic=True)
    w = 3
    # ---- node
    f.line((193, 64), (193, 198), w=w)
    f.line((0, 173), (193, 198), (370, 213), w=w)
    f.line((41, 346), (193, 198), (377, 386), w=w)
    f.circle(193, 198, 10, stroke=BLACK, fill=_RED, lw=1.6)
    _chevron_at(f, 193, 122, -math.pi / 2, color=BL)
    _chevron_at(f, 108, 186, math.atan2(25, 193), color=BL)
    _chevron_at(f, 302, 208, math.atan2(15, 177), s=26, color=BL)
    _chevron_at(f, 121, 268, math.atan2(148, -152), s=29, color=BL)
    _chevron_at(f, 293, 300, math.atan2(-188, -184), s=27, color=BL)
    f.fit(90, 162, 58, "Nœud", **it)
    for x, y, t in ((196, 120, "I_{1}"), (99, 165, "I_{2}"), (289, 187, "I_{5}"), (77, 286, "I_{3}"), (311, 298, "I_{4}")):
        f.text(x, y, t, size=29, **it)
    f.fit(28, 304, 410, "I_{1} + I_{2} + I_{3} + I_{4} + I_{5} = 0", bold=True, color=NAVY_)
    f.fit(28, 290, 443, "I2 + I4 = I1 + I3 + I5", **it)
    f.fit(321, 537, 443, "autre présentation", **it)
    # ---- loop
    f.line((752, 78.5), (517, 78.5), (517, 188.5), w=2)
    f.line((478, 188.5), (556, 188.5), w=2.4)
    f.rect(493, 211, 53, 11, stroke=None, fill=BLACK)
    f.line((517, 222), (517, 366), (836, 366), (836, 323), w=2)
    f.line((814, 78.5), (836, 78.5), (836, 134), w=2)
    f.line((729.5, 78.5), (729.5, 134), w=2)
    f.line((729.5, 323), (729.5, 366), w=2)
    f.circle(783, 73, 31, lw=3.4)
    f.text(783, 84, "M", size=30, anchor="c", **it)
    f.rect(693, 135.5, 80, 187.5, lw=4)
    f.rect(800, 135.5, 79.5, 187.5, lw=4)
    f.text(733, 229, "Résistance 1", size=29, rot=-90, anchor="c", va="middle", **it)
    f.text(840, 229, "Résistance 2", size=29, rot=-90, anchor="c", va="middle", **it)
    shape, grey = _curved_arrow_shape()
    f.poly(grey, stroke=None, fill="#c0c0c0")
    f.poly(shape, stroke=_RED, w=2.4)
    rot = lambda p: (1359 - p[0], 113 + (328 - p[1]) * 239 / 212)
    f.poly([rot(p) for p in grey], stroke=None, fill="#c0c0c0")
    f.poly([rot(p) for p in shape], stroke=_RED, w=2.4)
    for x, y0, y1 in ((472.5, 255, 150), (678.5, 327, 127), (893.5, 335, 124)):
        f.line((x, y0), (x, y1 + 14), stroke=BL, w=2.4)
        f.poly([(x - 7, y1 + 16), (x, y1), (x + 7, y1 + 16)], stroke=None, fill=BL)
    f.line((816, 32.5), (752, 32.5), stroke=BL, w=2.4)
    f.poly([(754, 25.5), (738, 32.5), (754, 39.5)], stroke=None, fill=BL)
    f.text(750, 26, "U_{moteur}", size=29, **it)
    f.text(449, 212, "U_{pile}", size=29, rot=-90, anchor="c", va="middle", **it)
    f.text(656, 228, "U_{R1}", size=29, rot=-90, anchor="c", va="middle", **it)
    f.text(915, 232, "U_{R2}", size=29, rot=-90, anchor="c", va="middle", **it)
    f.fit(551, 628, 58, "Maille", **it)
    f.fit(838, 920, 72, "Moteur", **it)
    f.fit(526, 573, 151, "Pile", **it)
    f.rich(440, 410, [("U_{pile} + U_{R1} = 0", {"b": 1, "color": NAVY_}), (" et ", {}),
                      ("U_{pile} + U_{moteur} + U_{R2} = 0", {"b": 1, "color": NAVY_})], size=29)
    f.fit(575, 890, 443, "U_{pile} = U_{R1} = U_{moteur} + U_{R2}", **it)
    # ---- Wheatstone bridge
    f.line((1180.5, 55), (1180.5, 80), w=2)
    f.line((1117, 144), (1180.5, 80), (1245, 144), w=2)
    for x0, y0, x1, y1, t, r in ((1095.5, 144.5, 1139, 209, "14Ω", -90), (1223.5, 144.5, 1267, 209, "30Ω", -90),
                                 (1097.5, 301.5, 1140, 367, "6 Ω", 90), (1223.5, 298.5, 1267, 363, "20Ω", 90)):
        f.rect(x0, y0, x1 - x0, y1 - y0, lw=2.4)
        f.text((x0 + x1) / 2, (y0 + y1) / 2, t, size=28, rot=r, anchor="c", va="middle", **it)
    f.line((1117, 209), (1117, 301.5), w=2)
    f.line((1245, 209), (1245, 298.5), w=2)
    f.line((1117, 367), (1177.5, 397), (1245, 363), w=2)
    f.line((1177.5, 397), (1177.5, 419), w=2)
    f.rect(1157, 419, 41, 11, stroke=None, fill=BLACK)
    for x, y0, y1 in ((1053.5, 228, 124), (1053.5, 383, 279), (1308.5, 228, 123), (1308.5, 383, 279)):
        f.line((x, y0), (x, y1 + 14), stroke=BL, w=2.2)
        f.poly([(x - 6, y1 + 16), (x, y1), (x + 6, y1 + 16)], stroke=None, fill=BL)
    f.line((1139, 254.5), (1208, 254.5), stroke=BL, w=2.2)
    f.poly([(1206, 248.5), (1222, 254.5), (1206, 260.5)], stroke=None, fill=BL)
    _grey_arrow(f, [(1120, 112), (1148, 76)])
    _grey_arrow(f, [(1121, 248), (1100, 248), (1095, 225)])
    _grey_arrow(f, [(1306, 276), (1306, 245), (1283, 236)])
    _grey_arrow(f, [(1226, 414), (1268, 384)])
    for x0, x1, y, t in ((1010, 1052, 197, "7 V"), (1012, 1050, 333, "3 V"), (1313, 1355, 197, "6 V"),
                         (1313, 1356, 352, "4 V"), (1145, 1192, 243, "1 V"), (1188, 1271, 72, "+ 10 V"),
                         (1205, 1352, 437, "0 V = masse"), (1075, 1312, 25, "Pont de Wheatstone")):
        f.fit(x0, x1, y, t, **it)
