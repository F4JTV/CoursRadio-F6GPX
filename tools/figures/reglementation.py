"""Réglementation (R-1 to R-5) schematics."""
import math

from figdsl import BLACK, BLUE, LIGHT, RED, empty, figure

PUREBLUE = "#0000ff"

from . import waves

GREYLINE = "#bfbfbf"
CHART_RED = "#c0504d"


@figure("c015_1#0")
def types_modulation(f):
    W, H = f.W, f.H
    f.rect(2, 2, W - 4, H - 4, lw=2.2)
    f.line((2, 46), (W - 2, 46), w=1.5)
    cols = [2, 290, 560, 848, 1118, W - 2]
    for x in cols[1:-1]:
        f.line((x, 2), (x, H - 2), w=1.5)
    heads = ["Type de modulation", "AM (Amplitude)", "BLU (dérivé de l’AM)", "CW (A1A)", "FM (Fréquence)"]
    for i, t in enumerate(heads):
        f.text((cols[i] + cols[i + 1]) / 2, 33, t, size=27, italic=True, anchor="c")
    for j, t in enumerate(["Représentation en", "fonction du temps", "(oscillogramme)"]):
        f.text(146, 75 + j * 29, t, size=27, italic=True, anchor="c")
    yc = 98
    # AM
    waves.am(f, 310, 535, yc, 36, periods=11, env_periods=2.0, depth=0.6, phase=0.9, w=2.2)
    f.arrow(310, yc, 548, yc, w=1.6, size=9)
    f.text(538, 82, "T", size=27)
    # BLU
    waves.ssb(f, 600, 825, yc, 40, [(625, 40, 42), (690, 24, 12), (790, 46, 40)], w=2.2)
    f.arrow(600, yc, 835, yc, w=1.6, size=9)
    f.text(827, 80, "T", size=27)
    # CW
    f.arrow(872, yc, 1105, yc, w=1.6, size=9)
    for a, b, n in ((888, 920, 3), (950, 976, 3), (998, 1072, 8)):
        waves.burst(f, a, b, yc, 30, n, w=2.2)
    f.text(1098, 80, "T", size=27)
    # FM
    waves.fm(f, 1160, 1345, yc, 30, periods=9, dev=0.3, w=2.2)
    f.arrow(1155, yc, 1360, yc, w=1.6, size=9)
    f.text(1352, 80, "T", size=27)


@figure("c016_1#0")
def emissions_hors_bande(f):
    W, H = f.W, f.H
    f.rect(8, 7, W - 16, H - 14, lw=2.2)
    y0 = 325
    # spectrum (dash-dot)
    def spec(x):
        d = abs(x - 405)
        if d < 30:
            return 96 + 5 * (1 - (d / 30) ** 2)
        return 320 - 224 * math.exp(-0.026 * (d - 30))
    pts = [(x, min(y0 - 4, spec(x))) for x in range(140, 671, 3)]
    f.line(pts, stroke=RED, w=2.0, dash=[18, 6, 3, 6])
    f.line((405, 86), (405, y0), stroke=RED, w=2.4)
    for x in (348, 457):
        f.line((x, 86), (x, y0), stroke=RED, w=2.0, dash=[7, 5])
    for x in (207, 593):
        f.line((x, 118), (x, y0), stroke=RED, w=2.0, dash=[2.5, 4])
    f.arrow(100, y0, 700, y0, stroke=PUREBLUE, w=2.4, size=14, open_=True)
    f.arrow(350, 237, 455, 237, stroke=PUREBLUE, w=2.4, size=16, both=True)
    f.arrow(209, 265, 401, 265, stroke=PUREBLUE, w=2.4, size=16, both=True)
    f.arrow(409, 265, 591, 265, stroke=PUREBLUE, w=2.4, size=16, both=True)
    s = 26
    f.text(405, 52, "Bande", size=s, anchor="c")
    f.text(405, 82, "Passante (BP)", size=s, anchor="c")
    for cx in (205, 600):
        f.text(cx, 113, "Emissions non désirées", size=s, italic=True, anchor="c")
    for cx, a, b in ((125, "Rayonn.", "non essentiels"), (275, "Emissions", "hors bande"),
                     (525, "Emissions", "hors bande"), (680, "Rayonn.", "non essentiels")):
        f.text(cx, 147, a, size=s, anchor="c")
        f.text(cx, 181, b, size=s, anchor="c")
    for cx in (115, 680):
        f.text(cx, 225, "atténuation =", size=s, italic=True, color=RED, anchor="c")
        f.text(cx, 259, "43 dB", size=s, italic=True, color=RED, anchor="c")
        f.text(cx, 293, "+10 log(P)", size=s, italic=True, color=RED, anchor="c")
    f.text(402, 224, "B P", size=s, color=PUREBLUE, anchor="c")
    f.text(305, 292, "2,5 x BP", size=s, color=PUREBLUE, anchor="c")
    f.text(500, 292, "2,5 x BP", size=s, color=PUREBLUE, anchor="c")
    f.text(405, 362, "Fréquence centrale", size=s, anchor="c")
    f.text(405, 394, "de l’émission (puissance = P)", size=s, anchor="c")
    f.text(690, 364, "fréq.", size=s, color=PUREBLUE, anchor="c")


@figure("c020_1#0")
def exposition_public(f):
    # the chart spans the two rasters c020_1#0 and #1 (1 unit = 1/3 pt)
    W = f.W
    H = 328.3
    f.rect(1, 1, W - 2, H - 2, stroke=GREYLINE, lw=1.5)
    x_axis, x_end = 48, 382
    y0, ytop = 247, 17          # 0 and 100 V/m
    step = (y0 - ytop) / 10
    for k in range(11):
        y = y0 - k * step
        f.line((x_axis, y), (x_end, y), stroke=GREYLINE if k else "#808080", w=1.2)
        f.text(x_axis - 6, y + 3, str(k * 10), size=7.5, family="sans", anchor="r")
    f.line((x_axis, y0), (x_axis, ytop), stroke="#808080", w=1.2)
    cats = ["0,1", "0,5", "1,0", "2,0", "4,0", "6,0", "8,0", "10,0", "20,0", "40,0", "80,0", "120,0",
            "200,0", "400,0", "700,0", "1 000,0", "1 500,0", "2 000,0", "2 500,0", "10 000,0", "30 000,0",
            "70 000,0", "100 000,0", "300 000,0"]
    vals = [87, 87, 87, 61, 43, 37, 33, 30.5, 28, 28, 28, 28, 28, 28, 36, 43, 53, 61, 61, 61, 61, 61, 61, 61]
    n = len(cats)
    dx = (x_end - x_axis) / n
    xs = [x_axis + dx * (i + 0.5) for i in range(n)]
    for i, (x, c) in enumerate(zip(xs, cats)):
        f.line((x_axis + dx * (i + 1), y0), (x_axis + dx * (i + 1), y0 + 4), stroke="#808080", w=1.0)
        f.text(x + 2.5, y0 + 8, c, size=7.2, family="sans", rot=-90, anchor="r")
    f.line([(x, y0 - v * step / 10) for x, v in zip(xs, vals)], stroke=CHART_RED, w=2.4)
    f.text(190, 310, "Fréquence (MHz)", size=8.5, family="sans", bold=True, anchor="c")
    f.text(18, 138, "E (V/m)", size=8.5, family="sans", bold=True, rot=-90, anchor="c")
    f.text(215, 68, "Niveaux de référence pour la", size=15, family="sans", bold=True, anchor="c")
    f.text(215, 96, "limitation de l'exposition du public", size=15, family="sans", bold=True, anchor="c")


empty("c020_1#1")


def _amp(f, label, x_left, top, bottom, apex_x, y, in_x0, out_x1, txt):
    f.poly((x_left, top), (apex_x, y), (x_left, bottom), w=1.8)
    f.line((in_x0, y), (x_left, y), w=1.8)
    f.line((apex_x, y), (out_x1, y), w=1.8)
    f.text(txt[0][0], txt[0][1], label, size=24, family="sans", bold=True)
    for (x, yy, t, b) in txt[1:]:
        f.text(x, yy, t, size=24, family="sans", bold=b)


@figure("c029_2#0")
def gain_1(f):
    _amp(f, "1)", 98, 6, 108, 166, 57, 6, 250,
         [(20, 40), (32, 90, "4 W", False), (192, 44, "8 W", False), (150, 92, "dB = ?", True)])


@figure("c029_2#1")
def gain_2(f):
    _amp(f, "2)", 78, 6, 112, 142, 58, 0, 224,
         [(18, 46), (6, 96, "20 W", False), (160, 44, "P = ?", True), (112, 96, "- 6 dB", False)])


NAVY = "#1c1c8c"
GROUND = "#c8c8c8"


@figure("c030_2#0")
def doublet(f):
    f.arrow(25, 48, 430, 48, stroke=PUREBLUE, w=3, size=18, both=True)
    f.text(210, 38, "L = λ / 2", size=30, bold=True, color=NAVY, anchor="c")
    f.line((25, 77), (214, 77), stroke=RED, w=6, cap=None)
    f.line((241, 77), (432, 77), stroke=RED, w=6, cap=None)
    f.line((214, 77), (214, 118), w=2.2)
    f.line((241, 77), (241, 118), w=2.2)
    f.text(165, 133, "Z", size=30, bold=True, underline=True)
    f.text(186, 133, " =", size=30, bold=True)
    f.text(253, 133, "73 Ω", size=30, bold=True, underline=True)
    f.text(227, 168, "Doublet demi-onde", size=28, anchor="c")


@figure("c030_3#0")
def yagi(f):
    f.text(250, 32, "Élément rayonnant = dipôle", size=27, anchor="c")
    f.text(20, 86, "Réflecteur", size=27)
    f.text(297, 111, "Directeur", size=27)
    f.arrow(37, 96, 113, 163, stroke=PUREBLUE, w=2.4, size=16)
    f.arrow(323, 36, 196, 174, stroke=PUREBLUE, w=2.4, size=16)
    f.arrow(348, 122, 275, 189, stroke=PUREBLUE, w=2.4, size=16)
    f.line((115, 215), (272, 215), w=2)
    f.line((115, 138), (115, 302), stroke=RED, w=6, cap=None)
    f.line((193, 155), (193, 279), stroke=RED, w=6, cap=None)
    f.line((272, 165), (272, 270), stroke=RED, w=6, cap=None)
    f.text(205, 296, "Antene Yagi", size=27, anchor="c")
    f.arrow(62, 319, 373, 319, stroke=PUREBLUE, w=2.4, size=14, open_=True)
    f.text(220, 355, "Direction du rayonnement", size=27, anchor="c")
    f.text(220, 387, "maximum", size=27, anchor="c")


@figure("c030_4#0")
def doublet_replie(f):
    f.arrow(10, 43, 340, 43, stroke=PUREBLUE, w=3, size=18, both=True)
    f.text(177, 31, "L = λ / 2", size=28, bold=True, color=NAVY, anchor="c")
    f.path("M163 96H22Q12 96 12 86V78Q12 69 22 69H330Q340 69 340 78V86Q340 96 330 96H189",
           stroke=RED, w=6)
    f.line((163, 96), (163, 122), w=2.2)
    f.line((189, 96), (189, 122), w=2.2)
    f.text(176, 158, "Z = 300 Ω", size=28, bold=True, underline=True, anchor="c")
    f.text(176, 190, "Doublet demi-onde replié", size=27, anchor="c")


@figure("c030_4#1")
def quart_onde(f):
    for i, t in enumerate(["Antenne quart", "d’onde", "verticale", "(GP)"]):
        f.text(220, 38 + i * 35, t, size=28, anchor="r")
    f.line((245, 0), (245, 186), stroke=RED, w=6, cap=None)
    f.arrow(272, 4, 272, 184, stroke=PUREBLUE, w=2.4, size=14, both=True, open_=True)
    f.text(332, 95, "L(m) = λ/ 4", size=28, bold=True, color=NAVY, rot=-90, anchor="c")
    f.text(62, 201, "Z = 36 Ω", size=28, bold=True, underline=True)
    f.line((190, 187), (245, 187), w=2.2)
    f.line((190, 197), (238, 197), (238, 214), w=2.2)
    f.rect(0, 216, 439, 25, stroke=None, fill=GROUND)
    f.text(88, 242, "Plan de sol,", size=27)
    f.text(258, 242, "masse ou terre", size=27)
    f.line((245, 205), (245, 414), w=4.5, dash=[3, 6], cap=None)
    for i, t in enumerate(["Brin", "reconstitué", "par le plan de", "sol ou la terre"]):
        f.text(122, 303 + i * 36, t, size=27, anchor="c")
    f.arrow(165, 302, 240, 298, stroke=PUREBLUE, w=2.4, size=14)


def _diagrammes(f):
    W = f.W
    s = 27
    lw = 3
    for i, t in enumerate(["Rayonnement", "vertical", "(vu de côté)"]):
        f.text(10, 88 + i * 36, t, size=s)
    f.text(10, 268, "Rayonnement", size=s)
    f.text(10, 304, "Horizontal", size=s)
    f.text(10, 392, "(vu du dessus)", size=s)
    for x, t in ((278, "Antenne isotropique"), (505, "Quart d'onde"), (893, "Doublet horizontal"), (1243, "Beam Yagi")):
        f.text(x, 434, t, size=s, anchor="c")
    f.text(500, 178, "Plan de sol", size=s, anchor="c")
    f.text(968, 174, "Sol", size=s, anchor="c")
    f.text(1360, 160, "Sol", size=s, anchor="c")
    f.text(763, 394, "en espace libre", size=s, anchor="c")
    f.text(1022, 394, "à λ/2 du sol", size=s, anchor="c")

    def reddot(x, y, color=RED):
        f.circle(x, y, 12, stroke=None, fill=color)

    def blue(x1, y1, x2, y2, both=False):
        f.arrow(x1, y1, x2, y2, stroke=PUREBLUE, w=3, size=16, open_=True, both=both)

    # isotropic
    f.circle(289, 100, 75, lw=lw)
    reddot(289, 100)
    f.circle(291, 297, 75, lw=lw)
    reddot(291, 297)
    # quarter wave, side view
    f.rect(420, 147, 177, 10, stroke=None, fill=GROUND)
    f.path("M507 142C430 150 384 64 440 58C485 54 506 100 507 142Z", w=lw)
    f.path("M507 142C510 100 532 54 577 58C632 64 586 150 507 142Z", w=lw)
    f.line((507, 63), (507, 147), stroke=RED, w=12, cap=None)
    blue(507, 140, 422, 65)
    blue(507, 140, 606, 62)
    # quarter wave, top view
    f.circle(510, 300, 77, lw=lw)
    blue(511, 302, 512, 226)
    blue(511, 302, 512, 370)
    blue(511, 302, 438, 300)
    blue(511, 302, 580, 300)
    reddot(510, 303)
    # dipole in free space
    f.ellipse(763, 113, 119, 109, lw=lw)
    blue(763, 118, 763, 8)
    blue(763, 118, 763, 218)
    blue(763, 118, 647, 118)
    blue(763, 118, 879, 118)
    reddot(761, 118)
    f.circle(705, 300, 59, lw=lw)
    f.circle(821, 300, 59, lw=lw)
    f.line((763, 247), (763, 356), stroke=RED, w=12, cap=None)
    blue(648, 300, 878, 300, both=True)
    # dipole half a wave above ground
    f.rect(933, 143, 175, 10, stroke=None, fill=GROUND)
    f.path("M905 72C905 30 990 40 1040 56C1080 40 1135 40 1135 82C1135 128 1078 140 1020 140C960 140 905 120 905 72Z", w=lw)
    blue(1021, 110, 920, 48)
    blue(1021, 110, 1131, 58)
    reddot(1021, 110)
    f.path("M1022 252C1056 235 1140 242 1140 300C1140 358 1056 365 1022 346C988 365 905 356 905 300C905 242 988 235 1022 252Z", w=lw)
    f.line((1025, 247), (1025, 356), stroke=RED, w=12, cap=None)
    blue(910, 300, 1140, 300, both=True)
    # beam Yagi
    f.rect(1213, 149, 197, 10, stroke=None, fill=GROUND)
    f.path("M1182 106C1182 92 1230 82 1300 82C1360 62 1442 92 1432 106C1420 122 1300 132 1202 132C1186 132 1182 120 1182 106Z", w=lw)
    reddot(1228, 112, "#a0a0a0")
    reddot(1317, 112, "#a0a0a0")
    reddot(1272, 112)
    blue(1272, 112, 1428, 102)
    f.path("M1182 286C1180 268 1230 266 1252 262C1310 252 1400 262 1432 288C1400 314 1310 322 1252 313C1230 310 1182 308 1182 295Z", w=lw)
    f.line((1233, 243), (1233, 330), stroke="#a0a0a0", w=12, cap=None)
    f.line((1315, 250), (1315, 322), stroke="#a0a0a0", w=12, cap=None)
    f.line((1274, 250), (1274, 322), stroke=RED, w=12, cap=None)
    blue(1278, 287, 1430, 287)


@figure("c031_1#0")
def diagrammes_rayonnement(f):
    _diagrammes(f)


@figure("c082_2#0")
def diagrammes_rayonnement_t9(f):
    _diagrammes(f)


@figure("c032_1#0")
def pire(f):
    f.text(172, 45, "Quelle", size=27, family="sans", anchor="r")
    f.text(172, 80, "est la PIRE ?", size=27, family="sans", anchor="r")
    f.rect(182, 10, 121, 72, lw=2.2)
    f.text(243, 58, "50 W", size=27, family="sans", anchor="c")
    f.rect(303, 39, 167, 15, stroke=None, fill="#808080")
    f.text(395, 31, "câble", size=27, family="sans", anchor="c")
    f.text(395, 84, "Perte = 2 dB", size=27, family="sans", anchor="c")
    f.text(482, 57, "Antenne = 12 dBi", size=27, family="sans")


@figure("c032_2#0")
def quart_onde_adapt(f):
    f.text(3, 32, "25 Ω", size=29, family="sans", italic=True)
    f.line((85, 12), (194, 12), w=4, cap=None)
    f.line((85, 23), (194, 23), w=4, cap=None)
    f.text(196, 32, "100 Ω", size=29, family="sans", italic=True)
    f.text(294, 32, "Z_{ligne} = ?", size=29, family="sans", italic=True)
    f.arrow(112, 48, 84, 48, stroke=PUREBLUE, w=2, size=10, open_=True)
    f.arrow(162, 48, 194, 48, stroke=PUREBLUE, w=2, size=10, open_=True)
    f.text(137, 57, "λ/4", size=25, family="sans", anchor="c")
