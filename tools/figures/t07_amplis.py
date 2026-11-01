"""Chapter 7 (amplifiers, oscillators, mixers) figures."""
import math

from figdsl import BLACK, RED, figure, text_width

from .t02_alternatif import BLUE, NAVY, GREY, NB, BU, I_, _humps
from .t03_transfo import vcoil
from .t05_diodes import gnd
from .t06_transistors import bjt

S = 31
W = 2.4
GREEN = "#00a050"
DGREEN = "#006000"
IT = dict(size=S, italic=True)


@figure("c070_1#0")
def plage_fonctionnement(f):
    pts = [(122, 58), (108, 58), (132, 18), (156, 58), (142, 58), (142, 176), (156, 176), (132, 216), (108, 176),
           (122, 176)]
    f.poly(pts, stroke="#005020", fill="#00a040", w=1.5)
    f.line((136, 19), (425, 19), stroke=DGREEN, w=1.6, dash=[1.5, 2.5])
    f.line((136, 215), (425, 215), stroke=DGREEN, w=1.6, dash=[1.5, 2.5])
    f.line((160, 115), (460, 115), w=1.6, dash=[1.5, 2.5])
    f.curve(lambda x: 115 - 63 * math.sin(2 * math.pi * (x - 191) / 64.5) * (0.78 + 0.22 * math.sin(2 * math.pi * (x - 215) / 129)),
            188, 427, n=240, stroke=RED, w=2.4)
    for x, t in ((18, "Plage de"), (47, "fonctionnement de"), (76, "l’amplificateur")):
        f.text(x, 115, t, size=29, rot=-90, anchor="c", va="middle")
    f.text(461, 111, "Tension de", size=27)
    f.text(461, 143, "repos (V)", size=27)
    f.text(352, 200, "Signal à amplifier", size=27, color=RED)


@figure("c070_2#0")
def etage_ampli(f):
    f.rect(92.5, 125.5, 43, 84, lw=2.6)
    f.rect(92.5, 288.5, 43, 85, lw=2.6)
    f.line((114, 85), (114, 125.5), w=W)
    f.line((114, 209.5), (114, 288.5), w=W)
    f.line((114, 373.5), (114, 405), w=W)
    gnd(f, 96, 404, 137, 414)
    f.text(85, 72, "U(+)", size=S)
    f.text(142, 163, "R1", size=S)
    f.text(142, 348, "R2", size=S)
    f.line((9, 248.5), (51, 248.5), w=W)
    gnd(f, 50, 229, 52.5, 269)
    gnd(f, 71, 229, 73.5, 269)
    f.line((72, 249), (277, 249), w=W)
    f.line((231, 243), (243, 249), (231, 255), stroke=BLUE, w=2)
    f.text(1, 219, "Entrée", size=S, color=RED)
    f.text(34, 299, "Ce", size=S)
    f.text(151, 230, "I_{b}", size=S)
    bjt(f, 302, 249.5, 40.5, 277, (322.5, 216), (330, 290))
    f.line((322.5, 216), (322.5, 170), w=W)
    f.rect(301.5, 84.5, 42, 84, lw=3.4)
    f.line((322.5, 23), (322.5, 84.5), w=W)
    f.line((316, 57), (322.5, 69), (329, 57), stroke=BLUE, w=2.2)
    f.text(303, 20, "U(+)", size=S)
    f.text(340, 63, "I_{c}", size=S)
    f.line((323, 187), (385, 187), w=W)
    gnd(f, 384.5, 168, 386.5, 208)
    gnd(f, 405.5, 168, 407.5, 208)
    f.line((407, 187), (430, 187), w=W)
    f.text(369, 238, "Cs", size=S)
    f.rich(458, 195, [("Sortie", {"color": RED}), (" (=entrée", {})], size=S)
    f.text(458, 229, "de l’étage", size=S)
    f.text(457, 262, "suivant)", size=S)
    f.line((330, 290), (330.5, 405), w=W)
    gnd(f, 305, 404, 346, 414)
    f.arrow(280.5, 183, 280.5, 63, stroke=BLUE, w=2.4, size=18, open_=True)
    f.text(236, 142, "U_{Rc}", size=S)
    f.arrow(427, 395, 427, 212, stroke=BLUE, w=2.4, size=18, open_=True)
    f.text(431, 302, "V_{ce}", size=S)
    f.arrow(287, 307, 245, 272, stroke=BLUE, w=2.4, size=16, open_=True)
    f.text(217, 316, "V_{be}", size=S)
    f.rich(369, 113, [("Résistance", BU)], size=S)
    f.rich(369, 150, [("de charge (Rc)", BU)], size=S)


def rfit(f, x0, x1, y, parts, cap=31):
    """Rich line whose ink spans x0..x1 on the original (font size derived
    from the measured width, capped)."""
    w = 0.0
    for t, st in parts:
        w += text_width(t, 10.0, "serif", st.get("b"), st.get("i"))
    size = max(28, min(cap, 10.0 * (x1 - x0) / w))
    f.rich(x0, y, parts, size=size)


def _axis(f, x, y_bot, y_top, x_end):
    f.line((x, y_bot), (x, y_top), w=2.2)
    f.line((x - 6, y_top + 12), (x, y_top), (x + 6, y_top + 12), w=2.2)
    f.line((x, y_bot), (x_end, y_bot), w=2.2)
    f.line((x_end - 12, y_bot - 6), (x_end, y_bot), (x_end - 12, y_bot + 6), w=2.2)


@figure("c070_3#0")
def classes_amplification(f):
    for y in (11.5, 47.5, 767):
        f.line((9.5, y), (1349.5, y), w=2.2)
    for x in (9.5, 209.5, 559.5, 971, 1349.5):
        f.line((x, 11.5), (x, 767), w=2.2)
    for x, t in ((387, "Classe A"), (765, "Classe B"), (1160, "Classe C")):
        f.text(x, 38, t, size=S, anchor="c")
    for y, x0, x1, t in ((176, 60, 158, "Schéma"), (419, 51, 167, "Forme du"), (453, 18, 201, "signal amplifié"),
                         (555, 45, 176, "Tension de"), (589.5, 33, 185, "repos / plage"), (624, 20, 200, "d’amplification"),
                         (760.5, 42, 182, "Rendement")):
        f.fit(x0, x1, y, t, max_size=S)
    f.text(109, 210, "de", size=29, anchor="c")
    f.fit(54, 148, 244, "principe", max_size=S)
    f.fit(24, 198, 692.5, "Commentaires", italic=True, max_size=S)
    # ---- class A
    f.rect(272.5, 138.5, 42, 63, lw=2)
    f.rect(272.5, 243.5, 42, 62, lw=2)
    f.line((294.5, 120), (294.5, 138.5), w=W)
    f.line((294.5, 201.5), (294.5, 243.5), w=W)
    f.line((294.5, 305.5), (294.5, 344), w=W)
    gnd(f, 274, 343, 313, 353)
    f.text(283, 106, "+", size=S)
    f.line((251, 223.5), (352, 223.5), w=W)
    f.text(236, 233, "E", size=S, color=RED)
    bjt(f, 380, 223, 42, 352, (399, 182), (414, 280), lw=3)
    f.rect(378, 98, 40, 62, lw=4)
    f.line((399, 160), (399, 182), w=W)
    f.line((399, 98), (399, 68), w=W)
    f.text(380, 82, "+", size=S)
    f.line((399, 182), (439, 182), w=W)
    gnd(f, 438, 160, 440.5, 202)
    gnd(f, 461, 160, 463.5, 202)
    f.line((462, 181), (502, 181), w=W)
    f.text(519, 190, "S", size=S, color=RED)
    f.fit(425, 552, 107, "Résistance")
    f.fit(425, 538, 139, "de charge")
    f.line((414, 280), (414, 355), w=W)
    gnd(f, 389, 354, 431, 364)
    _axis(f, 245.5, 516.5, 365, 505)
    f.line((247, 440), (495, 440), stroke="#a0a0a0", w=2, dash=[2, 2])
    f.curve(lambda x: 440 - 52 * math.sin(2 * math.pi * (x - 284) / 52), 280, 470, n=200, stroke=RED, w=2.2)
    f.text(214, 512, "0", size=29)
    f.text(507, 522, "T", size=S)
    f.text(513, 444, "V", size=29)
    # ---- class B
    f.text(583, 148, "E", size=S, color=RED)
    f.line((606, 138), (606, 184), w=W)
    vcoil(f, 606, 184, 263, 4, 20, side=1)
    f.line((606, 263), (606, 300), w=W)
    gnd(f, 579, 299, 629, 309)
    vcoil(f, 668, 157, 214, 2, 18, side=-1)
    vcoil(f, 668, 214, 265, 2, 18, side=-1)
    f.line((668, 157), (668, 109.5), (726, 109.5), w=W)
    f.line((668, 265), (670.5, 265), (670.5, 305.5), (728, 305.5), w=W)
    f.line((668, 214.5), (705, 214.5), w=W)
    gnd(f, 705, 194, 716, 235)
    bjt(f, 751.5, 110, 41, 726, (782, 72), (786, 172), lw=3)
    f.line((782, 72), (782, 67.5), (838, 67.5), (838, 162), w=W)
    f.line((786, 172), (786, 179), w=W)
    gnd(f, 761, 178, 800, 188)
    bjt(f, 753.5, 306, 41.5, 728, (786, 268), (789, 350), lw=3)
    f.line((786, 268), (786, 267), (838, 267), (838, 247), w=W)
    vcoil(f, 838, 162, 247, 4, 22, side=1)
    f.text(822, 214, "+", size=28)
    vcoil(f, 905, 185, 226, 2, 18, side=-1)
    f.line((905, 185), (905, 141), (947, 141), w=W)
    f.line((905, 226), (924.5, 226), (924.5, 291), w=W)
    gnd(f, 908, 290, 947, 300)
    f.text(921, 131, "S", size=S, color=RED)
    f.line((789, 350), (789, 357), w=W)
    gnd(f, 761, 356, 814, 367)
    f.text(674, 96, "T1", size=S, color=RED)
    f.text(674, 336, "T2", size=S, color=BLUE)
    _axis(f, 601.5, 519.5, 365, 950)
    f.line((605, 431), (920, 431), stroke="#a0a0a0", w=2, dash=[2, 2])
    per = 104.0
    x0 = 626
    for k in range(3):
        a = x0 + k * per
        f.curve(lambda x, a=a: 431 - 50 * math.sin(2 * math.pi * (x - a) / per), a, a + per / 2, n=40,
                stroke=RED, w=2.2, dash=[6, 4])
        if k < 2:
            b = a + per / 2
            f.curve(lambda x, a=a: 431 - 50 * math.sin(2 * math.pi * (x - a) / per), b, b + per / 2, n=40,
                    stroke="#4040ff", w=2, dash=[2, 2.5])
    f.text(578, 437, "0", size=29)
    f.text(677, 414, "T1", size=29, color=RED)
    f.text(733, 470, "T2", size=29, color=BLUE)
    f.text(922, 437, "V", size=29)
    # ---- class C
    f.text(1081, 136, "+", size=S)
    f.line((1099, 134.5), (1163, 134.5), stroke=GREY, w=W)
    f.line((1162.5, 111), (1162.5, 177), (1213, 177), w=W)
    f.line((1162.5, 111), (1182, 111), w=W)
    _humps(f, 1182, 1267, 111, 4, 18, w=W)
    f.line((1267, 111), (1282.5, 111), (1282.5, 212), (1224, 212), w=W)
    f.line((1224.5, 104), (1224.5, 69.5), (1305, 69.5), stroke=GREY, w=W)
    f.text(1313, 80, "S", size=S, color=RED)
    gnd(f, 1212, 156, 1214.5, 195)
    gnd(f, 1223, 154, 1225.5, 197)
    f.line((1225, 177), (1282.5, 177), w=W)
    f.text(1186, 86, "L", size=S)
    f.text(1186, 143, "Fo", size=S)
    f.text(1186, 196, "C", size=S)
    bjt(f, 1192.5, 255, 41, 1173, (1224, 212), (1205, 290), lw=3)
    f.line((1044, 256.5), (1173, 256.5), stroke=GREY, w=W)
    f.text(999, 268, "E", size=S, color=RED)
    f.line((1205, 290), (1205, 344), w=W)
    gnd(f, 1177, 343, 1227, 353)
    f.line((1046.5, 256.5), (1046.5, 271), w=W)
    f.rect(1027, 271, 41, 57, stroke="#808080", lw=4)
    f.rect(1032, 276, 31, 47, lw=1.4)
    f.text(1047, 299, "Rp", size=26, rot=-90, anchor="c", va="middle")
    f.line((1046.5, 328), (1046.5, 349), w=W)
    f.line((1124.5, 256.5), (1124.5, 297), w=W)
    gnd(f, 1097, 296, 1152, 298.5)
    gnd(f, 1097, 312, 1152, 314.5)
    f.line((1124.5, 314), (1124.5, 344), w=W)
    gnd(f, 1102, 343, 1143, 353)
    _axis(f, 1019.5, 519.5, 365, 1310)
    f.line((1025, 458), (1318, 458), stroke="#a0a0a0", w=2, dash=[2, 2])
    per = 78.5
    peak = lambda x: 457.5 - 52.5 * math.cos(2 * math.pi * (x - 1060) / per)
    for k in range(4):
        c = 1060 + k * per
        f.curve(peak, c - 14, c + 14, n=24, stroke=RED, w=2.4)
        if k < 3:
            f.curve(peak, c + 14, c + per - 14, n=50, stroke="#4040ff", w=2, dash=[5, 4])
    f.text(997, 437, "0", size=29)
    f.text(1112, 486, "LC", size=29, color=BLUE)
    f.text(1312, 470, "V", size=29)
    # ---- text rows (ink extents measured on the original)
    Y = [555, 589.5, 624, 658, 692.5, 726, 760.5]
    rows = [
        (Y[0], 247, 521, [("La tension de repos est", {})]),
        (Y[1], 247, 523, [("centrée", BU), (" par rapport à la", {})]),
        (Y[2], 248, 518, [("plage d’amplification", {})]),
        (Y[3], 265, 510, [("Montage classique ;", I_)]),
        (Y[4], 225, 546, [("génère peu d’harmoniques", I_)]),
        (Y[5], 289, 483, [("car très linéaire", I_)]),
        (Y[6], 220, 552, [("30% max ", {}), ("(50 % en théorie)", I_)]),
        (Y[0], 572, 827, [("amplification par T1 :", {})]),
        (Y[0], 935, 957, [("et", {})]),
        (Y[1], 572, 662, [("par T2 :", {})]),
        (Y[1], 768, 960, [(". Les tensions de", {})]),
        (Y[2], 572, 960, [("repos sont ", {}), ("à la limite", BU), (" de la plage.", {})]),
        (Y[3], 572, 959, [("2 transistors, 2 transformateurs ;", I_)]),
        (Y[4], 585, 950, [("peut générer des harmoniques", I_)]),
        (Y[5], 636, 899, [("impaires (3f, 5f, 7f, …)", I_)]),
        (Y[6], 582, 952, [("50% à 60% ", {}), ("(78,6% en théorie)", I_)]),
        (Y[0], 1110, 1324, [(": restitution par le", {})]),
        (Y[1], 1005, 1309, [("circuit LC. La tension de", {})]),
        (Y[2], 1003, 1330, [("repos ", {}), ("en dessous", BU), (" de la plage.", {})]),
        (Y[3], 1021, 1300, [("Montage peu courant ;", I_)]),
        (Y[4], 1028, 1291, [("génère un fort niveau", I_)]),
        (Y[5], 997, 1324, [("d’harmoniques (2f, 3f, 4f, …)", I_)]),
        (Y[6], 1004, 1315, [("70% à 80% (et parfois plus)", {})]),
    ]
    for y, x0, x1, parts in rows:
        rfit(f, x0, x1, y, parts)
    f.line((830, 549), (922, 549), stroke=RED, w=2, dash=[8, 6])
    f.line((678, 584), (760, 584), stroke=BLUE, w=1.6)
    f.line((1018, 549), (1105, 549), stroke=BLUE, w=2, dash=[6, 4])



PURPLE = "#800080"


def _axis_arrow(f, x, y, dx, dy, s=14, w=3):
    """Open chevron at (x, y) pointing along (dx, dy)."""
    px, py = -dy, dx
    f.line((x - dx * s + px * s * 0.55, y - dy * s + py * s * 0.55), (x, y),
           (x - dx * s - px * s * 0.55, y - dy * s - py * s * 0.55), w=w)


@figure("c071_1#0")
def caracteristiques(f):
    # characteristic curves of the transistor (Ic = f(Vce) for several Ib)
    f.spline([(259, 244), (260, 222), (264, 201), (270, 186), (279, 172), (290, 164), (300, 161.5)], w=3)
    f.line((300, 161.5), (561, 161.5), w=3)
    f.spline([(561, 161.5), (570, 156), (578, 148), (584, 138), (588, 127), (591, 110), (591, 102)], w=3)
    f.spline([(280, 282), (281, 266), (286, 251), (292, 240), (301, 231), (312, 226), (328, 223.5)], w=3)
    f.line((328, 223.5), (600, 223.5), w=3)
    f.spline([(600, 223.5), (608, 219), (616, 210), (623, 198), (628, 186), (632, 166), (634, 143)], w=3)
    f.spline([(322, 323), (323, 306), (328, 295), (335, 288), (345, 285)], w=3)
    f.line((345, 285), (642, 285), w=3)
    f.spline([(642, 285), (652, 278), (660, 265), (667, 247), (672, 225), (675, 203), (677, 184)], w=3)
    # load line and overheating curve
    f.line((238, 87.5), (585, 347), stroke=RED, w=1.5, dash=[1.5, 2.5], cap="b")
    f.spline([(338, 10), (346, 26), (355, 47), (364, 67), (376, 92), (392, 124), (408, 151), (424, 174),
              (440, 194), (456, 210), (472, 224), (496, 240), (528, 256), (560, 268), (600, 280), (640, 289),
              (704, 301)], stroke=PURPLE, w=3, dash=[7, 4])
    # input characteristic (red)
    f.spline([(0, 24), (30, 32), (60, 43), (84, 60), (96, 74)], stroke=RED, w=3)
    f.line((96, 74), (238, 347), stroke=RED, w=3)
    f.spline([(238, 347), (236, 385), (234, 421), (231, 445), (226, 462), (218, 476), (204, 485)], stroke=RED, w=3)
    f.line((204, 485), (96, 527), stroke=RED, w=3)
    # axes
    f.line((238, 44), (238, 529), w=3.2)
    f.line((42, 347), (693, 347), w=3.2)
    _axis_arrow(f, 238, 44, 0, -1)
    _axis_arrow(f, 238, 529, 0, 1)
    _axis_arrow(f, 42, 347, -1, 0)
    _axis_arrow(f, 693, 347, 1, 0)
    # graphical construction (blue dashes)
    dash = dict(stroke=BLUE, w=1.4, dash=[4, 3])
    f.line((236, 490), (180, 490), **dash)
    f.line((177, 488), (177, 228), **dash)
    f.line((180, 224), (422, 224), **dash)
    f.line((425.5, 227), (425.5, 344), **dash)
    for x, y, dx, dy in ((178, 490, -1, 0), (177, 225, 0, -1), (424, 224, 1, 0), (425.5, 345, 0, 1)):
        _axis_arrow(f, x, y, dx, dy, s=7, w=1.4)
        f.line((x - dx * 7 + dy * 4, y - dy * 7 - dx * 4), (x, y), (x - dx * 7 - dy * 4, y - dy * 7 + dx * 4),
               stroke=BLUE, w=1.4)
    # pointers
    for (x0, y0, x1, y1) in ((79, 14, 57, 35), (418, 41, 373, 63), (320, 418, 251, 426), (520, 443, 541, 327)):
        f.line((x0, y0), (x1, y1), stroke=BLUE, w=2.4)
        a = math.atan2(y1 - y0, x1 - x0)
        for da in (2.6, -2.6):
            f.line((x1, y1), (x1 + 15 * math.cos(a + da), y1 + 15 * math.sin(a + da)), stroke=BLUE, w=2.4)
    # labels
    T = 29
    f.fit(89, 202, 26, "saturation", max_size=T)
    f.fit(362, 602, 26, "courbe de surchauffe", max_size=T)
    f.fit(138, 232, 89, "U(+)/Rc", max_size=T)
    f.text(252, 72, "I_{c}", size=T)
    f.text(31, 152, "β = 100", size=T)
    f.text(444, 153, "I_{b}=40 µA", size=T)
    f.text(148, 214, "3", size=T)
    f.text(180, 214, "mA", size=T)
    f.text(474, 216, "I_{b}=30 µA", size=T)
    f.text(581, 275, "I_{b}= 20 µA", size=T)
    f.text(30, 331, "I_{b}", size=T)
    f.text(151, 376, "30 µA", size=T)
    f.text(408, 377, "5V", size=T)
    f.text(575, 377, "U (+)", size=T)
    f.text(651, 377, "V_{ce}", size=T)
    f.text(327, 419, "Blocage", size=T)
    f.text(412, 481, "droite de charge", size=T)
    f.text(243, 500, "1V", size=T)
    f.text(187, 523, "V_{be}", size=T)


@figure("c071_2#0")
def etage_hf(f):
    T = 29
    f.line((81, 196.5), (119, 196.5), w=W)
    _humps(f, 119, 158.5, 196.5, 2, 20, w=W)
    _humps(f, 177.5, 237, 196.5, 3, 20, w=W)
    f.line((158.5, 196.5), (158.5, 231), w=W)
    f.line((177.5, 196.5), (177.5, 231), w=W)
    gnd(f, 139, 230, 197, 239.5)
    f.fit(0, 110, 186, "Entrée HF", color=RED)
    bjt(f, 374, 197.5, 40, 237, (392.5, 160), (402, 230), lw=3)
    gnd(f, 349, 179, 358, 217)
    f.line((402, 230), (418.5, 246), w=W)
    f.line((256, 196.5), (256, 100.5), (294, 100.5), w=W)
    f.rect(294.5, 81.5, 80, 40, lw=3)
    f.fit(315, 352, 112, "Rcr")
    f.line((375, 100.5), (392.5, 100.5), w=W)
    f.line((392.5, 160), (392.5, 42.5), (470.5, 42.5), w=W)
    # tank circuit
    _humps(f, 470.5, 549, 24, 3, 18, w=W)
    f.line((470.5, 24), (470.5, 62), (490, 62), w=W)
    gnd(f, 489, 44, 492, 82)
    gnd(f, 508.5, 44, 511.5, 82)
    f.line((511, 62), (549, 62), w=W)
    f.line((549, 24), (549, 158), w=W)
    # output coupling
    _humps(f, 568.5, 609, 24, 2, 18, w=W)
    f.line((568.5, 24), (568.5, 62), (604, 62), w=W)
    gnd(f, 603, 44, 612, 82)
    f.line((609, 23.5), (663, 23.5), w=W)
    f.line((651, 15), (663, 23.5), (651, 32), w=W)
    f.fit(670, 774, 31, "Sortie HF", color=RED)
    f.fit(669, 794, 62, "= Entrée de")
    f.fit(670, 827, 93, "l’étage suivant")
    # decoupling and choke
    gnd(f, 466, 140, 476, 178)
    f.line((476, 158), (498.5, 158), w=W)
    gnd(f, 497.5, 139, 500, 177)
    gnd(f, 509, 140, 511.5, 178)
    f.line((511, 158), (590, 158), w=W)
    f.fit(475, 505, 127, "Cd")
    _humps(f, 589, 648, 158, 2, 20, w=W)
    f.line((593, 127.5), (650, 127.5), w=2.6, dash=[2.4, 3])
    f.line((648, 158), (686, 158), w=W)
    f.text(686, 166, "+", size=24)
    f.fit(591, 646, 185, "Choc")
    # emitter network
    f.line((418.5, 246), (418.5, 319.5), (467, 319.5), w=W)
    f.line((418.5, 246), (431, 246), w=W)
    f.rect(431.5, 234.5, 79, 40, lw=3)
    f.fit(452, 482, 258, "Re")
    f.line((511, 246), (545, 246), w=W)
    gnd(f, 544, 236, 554, 274)
    gnd(f, 466, 297, 468.5, 335)
    gnd(f, 480.5, 297, 483, 335)
    f.line((482, 319.5), (545, 319.5), w=W)
    gnd(f, 544, 297, 554, 335)
    f.fit(492, 522, 315, "Ce")


MAROON = "#990000"
GREEN_SIG = "#008000"


def _filled_head(f, x_base, y, length=16, half=7.5, fill=BLACK):
    f.poly([(x_base, y - half), (x_base + length, y), (x_base, y + half)], stroke=None, fill=fill)


def _chev(f, x, y, dx, dy, s=11, w=2.2, stroke=BLACK):
    px, py = -dy, dx
    f.line((x - dx * s + px * s * 0.6, y - dy * s + py * s * 0.6), (x, y),
           (x - dx * s - px * s * 0.6, y - dy * s - py * s * 0.6), w=w, stroke=stroke)


def _spectrum_axes(f, x, y_axis, y_top, x_end, f_lab):
    f.line((x, y_axis), (x, y_top), w=2.2)
    _chev(f, x, y_top, 0, -1)
    f.line((x, y_axis), (x_end, y_axis), w=2.2)
    _chev(f, x_end, y_axis, 1, 0)
    f.text(f_lab[0], f_lab[2], "f", size=27)


def _amp_triangle(f, x_left, y_top, y_bot, x_apex, y_in, x_in0, x_out1, thick_out=False):
    yc = (y_top + y_bot) / 2
    f.poly([(x_left, y_top), (x_apex, yc), (x_left, y_bot)], w=3)
    f.line((x_in0, y_in), (x_left, y_in), w=2)
    _chev(f, x_left, y_in, 1, 0, s=12, w=2)
    f.line((x_apex, yc), (x_out1, yc), w=3 if thick_out else 2)
    _chev(f, x_out1, yc, 1, 0, s=12, w=3 if thick_out else 2)


@figure("c072_1#0")
def distorsion_frequences(f):
    _spectrum_axes(f, 21, 193.5, 36, 256, (280, 290, 202))
    for x in (73, 125.5, 179):
        f.rect(x - 3, 113, 6, 80.5, stroke=None, fill=RED)
    for x0, x1, t in ((50, 72, "f1"), (104, 126, "f2"), (160, 182, "f3")):
        f.text((x0 + x1) / 2, 222.5, t, size=27, anchor="c")
    f.fit(50, 222, 44, "Signal d'entrée", color=RED)
    _amp_triangle(f, 310, 27, 111, 414, 78, 257, 455, thick_out=True)
    f.fit(317, 428, 144, "Ampli RF")
    _spectrum_axes(f, 497, 193.5, 36, 750, (757, 768, 202))
    for x, top in ((549.5, 61), (602, 88), (655.5, 113)):
        f.rect(x - 2.5, top, 5, 193.5 - top, stroke=None, fill=BLUE)
    for x0, x1, t in ((527, 548, "f1"), (580, 601, "f2"), (636, 656, "f3")):
        f.text((x0 + x1) / 2, 222.5, t, size=27, anchor="c")
    f.fit(552, 733, 44, "Signal de sortie", color=RED)
    f.fit(225, 515, 250, "distorsion de fréquences")


@figure("c072_1#1")
def distorsion_harmonique(f):
    _spectrum_axes(f, 18.5, 180.5, 14, 134, (139, 149, 170))
    f.rect(79, 74, 6, 106.5, stroke=None, fill=RED)
    f.text(75, 207.5, "fe", size=27, anchor="c")
    f.fit(40, 212, 40, "Signal d'entrée", color=RED)
    _amp_triangle(f, 221, 72, 177, 347, 135.5, 181, 389)
    f.fit(246, 360, 207.5, "Ampli RF")
    _spectrum_axes(f, 463.5, 179.5, 13, 642, (642, 652, 170))
    f.line((463.5, 70.5), (513, 70.5), stroke=RED, w=1.2)
    f.rect(510, 70, 6, 109.5, stroke=None, fill=RED)
    f.line((463.5, 124.5), (566, 124.5), stroke=BLUE, w=1.2)
    f.rect(564, 124, 4.5, 55.5, stroke=None, fill=BLUE)
    f.fit(407, 452, 82, "4 V")
    f.fit(407, 452, 135, "2 V")
    f.text(514, 207.5, "fe", size=27, anchor="c")
    f.text(575, 207.5, "2fe", size=27, anchor="c")
    f.fit(492, 670, 40, "Signal de sortie", color=BLUE)
    f.fit(115, 597, 257, "distorsion harmonique (ou d’amplitude)")
    T = 23.5
    sans = dict(size=T, family="sans")
    f.rich(11, 305, [("Exemple :", {"u": 1, "color": MAROON}), (" Quel est le taux de distorsion harmonique de", {})],
           **sans)
    f.rich(52, 336, [("l’harmonique 2 (signal 2fe) ?", {})], **sans)
    f.rich(52, 367, [("Réponse :", {"u": 1, "color": MAROON}),
                     (" TDH = (V_{2fe} / V_{fe}) x100 = (2/4) x100 = 50%", {})], **sans)


@figure("c072_1#2")
def entree_sortie(f):
    f.fit(38, 214, 38, "Signal d’entrée", color=RED)
    f.line((18, 80.5), (370, 80.5), w=2)
    _filled_head(f, 369, 80.5)
    f.text(389, 79, "T", size=27, bold=True)
    f.curve(lambda x: 80 + 28 * math.sin(2 * math.pi * (x - 12) / 108), 16, 331, n=200, stroke=RED, w=2)
    f.fit(540, 723, 40, "Signal de sortie", color=GREEN_SIG)
    f.line((464, 80.5), (794, 80.5), w=2)
    _filled_head(f, 793, 80.5)
    f.text(819, 79, "T", size=27, bold=True)

    def out(x):
        s = math.sin(2 * math.pi * (x - 466) / 106)
        return 80 - 28 * s if s >= 0 else 80 - 81 * s
    f.curve(out, 466, 784, n=300, stroke=GREEN_SIG, w=2)


@figure("c072_1#3")
def decomposition(f):
    f.fit(18, 415, 44, "Décomposition du signal de sortie")
    for y in (104.5, 235.5):
        f.line((18, y), (403, y), w=2)
        _filled_head(f, 402, y)
        f.text(423, y + 7.5, "T", size=27, bold=True)
    f.curve(lambda x: 104 - 53 * math.sin(2 * math.pi * (x - 41) / 108.5), 48, 390, n=240, stroke=RED, w=2)
    f.curve(lambda x: 236.5 - 26.5 * math.cos(2 * math.pi * (x - 48) / 52.8), 48, 390, n=300, stroke=BLUE, w=2)
    for x in (124.5, 179):
        f.line((x, 47), (x, 290), stroke="#00b050", w=1.6)
    f.fit(164, 449, 173, "Signal d’entrée amplifié")
    f.fit(217, 466, 283, "harmonique 2 généré")
    f.fit(217, 445, 317, "(avec TDH = 50%)")
    f.fit(14, 108, 388, "signaux")
    f.fit(14, 160, 421, "en phase (+)")
    f.fit(269, 363, 388, "signaux")
    f.fit(253, 422, 421, "en déphase (-)")
    for (x0, y0, x1, y1) in ((88, 356, 124, 293), (258, 375, 181, 293)):
        f.line((x0, y0), (x1, y1), stroke=BLUE, w=1.8)
        a = math.atan2(y1 - y0, x1 - x0)
        for da in (2.65, -2.65):
            f.line((x1, y1), (x1 + 11 * math.cos(a + da), y1 + 11 * math.sin(a + da)), stroke=BLUE, w=1.8)


@figure("c073_3#0")
def pll(f):
    T = 30
    lw = 3
    f.circle(132.5, 125, 47.5, lw=lw)
    f.text(132.5, 131, "VCO", size=T, anchor="c")
    f.line((25.5, 279), (25.5, 122.5), (85, 122.5), w=2)
    _chev(f, 85, 122.5, 1, 0, s=12, w=2)
    f.line((180, 122.5), (336, 122.5), w=2)
    _chev(f, 336, 122.5, 1, 0, s=12, w=2)
    f.line((238.5, 122.5), (238.5, 11), w=2)
    _chev(f, 238.5, 11, 0, -1, s=12, w=2)
    f.fit(112, 217, 36, "Sortie HF", color=RED)
    f.fit(9, 39, 94, "δU")
    f.fit(185, 205, 94, "δf")
    f.rect(336.5, 103.5, 193.5, 60, lw=3)
    f.text(433, 131, "Diviseur", size=T, anchor="c")
    for x in (356.5, 375.5, 393.5, 414.5, 433.5, 453.5, 472.5, 491.5):
        f.line((x, 86), (x, 103.5), w=1.6)
    f.fit(323, 542, 37, "Microprocesseur ou")
    f.fit(350, 517, 66, "roues codeuses")
    f.line((530, 122.5), (552, 122.5), (552, 259.5), (473, 259.5), w=2)
    _chev(f, 473, 259.5, -1, 0, s=12, w=2)
    f.rect(316.5, 237.5, 155.5, 78.5, lw=3)
    f.fit(318, 470, 267, "Comparateur")
    f.text(394, 298, "de phase", size=T, anchor="c")
    f.line((316, 276.5), (201, 276.5), w=2)
    _chev(f, 201, 276.5, -1, 0, s=12, w=2)
    f.fit(242, 274, 310, "δU")
    f.rect(82.5, 237.5, 116.5, 78.5, lw=3)
    f.text(141, 267, "Filtre", size=T, anchor="c")
    f.fit(88, 196, 298, "passe-bas")
    f.line((25.5, 278.5), (82.5, 278.5), w=2)
    f.line((136.5, 320), (136.5, 342), w=3)
    f.line((463, 400), (545, 400), (545, 296.5), (473, 296.5), w=2)
    _chev(f, 473, 296.5, -1, 0, s=12, w=2)
    f.fit(425, 540, 342, "Référence")
    f.circle(407.5, 398.5, 49, lw=lw)
    f.text(408, 407, "VXO", size=T, anchor="c")
    gnd(f, 124, 380, 134, 419)
    f.line((134, 400), (214, 400), w=1.6)
    f.line((214, 380), (214, 419), w=1.6)
    f.rect(233.5, 378.5, 40, 40, lw=3)
    f.text(253.5, 408, "Q", size=T, anchor="c")
    f.line((292.5, 380), (292.5, 419), w=1.6)
    f.line((293, 399), (359, 399), w=1.6)


@figure("c073_2#0")
def dds(f):
    T = 30
    gnd(f, 7, 28, 18, 81)
    f.line((18, 53), (59, 53), w=2)
    f.line((59, 28), (59, 82), w=2)
    f.rect(69.5, 26.5, 46, 44.5, lw=3.5)
    f.text(92.5, 62, "Q", size=T, anchor="c")
    f.line((126, 28), (126, 81), w=2)
    f.line((126, 52.5), (171.5, 52.5), w=2)
    f.fit(1, 127, 110, "Référence")
    f.rect(171.5, 6.5, 154, 152, lw=3.5)
    f.fit(207, 290, 77, "Micro-")
    f.fit(181, 316, 110, "processeur")
    for y in (24, 57, 84, 111, 138):
        f.line((325.5, y), (496.5, y), w=2.2)
    f.rect(496.5, 3.5, 199.5, 162, lw=3.5)
    f.fit(510, 684, 37, "Convertisseur")
    f.fit(527, 667, 72.5, "Numérique")
    f.fit(524, 670, 107.5, "Analogique")
    f.fit(565, 630, 143, "CNA")
    f.line((696, 84), (809.5, 84), w=2.2)
    f.rect(809.5, 48.5, 296, 65.5, lw=3.5)
    f.fit(877, 1025, 82, "Filtre Passe-bas")
    f.line((1105.5, 70), (1261, 70), w=2.4)
    f.line((1236, 55), (1261, 70), (1236, 85), w=2.4)
    f.fit(1292, 1413, 80, "Sortie HF", color=RED)
    for i, d in enumerate("3210012332"):
        f.text(80 + i * 31.4, 250, d, size=T, anchor="c")
    for x, y, d in ((473, 194, "3"), (502, 194, "3"), (538, 213, "2"), (557.5, 236, "1"), (587, 257, "0"),
                    (617, 257, "0")):
        f.text(x, y, d, size=T, anchor="c")
    xs = [394, 415.5, 438.5, 460.5, 529.5, 551.5, 574.5, 643.5, 665.5, 688.5, 757, 779.5, 802.5, 851]
    ys = [268, 246, 225, 203, 225, 246, 268, 246, 225, 203, 225, 246, 268]
    pts = []
    for i, y in enumerate(ys):
        pts += [(xs[i], y), (xs[i + 1], y)]
    f.line(pts, w=3, cap="b")
    f.line((851, 268), (915, 203.5), (986, 203.5), (1031, 248), w=3.4)
    f.curve(lambda x: 229 + 41.8 * math.cos(2 * math.pi * (x - 1057) / 192), 1026, 1295, n=200, w=1.4)


IU = {"i": 1, "u": 1}


def _vres(f, x, y0, y1, half=21.5, lw=3):
    f.rect(x - half, y0, 2 * half, y1 - y0, lw=lw)


@figure("c073_1#0")
def oscillateurs(f):
    T = 29
    w = 2.4
    # ---- Colpitts quartz oscillator (VXO)
    f.text(166, 38, "+", size=24, anchor="c")
    f.line((145.5, 51), (145.5, 91), w=w)
    _vres(f, 145.5, 91.5, 177)
    f.line((145.5, 177), (145.5, 298), w=w)
    _vres(f, 145.5, 298.5, 384)
    f.line((145.5, 384), (145.5, 438), w=w)
    gnd(f, 124, 438, 167, 448)
    f.line((81, 299), (81, 236.5), (311, 236.5), w=w)
    f.line((61, 298.5), (103, 298.5), w=w)
    f.rect(60.5, 319, 42, 43, lw=3.5)
    f.text(81.5, 352, "Q", size=26, anchor="c", italic=True)
    f.line((61, 380), (103, 380), w=w)
    f.line((81, 380), (81, 438), w=w)
    gnd(f, 61, 438, 103, 448)
    f.line((230.5, 236.5), (230.5, 277), w=w)
    for y in (277, 298.5, 340, 360):
        f.line((210, y), (252, y), w=w)
    f.line((230.5, 298.5), (230.5, 340), w=w)
    f.line((230.5, 360), (230.5, 438), w=w)
    gnd(f, 210, 438, 252, 448)
    f.line((230.5, 310.5), (375, 310.5), w=w)
    bjt(f, 337.5, 237.5, 42.5, 311, (358, 197.5), (366, 278), lw=3.4)
    gnd(f, 310, 218, 321, 259)
    f.line((366, 278), (375, 285), w=1.4)
    f.line((375, 285), (375, 336.5), w=w)
    _vres(f, 370.5, 336.5, 402)
    f.line((375, 402), (375, 438), w=w)
    gnd(f, 350, 438, 392, 449)
    f.line((358, 197.5), (358, 112.5), (272.5, 112.5), w=w)
    f.line((251.5, 112.5), (209, 112.5), (209, 70), w=w)
    _humps(f, 209, 315.5, 70, 4, 21, w=w)
    f.line((315.5, 70), (315.5, 112.5), w=w)
    f.line((251.5, 92), (251.5, 134), w=w)
    f.line((272.5, 92), (272.5, 134), w=w)
    f.line((188, 50), (188, 91.5), (209, 91.5), w=1.6)
    f.line((272.5, 50), (272.5, 29), (401, 29), w=1.6, stroke="#606060")
    f.fit(352, 470, 58, "Sortie HF", italic=True, color=RED)
    # ---- Clapp VFO
    gnd(f, 523, 196, 533, 238)
    f.line((533, 215), (570.5, 215), w=w)
    _humps(f, 570.5, 698.5, 195, 5, 20, w=1.8)
    f.line((570.5, 195), (570.5, 236.5), (592, 236.5), w=w)
    f.line((698.5, 195), (698.5, 236.5), (677, 236.5), w=w)
    f.line((613, 236.5), (656, 236.5), w=w)
    for x in (592, 613, 656, 677):
        f.line((x, 217), (x, 258), w=w)
    for x0, y0, x1, y1 in ((571, 257.5, 631, 218), (635, 256, 695, 218)):
        f.line((x0, y0), (x1, y1), w=1.8)
        a = math.atan2(y1 - y0, x1 - x0)
        for da in (2.6, -2.6):
            f.line((x1, y1), (x1 + 13 * math.cos(a + da), y1 + 13 * math.sin(a + da)), w=1.8)
    f.line((634.5, 236.5), (634.5, 298.5), (826, 298.5), w=w)
    f.line((698.5, 215), (736, 215), w=w)
    bjt(f, 761, 216.5, 42.5, 736, (783.5, 175), (793, 249), lw=3.4)
    gnd(f, 736, 196, 746, 238)
    f.line((793, 249), (801.5, 257), w=1.4)
    f.line((783.5, 175), (783.5, 135.5), w=w)
    _vres(f, 784, 50, 135.5)
    f.line((783.5, 31), (783.5, 50), w=w)
    f.text(772.5, 30, "+", size=24, anchor="c")
    f.line((783.5, 153), (826, 153), w=w)
    f.line((826, 135), (826, 176), w=w)
    f.line((847.5, 135), (847.5, 176), w=w)
    f.line((848, 153), (885, 153), w=w)
    gnd(f, 885, 134, 895, 176)
    f.text(830, 122, "Cd", size=T, italic=True)
    f.line((801.5, 257), (801.5, 337), w=w)
    _vres(f, 796, 337.5, 423)
    f.line((801.5, 423), (801.5, 438), w=w)
    gnd(f, 776, 438, 817, 449)
    f.line((826, 279), (826, 320), w=w)
    f.line((847.5, 279), (847.5, 320), w=w)
    f.line((848, 298.5), (890, 298.5), w=w)
    f.fit(872, 941, 286, "Sortie", italic=True, color=RED)
    f.fit(872, 912, 322, "HF", italic=True, color=RED)
    f.fit(575, 624, 288, "CV1", italic=True)
    f.fit(660, 710, 288, "CV2", italic=True)
    f.text(873, 25, "Cd =", size=T, italic=True)
    f.fit(873, 1032, 59, "condensateur", italic=True)
    f.fit(873, 1044, 92, "de découplage", italic=True)
    # ---- Hartley VCO with varicaps
    f.text(1093, 58, "+", size=24, anchor="c")
    f.line((1126, 49.5), (1190, 49.5), w=w)
    _humps(f, 1189, 1252, 49.5, 3, 20, w=w)
    f.line((1188, 19), (1255, 19), w=2.6, dash=[2.4, 2.6])
    f.line((1252, 47.5), (1306.5, 47.5), (1306.5, 182), w=w)
    f.fit(1152, 1212, 78, "Choc", italic=True)
    f.line((1306.5, 83.5), (1333, 83.5), w=w)
    f.line((1333, 63), (1333, 105), w=w)
    f.line((1354.5, 63), (1354.5, 105), w=w)
    f.line((1355, 83), (1370, 83), w=w)
    gnd(f, 1370, 63, 1381, 105)
    f.fit(1337, 1374, 50, "Cd", italic=True)
    _humps(f, 1039, 1209, 175, 7, 20, w=w)
    f.line((1039, 175), (1039, 237.5), (1053, 237.5), w=w)
    f.line((1209, 175), (1209, 237.5), (1196, 237.5), w=w)
    f.poly([(1053, 223), (1080, 237), (1053, 251)], stroke=None, fill=BLACK)
    f.line((1081, 217), (1081, 258), w=w)
    f.line((1103, 217), (1103, 258), w=w)
    f.line((1145, 218), (1145, 258), w=w)
    f.line((1103, 236.5), (1145, 236.5), w=w)
    f.line((1167, 218), (1167, 258), w=w)
    f.poly([(1196, 223), (1168, 237), (1196, 251)], stroke=None, fill=BLACK)
    f.fit(1042, 1089, 286, "Dv1", italic=True)
    f.fit(1127, 1175, 286, "Dv2", italic=True)
    f.line((1124, 236.5), (1124, 379), w=w)
    f.line((1110, 352), (1124, 379), (1138, 352), w=w)
    f.rect(1082.5, 380.5, 86, 42.5, lw=2.6)
    f.line((1019, 402), (1082.5, 402), w=w)
    f.line((1168.5, 402), (1225, 402), w=w)
    gnd(f, 1225, 382, 1236, 424)
    f.text(986, 409, "+", size=24, anchor="c")
    f.fit(960, 1223, 452, "Tension de commande", italic=True)
    f.line((1166.5, 151), (1166.5, 112), (1231, 112), (1231, 175), w=w)
    f.line((1209, 195), (1266, 195), w=w)
    f.circle(1295, 195, 42.5, lw=3.4)
    f.poly([(1266, 178), (1288, 195), (1266, 212)], stroke=None, fill=BLACK)
    gnd(f, 1289, 173, 1301, 216)
    f.line((1231, 216), (1231, 277.5), (1316, 277.5), w=w)
    f.line((1316, 258), (1316, 299), w=w)
    f.line((1337, 258), (1337, 299), w=w)
    f.line((1337, 277.5), (1358, 277.5), w=w)
    f.fit(1361, 1432, 267, "Sortie", italic=True, color=RED)
    f.fit(1361, 1403, 303, "HF", italic=True, color=RED)
    f.line((1301, 210), (1307, 210), (1307, 314), w=1.4)
    f.rect(1280.5, 314.5, 42, 86, lw=3)
    f.line((1307, 400.5), (1307, 442), w=1.4)
    gnd(f, 1281, 442, 1323, 453)
    # ---- captions
    caps = [
        (493, 28, 459, [("Oscillateur à Quartz (VXO), système", I_)]),
        (528, 25, 460, [("Colpitts", IU), (" fréquemment utilisé avec les", I_)]),
        (562, 12, 475, [("quartz. Très stable et facile à mettre au", I_)]),
        (598, 12, 470, [("point, il offre la possibilité d'utiliser le", I_)]),
        (632, 6, 480, [("circuit LC de sortie en multiplicateur de", I_)]),
        (667, 106, 371, [("fréquence (voir § 7.6).", I_)]),
        (493, 553, 870, [("VFO système ", I_), ("Clapp", IU), (", la HF", I_)]),
        (528, 559, 860, [("est réinjectée par le point", I_)]),
        (562, 554, 863, [("milieu du CV. CV1 et CV2", I_)]),
        (598, 566, 851, [("sont les deux cages d'un", I_)]),
        (632, 577, 840, [("condensateur variable", I_)]),
        (667, 586, 831, [("mécaniquement liées", I_)]),
        (519, 932, 1421, [("VCO à Varicap système ", I_), ("Hartley", IU), (" construit", I_)]),
        (555, 947, 1402, [("autour d’un transistor FET. La HF est", I_)]),
        (589, 917, 1432, [("réinjectée par la bobine. La bobine de choc", I_)]),
        (624, 906, 1444, [("et le condensateur de découplage, Cd, évitent", I_)]),
        (659, 925, 1423, [("que la H.F. \"remonte\" dans l'alimentation", I_)]),
    ]
    for y, x0, x1, parts in caps:
        rfit(f, x0, x1, y, parts, cap=33)


def _blue_tip(f, x, y, dx=1, dy=0, s=10, color=BLUE):
    px, py = -dy, dx
    f.poly([(x, y), (x - dx * s + px * s * 0.45, y - dy * s + py * s * 0.45),
            (x - dx * s * 0.7, y - dy * s * 0.7),
            (x - dx * s - px * s * 0.45, y - dy * s - py * s * 0.45)], stroke=None, fill=color)


@figure("c074_1#0")
def chaine_multiplicateur(f):
    sans = dict(family="sans")
    f.rich(0, 21, [("Exemple", {"u": 1, "b": 1, "color": MAROON}), (" : quel est l’étage marqué « ? »", {})], size=25,
           family="sans")
    f.rect(4, 44.5, 183, 94, lw=4)
    f.rect(239.5, 44.5, 209, 94, lw=4)
    f.rect(500.5, 44.5, 79, 98, lw=4)
    for x0, x1 in ((189, 241), (450, 502), (581, 631)):
        f.line((x0, 97), (x1 - 15, 97), w=2.6)
        f.poly([(x1 - 16, 89), (x1, 97), (x1 - 16, 105)], stroke=None, fill=BLACK)
    f.fit(33, 157, 81, "Oscillateur", **sans)
    f.fit(47, 143, 111, "3,5 MHz", **sans)
    f.fit(268, 421, 81, "Multiplicateur", **sans)
    f.fit(326, 361, 111, "x 2", **sans)
    f.text(540, 106, "?", size=26, anchor="c", **sans)
    f.fit(609, 698, 79, "21 MHz", **sans)


@figure("c075_1#0")
def ampli_op_ideal(f):
    T = 31
    f.poly([(315, 27.5), (550, 106), (315, 158)], w=4)
    f.line((117, 52.5), (315, 52.5), w=3)
    f.line((117, 132), (315, 132), w=3)
    _blue_tip(f, 250, 52.5, s=12)
    _blue_tip(f, 250, 132, s=12)
    f.text(333, 58, "–", size=26, anchor="c")
    f.text(333, 136, "+", size=26, anchor="c")
    f.line((419.5, 1), (419.5, 61), w=2.4)
    f.line((419.5, 134), (419.5, 196), w=2.4)
    rd = dict(stroke=RED, w=1.6, dash=[1.6, 2])
    f.line((419.5, 62), (419.5, 90), **rd)
    f.line((419.5, 119), (419.5, 133), **rd)
    f.line((419.5, 106), (548, 106), **rd)
    f.circle(419.5, 91.5, 5, stroke=None, fill=RED)
    f.circle(419.5, 118, 5, stroke=None, fill=RED)
    f.line((394, 87), (394, 120), w=1.6, dash=[1.6, 2])
    f.line((388, 93), (394, 85), (400, 93), w=1.6)
    f.line((388, 114), (394, 122), (400, 114), w=1.6)
    f.line((550, 106), (717, 106), w=3)
    f.fit(430, 511, 30, "Alim +")
    f.fit(430, 510, 172, "Alim –")
    f.text(533, 86, "δ", size=27)
    f.text(5, 57, "Z_{e–} = ∞", size=T)
    f.text(5, 136, "Z_{e+} = ∞", size=T)
    f.text(109, 100, "I_{e–} = 0", size=T)
    f.text(109, 162, "I_{e+} = 0", size=T)
    f.fit(736, 974, 112, "V_{S} = (V_{e+} – V_{e–}) x ∞")
    f.fit(684, 933, 160, "Gain en tension infini")


@figure("c075_2#0")
def ampli_inverseur(f):
    T = 31
    f.rect(33.5, 5.5, 41, 41, stroke=RED, lw=2.4)
    f.text(53.5, 36, "E", size=T, anchor="c", color=RED)
    f.rect(915.5, 6.5, 41.5, 42, stroke=RED, lw=2.4)
    f.text(936, 38, "S", size=T, anchor="c", color=RED)
    f.line((81, 29), (444, 29), w=2.4)
    f.line((460, 29), (909, 29), w=2.4)
    f.rect(268, 7, 103.5, 40.5, fill="#ffffff", lw=3.6)
    f.text(319.5, 38, "R1", size=T, anchor="c")
    f.rect(620, 7, 103.5, 40.5, fill="#ffffff", lw=3.6)
    f.text(671, 38, "R2", size=T, anchor="c")
    f.circle(452, 30, 7.5, stroke=BLACK, fill=BLUE, lw=1.6)
    _blue_tip(f, 225, 29, s=10)
    _blue_tip(f, 556, 29, s=10)
    f.text(210, 58, "I_{R1}", size=T)
    f.text(541, 58, "I_{R2}", size=T)
    for x, xb in ((81.5, (61, 102)), (889, (869, 909))):
        f.line((x, 186), (x, 43), stroke=RED, w=2.4)
        f.line((x - 9, 60), (x, 43), (x + 9, 60), stroke=RED, w=2.4)
        gnd(f, xb[0], 186, xb[1], 196)
    f.text(3, 100, "U_{E}", size=T)
    f.line((454, 37), (454, 135.5), (578, 135.5), w=2.4)
    _blue_tip(f, 491, 135.5, s=10)
    f.text(491, 128, "I_{e–}", size=T)
    f.rect(461.5, 41.5, 40, 41, stroke=BLUE, lw=2.4)
    f.text(481.5, 72, "N", size=T, anchor="c", color=BLUE)
    f.line((288.5, 186), (288.5, 123), (430, 43), stroke=BLUE, w=2.4)
    a = math.atan2(43 - 123, 430 - 288.5)
    for da in (2.6, -2.6):
        f.line((430, 43), (430 + 17 * math.cos(a + da), 43 + 17 * math.sin(a + da)), stroke=BLUE, w=2.4)
    gnd(f, 268, 186, 309, 196)
    f.text(230, 154, "U_{N}", size=T)
    f.rect(382.5, 133.5, 40, 42, stroke=BLUE, lw=2.4)
    f.text(402.5, 164, "P", size=T, anchor="c", color=BLUE)
    gnd(f, 366, 157, 377, 198)
    f.line((377, 179), (578, 179), w=2.4)
    _blue_tip(f, 491, 179, s=10)
    f.text(491, 171, "I_{e+}", size=T)
    f.poly([(578.5, 92.5), (765, 154), (578.5, 211)], w=3.6)
    f.text(596, 143, "–", size=26, anchor="c")
    f.text(596, 183, "+", size=26, anchor="c")
    f.text(689, 166, "δ", size=27)
    f.line((765, 154), (806, 154), (806, 29), w=2.4)
    nb = dict(b=1, color=NAVY)
    f.fit(914, 1148, 103, "U_{S} = – U_{E}.(R2 / R1)", bold=True, color=NAVY)
    f.fit(950, 1035, 135, "= U_{E}.G", bold=True, color=NAVY)
    f.fit(914, 1099, 170, "G = – (R2 / R1)", bold=True, color=NAVY)


@figure("c074_2#0")
def melangeurs(f):
    w = 2.2
    T = 29
    # ---- dual-gate MOS-FET mixer
    gnd(f, 162.5, 22.5, 204, 35)
    f.line((183.5, 35), (183.5, 50), w=w)
    f.rect(162, 50, 42, 84, lw=2.4)
    f.line((183.5, 134), (183.5, 174), w=w)
    f.text(244, 18, "+", size=24, anchor="c")
    f.line((252, 29), (252, 52), w=w)
    f.rect(232, 52, 42, 84, lw=2.4)
    f.line((235, 116), (271, 75), w=1.6)
    f.line((259, 78), (271, 75), (266, 87), w=1.6)
    f.line((252, 136), (252, 174), w=w)
    for y in (174, 233.5):
        f.line((113, y), (129, y), w=w)
        f.line((129, y - 20), (129, y + 21), w=w)
        f.line((149, y - 20), (149, y + 21), w=w)
        f.line((149, y), (293, y), w=w)
    f.fit(12, 110, 182, "f_{1} = Osc", italic=True, color=RED)
    f.fit(20, 110, 241, "f_{2} = HF", italic=True, color=RED)
    f.line((293.5, 152), (293.5, 195), w=w)
    f.line((293.5, 213), (293.5, 252), w=w)
    gnd(f, 308, 154, 320, 257)
    f.circle(325, 207.5, 74, lw=2.4)
    f.line((320, 174), (356.5, 174), (356.5, 91.5), (409, 91.5), w=w)
    f.poly([(322, 214), (343, 201), (343, 227)], stroke=None, fill=BLACK)
    f.line((343, 214), (356.5, 214), (356.5, 294.5), w=w)
    f.line((320, 234), (356.5, 234), w=w)
    f.line((183.5, 233.5), (183.5, 294.5), w=w)
    f.rect(161.5, 294.5, 42.5, 62.5, lw=2.4)
    f.line((183.5, 357), (183.5, 369), w=w)
    gnd(f, 161.5, 369, 204, 379)
    f.rect(335.5, 294.5, 42, 62.5, lw=2.4)
    f.line((356.5, 357), (356.5, 369), w=w)
    gnd(f, 335, 369, 378, 379)
    f.fit(209, 333, 307, "MOS-FET", italic=True)
    # output tank and coupling (MOS-FET)
    _humps(f, 409, 490, 47.5, 3, 12, w=1.8)
    f.line((409, 47.5), (409, 100), (429, 100), w=w)
    f.line((429, 78), (429, 121), w=w)
    f.line((449.5, 78), (449.5, 121), w=w)
    f.line((449.5, 100), (490, 100), (490, 47.5), w=w)
    f.line((490, 78), (551, 78), w=w)
    f.text(557, 86, "+", size=24, anchor="c")
    f.fit(452, 468, 80, "L", italic=True)
    f.fit(453, 471, 130, "C", italic=True)
    gnd(f, 382, 2.5, 391, 30)
    f.line((391, 14), (410, 14), w=w)
    _humps(f, 410, 453, 14, 2, 10, down=True, w=1.8)
    f.line((453, 14), (520, 14), w=w)
    f.line((508, 6), (520, 14), (508, 22), w=w)
    f.fit(528, 598, 18, "Sortie", italic=True, color=RED)
    # ---- J-FET mixer
    gnd(f, 775, 3, 782, 32)
    f.line((775, 14), (730, 14), w=w)
    _humps(f, 688, 730, 14, 2, 10, down=True, w=1.8)
    f.line((688, 14), (610, 14), w=w)
    f.line((622, 6), (610, 14), (622, 22), w=w)
    _humps(f, 683, 767, 50, 4, 12, w=1.8)
    f.line((630, 69.5), (683, 69.5), w=w)
    f.text(616, 77, "+", size=24, anchor="c")
    f.line((683, 50), (683, 100), (704.5, 100), w=w)
    f.line((704.5, 80), (704.5, 122), w=w)
    f.line((724.5, 80), (724.5, 122), w=w)
    f.line((724.5, 100), (767, 100), w=w)
    f.line((767, 50), (767, 162), (732, 162), w=w)
    f.fit(727, 743, 78, "L", italic=True)
    f.fit(728, 746, 128, "C", italic=True)
    f.circle(718, 198, 59.5, lw=2.4)
    gnd(f, 720, 158, 732, 233)
    f.line((595, 226), (618, 226), w=w)
    f.line((618, 205), (618, 248), w=w)
    f.line((631.5, 205), (631.5, 248), w=w)
    f.line((631.5, 226), (697, 226), w=w)
    f.poly([(697, 213), (720, 226.5), (697, 240)], stroke=None, fill=BLACK)
    f.fit(580, 616, 215, "RF", italic=True, color=RED)
    f.line((732, 226), (772.5, 226), (772.5, 289.5), w=w)
    f.line((772.5, 263), (812, 263), w=w)
    f.line((812, 243), (812, 285), w=w)
    f.line((825, 243), (825, 285), w=w)
    f.line((825, 263), (855, 263), w=w)
    f.fit(830, 870, 254, "Osc", italic=True, color=RED)
    f.line((651, 226), (651, 285.5), w=w)
    f.rect(630.5, 285.5, 42.5, 62.5, lw=2.4)
    f.line((651.5, 348), (651.5, 360), w=w)
    gnd(f, 631, 360, 673, 371)
    f.rect(750, 289.5, 42, 62.5, lw=2.4)
    f.line((771.5, 352), (771.5, 358), w=w)
    gnd(f, 751, 358, 792, 369)
    f.fit(679, 756, 282, "J-FET", italic=True)
    # ---- centre text
    for y, x0, x1, t in ((174, 414, 567, "Les circuits de"), (205, 436, 548, "sortie sont"),
                         (235, 411, 574, "accordés sur la"), (266, 425, 552, "fréquence à"),
                         (290, 440, 541, "conserver"), (323, 435, 551, "(Osc ± HF"),
                         (352, 441, 540, "ou f_{1} ± f_{2})")):
        f.fit(x0, x1, y, t, italic=True, max_size=30)
    # ---- mixer output
    f.fit(977, 1340, 81, "Signal à la sortie du mélangeur")
    f.fit(983, 1333, 114, "(avant le circuit bouchon LC)")
    f.line((936, 212.5), (1387, 212.5), w=2.2)
    _filled_head(f, 1386, 212.5, length=15, half=7.5)
    f.text(1398, 198, "T", size=26)
    blue = lambda x: 217 - 27 * math.cos(2 * math.pi * (x - 1001) / 250)
    f.curve(blue, 936, 1376, n=200, stroke="#4040ff", w=1.8, dash=[2, 1.5])
    f.curve(lambda x: blue(x) - 54 * math.sin(2 * math.pi * (x - 951) / 51.7), 936, 1378, n=600, stroke=RED, w=2.2)
    f.line((885, 338.5), (948, 338.5), stroke="#ff6060", w=3)
    f.line((885, 365), (948, 365), stroke="#4040ff", w=2.4, dash=[2, 1.5])
    f.text(965, 346, "Résultante Osc (f_{1}) + HF (f_{2}) = f_{max}", size=27)
    f.text(965, 372, "Résultante Osc (f_{1}) – HF (f_{2}) = f_{min}", size=27)


def _opamp_small(f, x_left, y_top, y_bot, x_apex, y_minus, y_plus, w=2.4):
    yc = (y_top + y_bot) / 2
    f.poly([(x_left, y_top), (x_apex, yc), (x_left, y_bot)], w=w)
    f.line((x_left + 10, y_minus), (x_left + 24, y_minus), w=1.8)
    f.line((x_left + 10, y_plus), (x_left + 24, y_plus), w=1.8)
    f.line((x_left + 17, y_plus - 7), (x_left + 17, y_plus + 7), w=1.8)
    return yc


def _gain_triangle(f, x0, x1, y_base, apex, circle, labels):
    cx, cy, r = circle
    f.circle(cx, cy, r, stroke=None, fill="#c0c0c0")
    f.poly([(x0, y_base), (apex[0], apex[1]), (x1, y_base)], stroke=BLUE, w=2.2)
    for x, y, t in labels:
        f.text(x, y, t, size=27)


@figure("c075_3#0")
def gain_inverseur(f):
    sans = dict(family="sans")
    f.text(4, 43, "E", size=26, color=NAVY, **sans)
    f.text(296, 43, "S", size=26, color=NAVY, **sans)
    f.line((39, 32), (54, 32), w=2)
    f.rect(54, 10.5, 62, 41.5, lw=2.2)
    f.text(85, 38, "R1", size=24, anchor="c", **sans)
    f.line((116, 32), (182, 32), w=2)
    f.rect(182, 11, 62, 42, lw=2.2)
    f.text(213, 38, "R2", size=24, anchor="c", **sans)
    f.line((244, 32), (290, 32), w=2)
    f.line((138, 32), (138, 88), (159.5, 88), w=2)
    yc = _opamp_small(f, 159.5, 66, 151, 242, 89, 129)
    f.line((242, yc), (264, yc), (264, 32), w=2)
    gnd(f, 23, 109, 33, 143)
    f.line((33, 129), (159.5, 129), w=2)
    f.fit(285, 432, 97, "R1 = 5000 Ω", **sans)
    f.fit(285, 416, 129, "R2 = 25 kΩ", **sans)
    _gain_triangle(f, 479, 636, 135.5, (557.5, 5), (595.5, 123.5, 37.5),
                   ((540, 68, "-R2"), (518, 120, "R1"), (576, 119, "G")))


@figure("c075_3#1")
def triangle_gain(f):
    _gain_triangle(f, 4, 162, 134.5, (83, 3), (120.5, 122.5, 38),
                   ((62, 67, "-R2"), (40, 119, "R1"), (102, 119, "G")))


@figure("c075_3#2")
def exemple_inverseur(f):
    sans = dict(family="sans")
    f.fit(8, 91, 48, "– 0,5 V", **sans)
    f.line((110, 28), (131, 28), w=2)
    f.rect(131, 7, 62, 42, lw=2.2)
    f.fit(143, 183, 35, "100", **sans)
    f.line((193, 28), (256, 28), w=2)
    f.rect(256, 7, 63, 42, lw=2.2)
    f.fit(268, 308, 35, "500", **sans)
    f.line((319, 28), (360, 28), w=2)
    f.text(364, 37, "S", size=26, **sans)
    f.line((214.5, 28), (214.5, 112), (235, 112), w=2)
    yc = _opamp_small(f, 235, 91, 170, 330, 112, 152)
    f.line((330, yc), (340.5, yc), (340.5, 28), w=2)
    gnd(f, 100, 143, 110, 168)
    f.line((110, 154.5), (235, 154.5), w=2)
    _gain_triangle(f, 397, 553, 155.5, (475, 24), (483, 73, 36),
                   ((462, 87, "U_{S}"), (437, 139, "U_{E}"), (498, 139, "G")))


@figure("c076_1#0")
def table_nand(f):
    T = 28
    f.rect(2.5, 2.5, 212, 141.5, lw=2)
    f.line((3, 3), (73, 73), w=1.8)
    f.line((73, 73), (214.5, 73), w=1.8)
    f.line((59, 104.5), (212, 104.5), w=1.8)
    f.line((73, 73), (73, 144), w=1.8)
    f.line((144, 50), (144, 144), w=1.8)
    f.fit(89, 179, 37, "Entrée A", italic=True)
    f.text(38, 87.5, "Entrée B", size=T, italic=True, rot=-90, anchor="c", va="middle")
    for x, y, t in ((107.5, 67.5, "1"), (180, 67.5, "0"), (62, 97, "1"), (108, 97, "0"), (180, 97, "0"),
                    (62, 128, "0"), (108, 128, "0"), (180, 128, "1")):
        f.text(x, y, t, size=T, italic=True, anchor="c")


def _hyst(f, x0, y0, w=2.2):
    f.line((x0, y0), (x0 + 37, y0), w=w)
    f.line((x0 + 18, y0), (x0 + 38, y0 + 37.5), w=w)
    f.line((x0 + 37, y0), (x0 + 56, y0 + 37.5), w=w)
    f.line((x0 + 38, y0 + 37.5), (x0 + 73, y0 + 37.5), w=w)


def _and_body(f, x_bar, x_arc, y_top, y_bot, x_in=None, w=2.4):
    r = (y_bot - y_top) / 2
    cy = (y_top + y_bot) / 2
    x_in = x_bar if x_in is None else x_in
    f.line((x_in, y_top), (x_arc, y_top), w=w)
    f.line((x_in, y_bot), (x_arc, y_bot), w=w)
    f.line((x_bar, y_top), (x_bar, y_bot - 3), w=w)
    f.arc(x_arc, cy, r, r, -90, 90, w=w)
    return x_arc + r, cy


@figure("c076_2#0")
def portes_trigger(f):
    w = 2.4
    # AND gate
    xo, yo = _and_body(f, 42.5, 135, 54.5, 132.5, x_in=6)
    _hyst(f, 62, 74.5)
    f.line((xo, 94), (209, 94), w=w)
    f.fit(55, 148, 50, "porte ET", italic=True)
    # inverter
    f.line((182, 73.5), (238, 73.5), w=w)
    f.poly([(237, 39), (400, 71.5), (237, 130)], w=w)
    f.circle(411, 71.5, 10.5, lw=w)
    f.line((422, 71), (460, 71), w=w)
    _hyst(f, 256, 54)
    f.fit(282, 380, 141, "inverseur", italic=True)
    # OR gate
    f.line((455, 62.5), (587, 62.5), (640, 101.5), (586, 139.5), (455, 139.5), w=w)
    f.spline([(470, 62.5), (497, 75), (511, 101), (497, 127), (470, 139.5)], w=w)
    f.line((640, 101.5), (677, 101.5), w=w)
    _hyst(f, 529, 82)
    f.fit(487, 585, 50, "porte OU", italic=True)
    # NAND oscillator
    xo, yo = _and_body(f, 128.5, 202, 184.5, 262.5, x_in=86.5)
    f.circle(250, 224.5, 8.5, lw=w)
    _hyst(f, 148, 204.5)
    f.line((86.5, 184.5), (86.5, 277.5), (364.5, 277.5), w=w)
    f.line((258.5, 225), (280, 225), (280, 179), (409, 179), w=w)
    f.line((317.5, 179), (317.5, 207.5), w=w)
    f.rect(295, 207.5, 38, 57, lw=w)
    f.fit(299, 314, 237, "R", italic=True)
    f.line((318.5, 264.5), (318.5, 277.5), w=w)
    f.line((364.5, 255), (364.5, 291), w=w)
    f.line((388, 255), (388, 291), w=w)
    f.line((388, 277.5), (406, 277.5), w=w)
    gnd(f, 406, 255, 416, 291)
    f.fit(369, 385, 259, "C", italic=True)
    sq = [(296, 173)]
    for x0 in (313.5, 350.5, 388):
        sq += [(x0, 173), (x0, 154.5), (x0 + 19, 154.5), (x0 + 19, 173)]
    f.line(sq, stroke=RED, w=2.2)
    f.fit(416, 428, 168, "S", italic=True)
    for y, x0, x1, t in ((199, 480, 535, "porte"), (230, 446, 538, "NON-ET"), (261, 430, 536, "montée en"),
                         (291, 427, 536, "oscillateur")):
        f.fit(x0, x1, y, t, italic=True)


def _oa(f, x_left, y_top, y_bot, apex, minus, plus, w=3):
    f.poly([(x_left, y_top), apex, (x_left, y_bot)], w=w)
    f.line((minus[0] - 7, minus[1]), (minus[0] + 7, minus[1]), w=2)
    f.line((plus[0] - 7, plus[1]), (plus[0] + 7, plus[1]), w=2)
    f.line((plus[0], plus[1] - 7), (plus[0], plus[1] + 7), w=2)


def _hbox(f, x0, y0, x1, y1, label=None, lx=None, ly=None, size=27, lw=2.4):
    f.rect(x0, y0, x1 - x0, y1 - y0, lw=lw)
    if label:
        f.text(lx, ly, label, size=size, italic=True)


@figure("c076_3#0")
def montages_aop(f):
    w = 2.4
    T = 29
    f.rect(4, 4, 1406, 385, lw=1.6)
    f.line((5, 41), (1410, 41), w=1.6)
    for x in (275, 566, 837, 1108):
        f.line((x, 4), (x, 389), w=1.6)
    for x0, x1, t in ((52, 226, "Non inverseur"), (342, 499, "Soustracteur"), (632, 773, "Intégrateur"),
                      (914, 1031, "Filtre RC"), (1166, 1352, "Ampli classe D")):
        f.fit(x0, x1, 32, t, italic=True)
    # ---- non-inverting
    gnd(f, 15, 70, 26, 111)
    f.line((26, 97), (41.5, 97), w=w)
    _hbox(f, 41.5, 68.5, 105.5, 111, "R1", 45, 100)
    f.line((105.5, 97), (168.5, 97), w=w)
    _hbox(f, 168.5, 68.5, 232, 111, "R2", 172, 100)
    f.line((232, 97), (269, 97), w=w)
    f.text(245, 82, "S", size=T, italic=True, color=RED)
    f.line((121, 97), (121, 175), (147.5, 175), w=w)
    _oa(f, 147.5, 152.5, 237.5, (231.5, 195), (165, 175), (167.5, 207.5))
    f.line((231.5, 195), (253, 195), (253, 97), w=w)
    f.line((22, 216), (147.5, 216), w=w)
    f.text(22, 197, "E", size=T, italic=True, color=RED)
    f.fit(32, 245, 345, "G = (R2 / R1) + 1", bold=True, italic=True, color=NAVY)
    f.fit(80, 205, 376, "U_{S} = U_{E}.G", bold=True, italic=True, color=NAVY)
    # ---- subtractor
    f.text(292, 92, "E–", size=T, italic=True, color=RED)
    f.line((298, 98), (333, 98), w=w)
    _hbox(f, 333, 68.5, 397, 112, "R", 336, 101)
    f.line((397, 100), (441, 100), w=w)
    _hbox(f, 441, 73.5, 504.5, 117, "R", 446, 106)
    f.line((504.5, 102), (557, 102), w=w)
    f.text(540, 90, "S", size=T, italic=True, color=RED)
    f.line((409, 100), (409, 156), (435, 156), w=w)
    _oa(f, 435, 130, 213, (514, 181.5), (452, 152), (452.5, 185))
    f.line((514, 181.5), (541, 181.5), (541, 102), w=w)
    f.text(292, 175, "E+", size=T, italic=True, color=RED)
    f.line((305, 182), (333, 182), w=w)
    _hbox(f, 333, 155.5, 397, 199, "R", 336, 188)
    f.line((397, 182), (435, 182), w=w)
    f.line((411.5, 182), (411.5, 263), (397, 263), w=w)
    _hbox(f, 333, 245.5, 397, 289, "R", 336, 278)
    gnd(f, 315, 246, 325, 300)
    f.line((325, 265), (333, 265), w=w)
    f.fit(287, 552, 345, "G = -1 (si R constant)", italic=True)
    f.fit(315, 545, 376, "U_{S} = (U_{E+}) - (U_{E-})", italic=True)
    # ---- integrator
    f.text(572, 110, "E", size=T, italic=True, color=RED)
    f.line((573, 84), (605, 84), w=w)
    _hbox(f, 605, 64.5, 669, 107.5, "R", 627, 96)
    f.line((669, 84), (741, 84), w=w)
    f.line((741, 64), (741, 106), w=w)
    f.line((762, 64), (762, 106), w=w)
    f.line((762, 84), (826, 84), w=w)
    f.text(807, 79, "S", size=T, italic=True, color=RED)
    f.text(767, 115, "C", size=T, italic=True)
    f.line((684, 84), (684, 135), (710, 135), w=w)
    _oa(f, 710, 112.5, 190, (790, 137.5), (728, 132), (730, 165))
    f.line((790, 137.5), (816, 137.5), (816, 84), w=w)
    gnd(f, 611, 142, 622, 197)
    f.line((622, 164), (710, 164), w=w)
    for y, x0, x1, t in ((275, 597, 805, "T(s) = R(Ω).C(F)"), (309, 597, 807, "Au bout de 5T, le"),
                         (343, 585, 820, "condensateur C est"), (377, 597, 807, "chargé : U_{S} ≈ U_{E}")):
        f.fit(x0, x1, y, t, italic=True)
    # ---- RC filter
    f.line((877.5, 110), (877.5, 89.5), (983, 89.5), w=w)
    _hbox(f, 983, 68, 1046.5, 111, "R", 1006, 100)
    f.line((1046.5, 89), (1089, 89), w=w)
    f.text(1057, 77, "S", size=T, italic=True, color=RED)
    f.line((858, 110.5), (899, 110.5), w=w)
    f.line((858, 132), (899, 132), w=w)
    f.text(902, 129, "C", size=T, italic=True)
    f.line((877.5, 132), (877.5, 152), w=w)
    f.rect(856.5, 152, 41.5, 65, lw=w)
    f.text(877, 184.5, "R", size=T, italic=True, rot=-90, anchor="c", va="middle")
    f.line((877.5, 217), (877.5, 232), w=w)
    gnd(f, 858, 232, 899, 243)
    f.line((941, 89.5), (941, 215), (962, 215), w=w)
    f.line((941, 152.5), (1004, 152.5), w=w)
    f.line((1004, 133), (1004, 174), w=w)
    f.line((1025, 133), (1025, 174), w=w)
    f.line((1025, 152.5), (1067.5, 152.5), w=w)
    f.text(1030, 182, "C", size=T, italic=True)
    f.line((1067.5, 89), (1067.5, 237.5), (1047.5, 237.5), w=w)
    _oa(f, 962, 196, 279, (1047.5, 237.5), (979.5, 218.5), (981, 250))
    f.line((921, 258.5), (962, 258.5), w=w)
    f.text(921, 251, "E", size=T, italic=True, color=RED)
    f.fit(867, 1075, 309, "Filtre de bande 2", italic=True)
    f.fit(850, 1095, 343, "cellules (12 dB/oct.)", italic=True)
    f.fit(855, 1090, 375, "f(Hz)=1/[2π.R(Ω).C(F)]", italic=True)
    # ---- class D
    f.line((1121, 81.5), (1218, 81.5), w=w)
    f.line((1209, 75), (1218, 81.5), (1209, 88), w=w)
    f.spline([(1121, 79), (1128, 66), (1138, 56), (1144, 66), (1148, 80), (1155, 99), (1162, 92), (1168, 78),
              (1175, 64), (1181, 58), (1186, 66), (1190, 79)], stroke=RED, w=2.4)
    for x in (1163, 1167.5, 1172):
        f.line((x, 50), (x, 208), stroke=BLUE, w=0.9, dash=[1.2, 1.2])
    f.text(1123, 125, "E", size=T, italic=True, color=RED)
    f.line((1147, 116.7), (1188, 116.7), w=w)
    f.line((1147, 158), (1188, 158), w=w)
    _oa(f, 1188, 96, 179, (1273, 137.7), (1206, 119), (1208, 150))
    f.line((1273, 137.7), (1282, 137.7), w=w)
    f.rect(1282, 108, 105.5, 60.5, lw=3)
    f.fit(1310, 1358, 131.7, "Filtre", italic=True)
    f.fit(1292, 1377, 155, "passe-bas", italic=True)
    f.line((1387.5, 138), (1400, 138), w=w)
    f.text(1263, 164, "S", size=T, italic=True, color=RED)
    saw = []
    for xk in (1126.5, 1140.5, 1154.5, 1168, 1181.5):
        saw += [(xk, 208), (xk, 173), (xk + 13.5, 208)]
    f.line([(1121, 200)] + saw, stroke=BLUE, w=2.2)
    f.line((1121, 191), (1218, 191), w=w)
    f.line((1209, 184.5), (1218, 191), (1209, 197.5), w=w)
    for x0, x1 in ((1228, 1233), (1239, 1250), (1255, 1262), (1271, 1274), (1285, 1287.5)):
        f.rect(x0, 174, x1 - x0, 33, stroke=None, fill=RED)
    for x in (1263, 1269, 1275):
        f.line((x, 163), (x, 208), stroke=BLUE, w=0.9, dash=[1.2, 1.2])
    f.line((1222, 207.7), (1325, 207.7), w=w)
    f.line((1316, 201), (1325, 207.7), (1316, 214.4), w=w)
    f.fit(1115, 1215, 241, "Horloge", italic=True, color=BLUE)
    f.fit(1228, 1297, 241, "PWM", italic=True, color=RED)
    for y, x0, x1, t in ((275, 1137, 1385, "Amplificateur PWM"), (309, 1120, 1398, "(sortie en impulsions à"),
                         (343, 1155, 1365, "largeur variable)"), (374, 1128, 1388, "si V_{E}<V_{H}, alors V_{S}, sinon 0")):
        f.fit(x0, x1, y, t, italic=True)


def _seq(f, x0, x1, y, parts, cap=None, color=BLACK):
    """Runs laid out one after the other, fitted to x0..x1; a run flagged
    'o' gets an overline (logic complement)."""
    widths = [text_width(t, 10.0, "serif", False, st.get("i")) for t, st in parts]
    size = 10.0 * (x1 - x0) / sum(widths)
    if cap:
        size = min(size, cap)
    x = x0
    for (t, st), wd in zip(parts, widths):
        wd *= size / 10.0
        f.text(x, y, t, size=size, italic=bool(st.get("i")), color=color)
        if st.get("o"):
            f.line((x + size * 0.08, y - size * 0.78), (x + wd - size * 0.02, y - size * 0.78), w=1.6)
        x += wd


@figure("c076_4#0")
def portes_logiques(f):
    lw = 1.8
    f.rect(1.5, 1.5, 1368, 362, lw=lw)
    for y in (39, 147, 184):
        f.line((2, y), (1370, y), w=lw)
    f.line((118, 221), (1370, 221), w=lw)
    for x, y0 in ((117.5, 185), (162.5, 185), (226.5, 2), (478.5, 2), (733.5, 2), (1030.5, 2)):
        f.line((x, y0), (x, 363), w=lw)
    for x0, x1, t in ((25, 203, "Circuit logique"), (255, 448, "ET (AND ou &)"), (511, 699, "OU (OR ou ≥1)"),
                      (780, 981, "NON ET (Nand)"), (1065, 1334, "OU Ex (EXOR ou =1)")):
        f.fit(x0, x1, 31, t)
    f.fit(68, 160, 102, "Schéma")
    f.fit(18, 210, 176, "Calcul de Boole")
    f.text(31, 279, "Table de", size=30, rot=-90, anchor="c", va="middle")
    f.text(70, 271, "vérité", size=30, rot=-90, anchor="c", va="middle")
    T = 30
    f.text(139.5, 212, "A", size=T, anchor="c")
    f.text(182, 212, "B", size=T, anchor="c")
    cols = (352, 605.5, 881.5, 1199.5)
    for cx in cols:
        f.text(cx, 212, "Sortie", size=T, anchor="c")
    rows = ((1, 1), (1, 0), (0, 1), (0, 0))
    outs = ((1, 0, 0, 0), (1, 1, 1, 0), (0, 1, 1, 1), (0, 1, 1, 0))
    for i, (y, (a, b)) in enumerate(zip((250, 285, 320, 356), rows)):
        f.text(135, y, str(a), size=T, anchor="c")
        f.text(179, y, str(b), size=T, anchor="c")
        for cx, o in zip(cols, outs):
            f.text(cx, y, str(o[i]), size=T, anchor="c")
    w = 3
    red = dict(size=T, color=RED)
    # AND
    f.line((286, 48.5), (400, 48.5), w=w)
    f.line((286, 134), (400, 134), w=w)
    f.line((328, 48.5), (328, 134), w=w)
    f.arc(400, 91.25, 42.75, 42.75, -90, 90, w=w)
    f.line((443, 91), (457, 91), w=w)
    f.text(377, 113, "&", size=T, anchor="c")
    f.text(267, 72, "A", **red)
    f.text(267, 128, "B", **red)
    f.text(447, 84, "S", **red)
    # OR
    f.line((543, 48), (651, 48), (693.5, 90), (651, 134.5), (543, 134.5), w=w)
    f.spline([(569, 48), (593, 60), (606, 91), (593, 122), (569, 134.5)], w=w)
    f.line((693.5, 90), (713, 90), w=w)
    f.text(632, 113, "≥1", size=T, anchor="c")
    f.text(520, 72, "A", **red)
    f.text(521, 128, "B", **red)
    f.text(705, 89, "S", **red)
    # NAND
    f.line((790, 51.5), (900, 51.5), w=w)
    f.line((790, 138), (900, 138), w=w)
    f.line((832, 51.5), (832, 138), w=w)
    f.arc(900, 94.75, 43.25, 43.25, -90, 90, w=w)
    f.circle(952.5, 95.5, 9.5, lw=w)
    f.line((962, 95.5), (983, 95.5), w=w)
    f.text(873, 113, "&", size=T, anchor="c")
    f.text(768, 72, "A", **red)
    f.text(769, 132, "B", **red)
    f.text(988, 104, "S", **red)
    # XOR
    f.line((1093, 51.5), (1222, 51.5), (1265, 95), (1222, 138), (1093, 138), w=w)
    f.spline([(1093, 51.5), (1137, 62), (1157, 95), (1137, 128), (1093, 138)], w=w)
    f.spline([(1123, 51.5), (1164, 62), (1180, 95), (1164, 128), (1123, 138)], w=w)
    f.line((1265, 95), (1305, 95), w=w)
    f.text(1215, 113, "=1", size=T, anchor="c")
    f.text(1066, 72, "A", **red)
    f.text(1067, 132, "B", **red)
    f.text(1313, 104, "S", **red)
    # Boolean expressions
    f.fit(303, 398, 176, "S = A.B")
    f.fit(546, 663, 176, "S = A + B")
    I = {"i": 1}
    _seq(f, 770, 992, 176, [("S = ", {}), ("A.B", {"o": 1}), (" (= ", I), ("A", {"i": 1, "o": 1}), (" + ", I),
                            ("B", {"i": 1, "o": 1}), (")", I)])
    _seq(f, 1045, 1355, 176, [("S = A ⊕ B ", {}), ("(= ", I), ("A", {"i": 1, "o": 1}), (".B + A.", I),
                              ("B", {"i": 1, "o": 1}), (")", I)])


@figure("c078_2#0")
def lambda_f(f):
    nb = dict(bold=True, color=NAVY)
    f.fit(23, 108, 42.5, "λ(m) =", **nb)
    f.line((113, 45.5), (218, 45.5), stroke=NAVY, w=2)
    f.fit(135, 182, 40, "300", **nb)
    f.fit(113, 205, 70, "f(MHz)", **nb)
    f.fit(289, 320, 40, "ou", **nb)
    f.fit(425, 542, 42.5, "f(MHz) =", **nb)
    f.line((552, 45.5), (657, 45.5), stroke=NAVY, w=2)
    f.fit(572, 620, 40, "300", **nb)
    f.fit(567, 627, 70, "λ(m)", **nb)


@figure("c078_3#0")
def triangle_lambda(f):
    f.poly([(27, 235.5), (163, 14), (299, 235.5)], stroke=BLUE, w=2)
    f.fit(140, 185, 106, "300")
    f.fit(66, 164, 211, "f (MHz)")
    f.fit(194, 259, 211, "λ (m)")


def _nand_rs(f, x_bar, y_top, y_bot, x_arc, bub, x_out, w=2.4):
    r = (y_bot - y_top) / 2
    f.line((x_bar, y_top), (x_bar, y_bot), w=w)
    f.arc(x_arc, y_top + r, r, r, -90, 90, w=w)
    f.circle(bub[0], bub[1], bub[2], lw=w)
    f.line((bub[0] + bub[2], bub[1]), (x_out, bub[1]), w=w)


def _nor_rs(f, back_x, y_top, y_bot, x_front, bub, x_out, w=2.4):
    ym = (y_top + y_bot) / 2
    f.spline([(back_x, y_top), (back_x + 28, y_top + 10), (back_x + 40, ym), (back_x + 28, y_bot - 10),
              (back_x, y_bot)], w=w)
    f.line((x_front, y_top), (bub[0] - bub[2], bub[1]), (x_front, y_bot), w=w)
    f.circle(bub[0], bub[1], bub[2], lw=w)
    f.line((bub[0] + bub[2], bub[1]), (x_out, bub[1]), w=w)


@figure("c077_2#0")
def bascules(f):
    w = 2.4
    T = 28
    it = dict(italic=True)
    red = dict(italic=True, color=RED)
    # ---- NAND latch
    gnd(f, 7, 8, 18, 44)
    gnd(f, 7, 214, 18, 249)
    f.line((18, 26.5), (55, 26.5), (92, 36), w=w)
    f.line((18, 232.5), (55, 232.5), (92, 221.5), w=w)
    f.line((97, 27), (310, 27), w=w)
    f.line((97, 232.5), (310, 232.5), w=w)
    f.line((118, 27), (118, 44.5), w=w)
    f.rect(96.5, 44.5, 43, 55, lw=w)
    f.line((118, 99.5), (118, 157), w=w)
    f.rect(96.5, 157, 43, 54.5, lw=w)
    f.line((118, 211.5), (118, 232.5), w=w)
    f.line((93, 123.5), (118, 123.5), w=w)
    f.text(77, 130, "+", size=24, anchor="c")
    f.fit(103, 118, 72, "R", **it)
    f.fit(103, 118, 182, "R", **it)
    f.fit(5, 36, 66, "E1", **red)
    f.fit(21, 54, 215, "E2", **red)
    f.line((181, 101.5), (312, 101.5), w=w)
    f.line((181, 157), (312, 157), w=w)
    _nand_rs(f, 202, 27, 101.5, 312, (361, 64, 11), 476)
    _nand_rs(f, 202, 157, 232.5, 312, (361, 194, 11), 476)
    f.line((413, 64), (413, 101), (182, 157), w=w)
    f.line((413, 194), (413, 155), (182, 102), w=w)
    f.fit(227, 302, 72, "NAND", **it)
    f.fit(227, 302, 202, "NAND", **it)
    f.fit(480, 506, 72, "S1", **red)
    f.fit(480, 509, 202, "S2", **red)
    f.fit(147, 163, 113, "A", **it)
    f.fit(150, 165, 160, "B", **it)
    f.fit(432, 570, 105, "Bascule R/S", **it)
    f.fit(432, 508, 135, "NAND", **it)
    f.fit(432, 548, 162, "entrée à 0", **it)
    # ---- NOR latch
    f.text(592, 38, "+", size=24, anchor="c")
    f.text(592, 243, "+", size=24, anchor="c")
    f.line((603, 31), (645, 31), (682.5, 40), w=w)
    f.line((603, 236.5), (645, 236.5), (682.5, 226), w=w)
    f.line((687, 31), (920, 31), w=w)
    f.line((687, 236.5), (918, 236.5), w=w)
    f.line((729, 31), (729, 48.5), w=w)
    f.rect(708, 48.5, 42, 55.5, lw=w)
    f.line((730, 104), (730, 143.5), w=w)
    f.rect(708, 143.5, 42, 54.5, lw=w)
    f.line((731, 198), (731, 236.5), w=w)
    gnd(f, 682, 106, 692, 141)
    f.line((692, 124), (730, 124), w=w)
    f.fit(712, 730, 77, "R", **it)
    f.fit(712, 730, 172, "R", **it)
    f.fit(584, 613, 66, "E1", **red)
    f.fit(606, 638, 219, "E2", **red)
    f.line((793, 105.5), (919, 105.5), w=w)
    f.line((793, 161.5), (920, 161.5), w=w)
    _nor_rs(f, 797.5, 31, 105.5, 920, (971, 67.5, 10), 1087)
    _nor_rs(f, 797.5, 161.5, 236.5, 919, (971, 198.5, 10), 1087)
    f.line((1003.5, 68), (1003.5, 106), (793, 161), w=w)
    f.line((1003.5, 198.5), (1003.5, 159), (793, 105.5), w=w)
    f.fit(857, 917, 75, "NOR", **it)
    f.fit(858, 916, 207, "NOR", **it)
    f.fit(1091, 1118, 75, "S1", **red)
    f.fit(1091, 1120, 206, "S2", **red)
    f.fit(760, 775, 117, "A", **it)
    f.fit(761, 776, 170, "B", **it)
    f.fit(1018, 1160, 107, "Bascule R/S", **it)
    f.fit(1017, 1075, 137, "NOR", **it)
    f.fit(1019, 1133, 165, "entrée à 1", **it)
    # ---- MOS-FET memory cell
    f.rect(1213, 26.5, 192, 73.5, stroke=None, fill="#d9d9d9")
    f.rect(1213, 51.5, 68, 48.5, stroke=None, fill="#ffffff")
    f.rect(1337.5, 51.5, 67.5, 48.5, stroke=None, fill="#ffffff")
    f.rect(1281, 94, 56.5, 6, stroke=None, fill="#ffffff")
    f.rect(1213, 26.5, 192, 73.5, lw=2)
    f.line((1213, 51.5), (1281, 51.5), (1281, 100), w=2)
    f.line((1405, 51.5), (1337.5, 51.5), (1337.5, 100), w=2)
    f.fit(1252, 1275, 71.7, "N", **it)
    f.text(1309, 71.7, "P", size=28, italic=True)
    f.fit(1372, 1393, 71.7, "N", **it)
    f.line((1298, 87.3), (1307, 87.3), w=1.6)
    f.line((1319, 87.3), (1328, 87.3), w=1.6)
    blue = "#1a68b8"
    f.spline([(1242, 76), (1262, 87), (1300, 96), (1340, 94), (1370, 85), (1388, 80)], stroke=blue, w=4.5)
    f.poly([(1380, 73), (1401, 81.5), (1384, 88)], stroke=None, fill=blue)
    gnd(f, 1281, 109, 1334, 118)
    f.line((1312, 118), (1312, 155), w=2)
    for cx in (1299, 1327.5):
        f.line((cx - 8.5, 133), (cx + 8.5, 133), w=2)
        f.line((cx, 126), (cx, 140), w=2)
    f.line((1193, 71.5), (1213, 71.5), w=2)
    f.line((1202, 62.5), (1213, 62.5), w=2)
    f.line((1207.5, 57), (1207.5, 68), w=2)
    f.line((1404, 71.5), (1424, 71.5), w=2)
    f.line((1413, 65.5), (1427, 65.5), w=2)
    f.fit(1272, 1352, 180, "Bit = 1", **it)
    f.fit(1185, 1445, 224, "Mémoire à MOS-FET", **it)


PURPLE2 = "#7030a0"
DBLUE = "#0070c0"


@figure("c077_3#0")
def echantillonnage(f):
    grey = dict(stroke="#808080", w=1.4, dash=[5, 3])
    for y in (20, 135.5):
        f.line((0, y), (575, y), **grey)
    for y in (29.5, 38.5, 46, 52.5, 62, 70, 80.5, 92, 101.5, 113, 125):
        f.line((60, y), (575, y), **grey)
    bd = dict(stroke=DBLUE, w=1.8, dash=[6, 4])
    for x in (104, 146, 188, 231, 272.5, 315, 441, 484, 526):
        f.line((x, 28), (x, 283), **bd)
    for x in (357.5, 400):
        f.line((x, 28), (x, 330), **bd)
    f.line((567.5, 28), (567.5, 370), **bd)
    f.line((62.5, 285), (62.5, 370), **bd)
    f.spline([(63, 93), (84, 75), (102, 60), (126, 43), (150, 33), (162, 32), (180, 38), (216, 54), (246, 75),
              (276, 94), (318, 115), (351, 119), (384, 109), (408, 97), (440, 76), (465, 60), (490, 44),
              (515, 33), (540, 30), (560, 37), (580, 50)], stroke=RED, w=1.6, dash=[1.6, 2.2])
    f.curve(lambda x: 201.5 - 36 * math.cos(2 * math.pi * (x - 88) / 53.2), 70, 578, n=400,
            stroke=PURPLE2, w=1.6, dash=[1.6, 2.2])
    for x0, x1, y in ((65, 104, 92.5), (105, 147, 52.5), (147, 187, 37.5), (189, 229, 52.5), (231, 271, 70),
                      (272, 313, 92.5), (315, 354, 114), (357, 397, 124), (400, 439, 102.5), (442, 482, 80),
                      (484, 522, 46), (526, 567, 29)):
        f.line((x0, y), (x1, y), stroke=RED, w=2.6)
    for x0, x1, y in ((65, 102, 214), (105, 145, 231), (147, 187, 206), (189, 228, 165), (231, 270, 201),
                      (272, 312, 237.5), (315, 354, 231), (357, 397, 166), (400, 441, 166), (442, 483, 207.5),
                      (484, 524, 237.5), (526, 567, 201)):
        f.line((x0, y), (x1, y), stroke=PURPLE2, w=2.2)
    f.line((63.5, 284), (63.5, 15), w=2.4)
    f.line((56, 28), (63.5, 14), (71, 28), w=2.4)
    f.line((63, 284), (600, 284), w=2.4)
    f.line((586, 277), (600, 284), (586, 291), w=2.4)
    f.text(603, 308, "T", size=26)
    f.line((135, 290), (135, 66), stroke=RED, w=2.6)
    f.poly([(126, 68), (135, 50), (144, 68)], stroke=None, fill=RED)
    f.line((120, 290), (120, 248), stroke=PURPLE2, w=2.4)
    f.poly([(113, 250), (120, 232), (127, 250)], stroke=None, fill=PURPLE2)
    f.poly([(357, 323), (365, 317), (365, 320.5), (391, 320.5), (391, 317), (399, 323), (391, 329), (391, 325.5),
            (365, 325.5), (365, 329)], stroke=DBLUE, w=1.4)
    for x0, x1 in ((95, 65), (525, 565)):
        f.line((x0, 371), (x1 + (8 if x1 < x0 else -8), 371), stroke=DBLUE, w=2.2)
        d = 1 if x1 > x0 else -1
        f.poly([(x1, 371), (x1 - d * 14, 364.5), (x1 - d * 14, 377.5)], stroke=None, fill=DBLUE)
    f.text(9, 45, "U_{max}", size=27)
    f.text(9, 152, "U_{min}", size=27)
    for cx, cy, span, t, col in ((22, 92, 75, "signal", RED), (52, 80, 100, "converti", RED),
                                 (50, 207, 45, "alias", PURPLE2), (593, 36, 52, "p(V) =", BLACK),
                                 (617, 140, 260, "pas de résolution du CAN", BLACK),
                                 (650, 157, 295, "quantification = (U_{max} – U_{min} / p", BLACK)):
        size = min(28, 10.0 * span / text_width(t, 10.0))
        f.text(cx, cy, t, size=size, color=col, rot=-90, anchor="c", va="middle")
    f.text(593, 130, "p", size=27, rot=-90, anchor="c", va="middle")
    f.fit(98, 321, 314, "Tension échantillonnée")
    f.fit(109, 319, 337, "convertie par le CAN")
    f.text(377, 314, "e", size=27)
    f.fit(402, 562, 314, "e(s) = 1/f_{ech}(Hz)")
    f.fit(402, 542, 337, "f_{nyquist} = f_{ech} / 2")
    f.fit(102, 537, 372, "échantillonnage pour convolution avec DFT")


def _arrow_tip(f, x0, y0, x1, y1, color, size=16, w=2.4, filled=False):
    a = math.atan2(y1 - y0, x1 - x0)
    p1 = (x1 + size * math.cos(a + 2.65), y1 + size * math.sin(a + 2.65))
    p2 = (x1 + size * math.cos(a - 2.65), y1 + size * math.sin(a - 2.65))
    if filled:
        f.poly([p1, (x1, y1), p2], stroke=None, fill=color)
    else:
        f.line(p1, (x1, y1), p2, stroke=color, w=w)


@figure("c078_1#0")
def propagation(f):
    xs = (36, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1236)
    top = (80, 56, 34, 19, 12, 8, 10, 12, 17, 26, 38, 52, 73, 82)
    bot = (200, 182, 165, 154, 148, 145, 146, 149, 154, 161, 171, 184, 203, 210)
    f.spline(list(zip(xs, top)) + list(zip(reversed(xs), reversed(bot))), stroke=None, fill="#ececec", closed=True)
    n = 44
    for k in range(n + 1):
        t = k / n
        f.spline([(x, a + (b - a) * t) for x, a, b in zip(xs, top, bot)], stroke="#c4c4c4", w=0.7, n=6)
    # ground
    f.poly([(30, 458), (168, 414), (258, 350), (325, 349), (380, 386), (386, 390), (490, 391), (495, 397),
            (730, 411), (745, 413), (760, 406), (868, 370), (1058, 391), (1065, 402), (1235, 445), (1235, 500),
            (30, 500)], stroke="#14301c", fill="#24543a", w=1.4)
    for (cx, cy, rx, ry) in ((120, 470, 60, 14), (330, 430, 70, 16), (600, 450, 90, 18), (900, 420, 80, 15),
                            (1120, 470, 70, 12)):
        f.ellipse(cx, cy, rx, ry, stroke=None, fill="#2f6646")
    # antennas
    for x, y0, y1 in ((276.5, 302, 352), (765, 368, 408), (1205, 390, 450)):
        f.line((x, y0), (x, y1), stroke="#808080", w=4)
    # rays
    bdot = dict(stroke=BLUE, w=2.2, dash=[1.6, 2.6], cap="b")
    f.line((278, 300), (658, 89), **bdot)
    _arrow_tip(f, 278, 300, 660, 88, BLUE, w=2.2)
    f.line((660, 88), (779, 63.5), **bdot)
    _arrow_tip(f, 660, 88, 781, 63, BLUE, w=2.2)
    f.line((781, 63), (885, 85), **bdot)
    _arrow_tip(f, 781, 63, 887, 85, BLUE, w=2.2)
    f.line((781, 63), (903, 30), stroke=BLUE, w=1, dash=[1.2, 1.8], cap="b")
    _arrow_tip(f, 781, 63, 905, 30, BLUE, size=12, w=1.2)
    f.line((887, 85), (1203, 383), stroke=BLUE, w=1, dash=[1.2, 1.8], cap="b")
    _arrow_tip(f, 887, 85, 1205, 385, BLUE, size=13, w=1.2)
    f.line((280, 302), (762, 368), stroke="#008000", w=2.2, dash=[1.6, 2.6], cap="b")
    _arrow_tip(f, 280, 302, 765, 368, "#008000", w=2.2)
    f.line((768, 368), (850, 346), (950, 346), (1060, 365), (1160, 410), (1198, 394), stroke=RED, w=2.2,
           dash=[1.6, 2.6], cap="b")
    _arrow_tip(f, 1160, 410, 1202, 392, RED, w=2.2)
    # pointers
    for x0, y0, x1, y1, col in ((530, 272, 461, 307, "#008000"), (745, 245, 850, 337, RED),
                                (990, 268, 1030, 236, BLUE), (1020, 12, 937, 12, BLUE)):
        f.line((x0, y0), (x1, y1), stroke=col, w=2.4)
        _arrow_tip(f, x0, y0, x1, y1, col, w=2.4)
    for x0, y0, x1, y1 in ((455, 455, 287, 362), (620, 460, 750, 420), (620, 460, 1175, 440)):
        f.line((x0, y0), (x1, y1), stroke="#ffffff", w=2.4)
        _arrow_tip(f, x0, y0, x1, y1, "#ffffff", w=2.4)
    # labels
    f.text(20, 150, "Ionosphère", size=28, rot=-90, anchor="c", va="middle")
    f.fit(448, 650, 33, "Couches E et F")
    f.fit(399, 669, 72, "(réfraction et réflexion)", italic=True)
    f.rich(107, 147, [("Couche D ", {}), ("(absorption)", I_)], size=27)
    f.fit(1026, 1270, 22, "Ondes non réfléchies", italic=True)
    f.fit(1252, 1360, 58, "Altitude :")
    f.fit(1252, 1411, 93, "250 à 650 km")
    f.fit(1255, 1345, 126, "130 km")
    f.fit(1253, 1325, 161, "90 km")
    f.fit(1253, 1325, 227, "50 km")
    for y, t in ((112, "F"), (148, "E"), (193, "D")):
        f.text(1208, y, t, size=27, anchor="c")
    f.fit(474, 644, 250, "Ondes directes")
    f.fit(708, 780, 189, "Ondes")
    f.fit(708, 775, 224, "de sol")
    f.fit(895, 967, 258, "Ondes")
    f.fit(894, 1006, 293, "réfléchies")
    f.fit(224, 293, 439, "Terre", bold=True, color="#ffffff")
    f.fit(477, 584, 466, "Antennes", color="#ffffff")


@figure("c079_1#0")
def ionosphere(f):
    it = dict(italic=True)
    f.line((58, 433), (58, 153), w=2.4)
    f.line((58, 153), (58, 84), w=2.4, dash=[5, 4], cap="b")
    f.line((58, 84), (58, 36), w=2.4)
    f.line((51, 48), (58, 35), (65, 48), w=2.4)
    dots = dict(w=1.6, dash=[1.6, 1.6], cap="b")
    for y, x1 in ((82, 745), (161, 737), (240, 743), (292, 614), (345, 745), (397, 745)):
        f.line((58, y), (x1, y), **dots)
    for k in range(58):
        f.circle(62 + k * 12.1, 430, 3.2, stroke=None, fill=BLACK)
    for x0, x1, y, t in ((13, 55, 92, "650"), (11, 55, 165, "200"), (13, 55, 244, "130"), (27, 55, 297, "90"),
                         (30, 55, 349, "50"), (26, 55, 401, "15")):
        f.fit(x0, x1, y, t, **it)
    f.text(37, 437, "0", size=28, italic=True)
    f.fit(6, 159, 26, "Altitude (km)", **it)
    f.fit(98, 279, 60, "Magnétosphère", **it)
    f.fit(329, 738, 32, "Densité en électrons libres par cm^{3}", **it)
    f.fit(327, 425, 69, "Couches", **it)
    for x, e in zip((487, 540, 594, 647, 700), "23456"):
        f.text(x, 69, "10^{%s}" % e, size=28, italic=True)
    for x, y, t in ((384, 113, "F2"), (322, 147, "F"), (384, 216, "F1"), (322, 286, "E"), (322, 318, "D"),
                    (322, 365, "C"), (322, 393, "B"), (322, 424, "A")):
        f.text(x, y, t, size=28, italic=True)
    for x, y0, y1, word in ((122, 405, 97, "Atmosphère"), (231, 324, 97, "Ionosphère")):
        step = (y1 - y0) / (len(word) - 1)
        for k, ch in enumerate(word):
            f.text(x, y0 + k * step, ch, size=28, italic=True, rot=-90, anchor="c", va="middle")
    f.fit(158, 297, 365, "Mésosphère", **it)
    f.fit(158, 305, 393, "Stratosphère", **it)
    f.fit(160, 305, 424, "Troposphère", **it)
    f.fit(447, 708, 365, "sans incidence notoire", **it)
    f.fit(447, 665, 393, "sur la propagation", **it)
    f.fit(447, 748, 424, "incidence météorologique", **it)
    f.fit(447, 624, 452, "sur les rebonds", **it)
    f.fit(681, 735, 277, "Jour", **it)
    f.fit(681, 732, 312, "Nuit", **it)
    jour = [(868, 142), (1000, 155), (1200, 163), (1350, 172), (1420, 175), (1445, 192), (1447, 222), (1437, 240),
            (1395, 243), (1360, 250), (1345, 270), (1340, 330), (1330, 395), (1305, 405), (1250, 410), (1232, 430),
            (1225, 480), (1218, 540), (1198, 570), (1100, 585), (1080, 610), (1068, 640), (1040, 652), (900, 655),
            (845, 685)]
    f.spline([(x / 2, y / 2) for x, y in jour], stroke=BLUE, w=2.4)
    nuit = [(868, 155), (950, 165), (1050, 180), (1150, 215), (1200, 235), (1205, 268), (1190, 290), (1140, 295),
            (1125, 315), (1120, 350), (1125, 420), (1128, 480), (1123, 520), (1105, 545), (1000, 556), (900, 575),
            (870, 590), (850, 610), (830, 635)]
    f.spline([(x / 2, y / 2) for x, y in nuit], stroke=RED, w=2.4, dash=[5, 4], cap="b")
    for x0, y0, x1, y1, col in ((680, 250, 652, 218, BLUE), (678, 298, 575, 215, RED)):
        f.line((x0, y0), (x1, y1), stroke=col, w=2.2)
        _arrow_tip(f, x0, y0, x1, y1, col, size=15, w=2.2)


def _hdarrow(f, x0, x1, y, left=True, right=True, color=BLUE, w=2.4, s=11):
    f.line((x0 + (s - 2 if left else 0), y), (x1 - (s - 2 if right else 0), y), stroke=color, w=w)
    if left:
        f.poly([(x0, y), (x0 + s, y - 5.5), (x0 + s, y + 5.5)], stroke=None, fill=color)
    if right:
        f.poly([(x1, y), (x1 - s, y - 5.5), (x1 - s, y + 5.5)], stroke=None, fill=color)


@figure("c079_2#0")
def spectre(f):
    it = dict(italic=True)
    f.rect(1.5, 1.5, 1390, 266, lw=2)
    f.line((2, 75), (1392, 75), w=2)
    f.line((2, 193), (1392, 193), w=2)
    f.line((180.5, 2), (180.5, 268), w=2)
    f.line((696, 76), (696, 193), w=1.4, dash=[6, 3, 1.5, 3], cap="b")
    f.line((966, 143), (966, 193), w=1.4, dash=[6, 3, 1.5, 3], cap="b")
    T = 30
    f.text(90, 32, "λ (m)", size=T, anchor="c", **it)
    f.fit(27, 152, 67, "Fréq. (Hz)", **it)
    f.text(90, 126, "Gammes", size=T, anchor="c", **it)
    f.text(90, 161, "d’ondes", size=T, anchor="c", **it)
    f.fit(15, 167, 221, "Propagation", **it)
    f.fit(30, 150, 258, "par ondes", **it)
    units = ((215, 272, "mam"), (290, 324, "km"), (352, 385, "hm"), (409, 459, "dam"), (487, 507, "m"),
             (544, 580, "dm"), (607, 642, "cm"), (667, 710, "mm"), (730, 775, "10^{-4}"), (797, 840, "10^{-5}"),
             (862, 897, "µm"), (922, 962, "10^{-7}"), (985, 1030, "10^{-8}"), (1052, 1090, "nm"),
             (1107, 1162, "10^{-10}"), (1172, 1225, "10^{-11}"), (1242, 1280, "pm"), (1297, 1352, "10^{-13}"))
    for x0, x1, t in units:
        f.text((x0 + x1) / 2, 31, t, size=T, anchor="c", **it)
    freqs = ((205, 242), (267, 305), (331, 370), (395, 432), (457, 497), (522, 560), (582, 629), (645, 692),
             (709, 755), (772, 819), (835, 882), (900, 947), (962, 1010), (1026, 1074), (1090, 1137), (1154, 1202),
             (1217, 1265), (1281, 1329))
    for k, (x0, x1) in enumerate(freqs):
        f.text((x0 + x1) / 2, 67, "10^{%d}" % (k + 4), size=T, anchor="c", **it)
    for x0, x1, t in ((192, 235, "VLF"), (260, 290, "LF"), (320, 360, "MF"), (385, 422, "HF"), (442, 492, "VHF"),
                      (505, 555, "UHF"), (570, 620, "SHF"), (632, 682, "EHF")):
        f.text((x0 + x1) / 2, 120, t, size=28, anchor="c", **it)
    f.fit(247, 652, 152, "radiofréquences gérées par l’UIT", **it)
    f.fit(332, 567, 185, "(de 9 kHz à 275 GHz)", **it)
    _hdarrow(f, 706, 885, 92.5)
    _hdarrow(f, 941, 993, 92.5)
    _hdarrow(f, 997, 1181, 92.5)
    _hdarrow(f, 1184, 1369, 92.5, right=False)
    _hdarrow(f, 1266, 1370, 129.5, right=False)
    for x0, x1, y, t in ((729, 842, 120, "Infrarouges"), (877, 947, 120, "spectre"), (962, 995, 120, "UV"),
                         (1035, 1127, 120, "Rayons X"), (1187, 1277, 120, "Rayons γ"), (882, 945, 153, "visible"),
                         (1200, 1380, 153, "Rayons cosmiques"), (740, 956, 185, "fréquences optiques"),
                         (1037, 1295, 185, "rayonnements ionisants"), (222, 292, 240, "de sol"),
                         (349, 464, 240, "réfléchies"), (507, 600, 240, "directes"), (775, 922, 240, "photoniques")):
        f.fit(x0, x1, y, t, max_size=31, **it)
    _hdarrow(f, 327, 483, 209.5)
    _hdarrow(f, 215, 347, 246.5, left=False)
    _hdarrow(f, 460, 750, 246.5)
    _hdarrow(f, 697, 965, 219.5)


@figure("c080_1#0")
def champ_magnetique(f):
    f.poly([(63, 124.5), (351, 124.5), (300, 255.5), (11, 255.5)], stroke=RED, w=2)
    for rx, ry, cy in ((105, 64, 189), (77, 40, 190), (27.5, 12.5, 190)):
        f.ellipse(167.5, cy, rx, ry, stroke=RED, lw=2, dash=[6, 4])
    f.line((167.5, 47), (167.5, 178), w=4)
    f.line((167.5, 184), (167.5, 255), w=4, dash=[5, 4], cap="b")
    f.line((167.5, 258), (167.5, 308), w=4)
    f.poly([(161, 86), (167.5, 75), (174, 86)], stroke=None, fill="#008000")
    f.fit(182, 193, 89, "I", color="#008000")
    dg = "#404040"
    f.spline([(167, 124.5), (120, 130), (82, 145), (64, 168)], stroke=dg, w=2.4)
    f.line((58, 152), (62, 170), (75, 158), stroke=dg, w=2.4)
    f.spline([(167, 229), (205, 225), (232, 210), (245, 187)], stroke=dg, w=2.4)
    f.line((236, 197), (245, 186), (249, 201), stroke=dg, w=2.4)
    for x0, y0, x1, y1 in ((90, 100, 88.5, 176), (95, 100, 140, 175)):
        f.line((x0, y0), (x1, y1), w=2.2)
        _arrow_tip(f, x0, y0, x1, y1, BLACK, size=14, filled=True)
    for y, t in ((26, "Lignes de"), (59, "champ"), (91, "magnétique")):
        f.text(146, y, t, size=29, anchor="r")
    f.text(294, 188, "H", size=30, color=RED)
    f.fit(204, 350, 283, "Plan perpen-")
    f.fit(216, 350, 317, "diculaire au")
    f.fit(223, 351, 351, "conducteur")


@figure("c081_1#0")
def yagi(f):
    f.rect(164, 23, 5, 167, stroke=None, fill=RED)
    f.rect(248, 44, 5, 126, stroke=None, fill=RED)
    f.rect(332, 67, 4.5, 82, stroke=None, fill=RED)
    f.line((168, 109), (334, 109), w=2.2)
    for x0, y0, x1, y1 in ((127, 133, 164, 92), (283, 29, 261, 76), (387, 160, 338, 134)):
        f.line((x0, y0), (x1, y1), stroke=BLUE, w=2.2)
        _arrow_tip(f, x0, y0, x1, y1, BLUE, size=13, w=2.2)
    f.line((128, 212), (375, 212), stroke=BLUE, w=2.2)
    _arrow_tip(f, 128, 212, 377, 212, BLUE, size=13, w=2.2)
    f.fit(297, 515, 33, "Élément rayonnant")
    f.fit(419, 514, 68, "= dipôle")
    f.fit(4, 124, 138, "Réflecteur")
    f.fit(391, 500, 165, "Directeur")
    f.fit(18, 443, 251, "Direction du rayonnement maximum")


@figure("c081_2#0")
def dipole(f):
    f.fit(165, 512, 32, "L(m) = 150 / f(MHz) = λ / 2", bold=True, color=NAVY)
    _hdarrow(f, 8, 632, 44.5, s=14)
    f.curve(lambda x: 90 + 72 * math.cos(math.pi * (x - 320) / 624), 8, 632, n=200, stroke=RED, w=2)
    f.curve(lambda x: 185 - 94 * math.cos(math.pi * (x - 320) / 624), 8, 632, n=200, stroke="#00a050", w=2.2,
            dash=[7, 6], cap="b")
    f.line((6, 186.5), (313, 186.5), (313, 229), w=3)
    f.line((633, 186.5), (325.5, 186.5), (325.5, 230), w=3)
    f.text(20, 90, "U_{eff}", size=29, color=RED)
    f.text(305, 76, "I_{eff}", size=29, color="#008000")
    f.fit(255, 370, 266, "Z = 73 Ω", bold=True)


@figure("c081_3#0")
def doublet(f):
    nv = dict(color=NAVY)
    f.fit(14, 535, 36, "Longueur théorique du doublet demi-onde :")
    f.fit(567, 770, 36, "L(m) = λ(m)/2 =", **nv)
    f.fit(865, 905, 35, "300", **nv)
    f.line((827, 39.5), (932, 39.5), stroke=NAVY, w=2)
    f.fit(822, 937, 70, "2.f(MHz)", **nv)
    f.text(957, 35, "=", size=28, **nv)
    f.fit(1037, 1080, 35, "150", bold=True, **nv)
    f.line((1012, 39.5), (1105, 39.5), stroke=NAVY, w=2)
    f.fit(1012, 1100, 70, "f(MHz)", bold=True, **nv)


@figure("c081_4#0")
def quart_onde(f):
    f.line((202.5, 11), (202.5, 226.5), (175, 226.5), w=4)
    f.line((175, 253), (203, 253), (203, 270), w=2.4)
    f.line((203, 270), (203, 436), w=2.2, dash=[6, 4], cap="b")
    _arrow_tip(f, 312, 388, 205, 442, BLACK, size=16, filled=True)
    f.line((312, 388), (215, 437), w=1.8)
    f.line((158.5, 26), (158.5, 219), stroke=BLUE, w=2)
    f.poly([(158.5, 16), (153, 28), (164, 28)], stroke=None, fill=BLUE)
    f.poly([(158.5, 229), (153, 217), (164, 217)], stroke=None, fill=BLUE)
    nb = dict(bold=True, color=NAVY)
    for cx, cy, span, t in ((99, 105, 200, "L(m) = λ / 4 ="), (133, 110, 150, "75 / f (MHz)")):
        size = 10.0 * span / text_width(t, 10.0, bold=True)
        f.text(cx, cy, t, size=size, rot=-90, anchor="c", va="middle", **nb)
    f.spline([(229, 220), (235, 180), (245, 145), (265, 107), (287, 77), (310, 47), (332, 17)], stroke=RED, w=2)
    f.spline([(212, 19), (240, 37), (270, 57), (287, 75), (300, 105), (310, 135), (322, 175), (332, 217)],
             stroke="#00a050", w=2.2, dash=[6, 5], cap="b")
    f.text(342, 37, "U_{eff}", size=27, color=RED)
    f.text(342, 229, "I_{eff}", size=27, color="#008000")
    f.fit(40, 155, 259, "Z = 36 Ω", bold=True)
    f.rect(11.5, 270, 396.5, 31, stroke=None, fill="#c0c0c0")
    f.line((203, 270), (203, 301), w=2.2, dash=[6, 4], cap="b")
    f.fit(62, 388, 291, "Plan de sol, terre ou masse")
    f.fit(230, 425, 347, "Brin reconstitué")
    f.fit(217, 425, 381, "par le plan de sol")


BROWN = "#993300"


@figure("c082_1#0")
def diagramme_rayonnement(f):
    outline = [(653, 169), (647, 152), (635, 138), (605, 119), (540, 91), (496, 80), (453, 74), (421, 74), (352, 88),
               (218, 137), (206, 139), (177, 152), (149, 159), (133, 159), (132, 138), (116, 124), (101, 118),
               (93, 118), (78, 128), (63, 156), (61, 172), (30, 168), (20, 174), (12, 197), (11, 222), (16, 238),
               (27, 254), (50, 255), (76, 241), (88, 240), (90, 256), (94, 263), (111, 275), (133, 284), (142, 282),
               (149, 273), (151, 248), (144, 240), (144, 227), (154, 226), (179, 237), (349, 290), (418, 304),
               (453, 305), (510, 296), (593, 267), (616, 254), (645, 224), (653, 190)]
    f.spline(outline, closed=True, stroke=BLACK, fill="#c0c0c0", w=2, n=6)
    f.line((120, 200), (612, 72), stroke=BLUE, w=1.2)
    f.line((120, 200), (612, 320), stroke=BLUE, w=1.2)
    f.rect(112, 158, 8, 82, stroke=None, fill=RED)
    f.spline([(503, 12), (512, 40), (521, 70), (530, 115), (535, 145), (537, 180), (536, 215), (530, 245),
              (518, 268), (508, 295), (497, 325), (489, 345)], stroke=BLUE, w=2.4, dash=[7, 5], cap="b")
    f.arc(120, 200, 112, 112, -13, 13, w=1.4)
    _hdarrow(f, 536, 652, 179, s=13, w=2.6)
    _hdarrow(f, 15, 115, 404.5, s=13, w=2.6)
    _hdarrow(f, 119, 652, 404.5, s=13, w=2.6)
    for x0, y0, x1, y1 in ((611, 26, 512, 26), (271, 26, 101, 134), (271, 26, 147, 252), (64, 82, 104, 188),
                           (716, 214, 565, 237), (63, 289, 36, 225)):
        f.line((x0, y0), (x1, y1), stroke=BROWN, w=1.8)
        _arrow_tip(f, x0, y0, x1, y1, BROWN, size=15, w=1.8)
    for x0, x1, y, t in ((37, 197, 28, "Antenne (brin"), (37, 161, 61, "rayonnant)"), (300, 470, 28, "Lobes latéraux"),
                         (647, 926, 28, "Atténuation de 3 dB par"), (683, 926, 62, "rapport à la direction"),
                         (734, 925, 95, "la plus favorable"), (582, 635, 166, "3 dB"),
                         (222, 538, 209, "Angle d'ouverture à –3 dB"), (744, 872, 214, "Lobe avant"),
                         (36, 177, 317, "Lobe arrière"), (6, 119, 361, "Puissance"), (26, 100, 393, "arrière"),
                         (163, 675, 382, "Puissance dans la direction la plus favorable")):
        f.fit(x0, x1, y, t, max_size=31)


@figure("c083_1#0")
def smith_fouet(f):
    f.line((8.5, 26), (8.5, 358), w=2.4)
    f.poly([(1, 28), (8.5, 10), (16, 28)], stroke=None, fill=BLACK)
    f.poly([(1, 357), (8.5, 375), (16, 357)], stroke=None, fill=BLACK)
    f.line((9, 192.5), (361, 192.5), w=2.4)
    f.poly([(360, 184.5), (377, 192.5), (360, 200.5)], stroke=None, fill=BLACK)
    f.line((10, 62), (357, 62), w=1.2, dash=[1.4, 1.4], cap="b")
    f.line((10, 323), (357, 323), w=1.2, dash=[1.4, 1.4], cap="b")
    pts = [(27, 363), (33, 320), (42, 260), (48, 215), (52, 193), (58, 160), (66, 138), (75, 124), (100, 100),
           (140, 78), (175, 65), (200, 62), (230, 67), (260, 80), (285, 98), (305, 125), (318, 155), (322, 193),
           (319, 230), (310, 262), (295, 285), (270, 305), (240, 318), (205, 324), (175, 320), (140, 305),
           (110, 282), (93, 255), (90, 225), (97, 195), (108, 165), (125, 140), (150, 122), (175, 115), (195, 114),
           (220, 120), (245, 133), (262, 150), (273, 170), (277, 193), (277, 226)]
    f.spline(pts, stroke=RED, w=2.4)
    for x0, y0, x1, y1 in ((52, 108, 72, 123), (218, 84, 202, 64), (66, 248, 52, 196), (138, 266, 111, 265),
                           (222, 248, 103, 193), (297, 249, 278, 198), (350, 249, 325, 197), (82, 304, 40, 291),
                           (251, 304, 211, 323)):
        f.line((x0, y0), (x1, y1), stroke=BLUE, w=2.2)
        _arrow_tip(f, x0, y0, x1, y1, BLUE, size=13, w=2.4)
    it = dict(italic=True)
    T = 29
    f.text(30, 22, "Z_{L}", size=T, **it)
    f.text(30, 388, "Z_{C}", size=T, **it)
    f.fit(365, 472, 70, "+j 350 Ω", **it)
    f.fit(370, 482, 332, "–j 350 Ω", **it)
    f.fit(370, 435, 181, "R (Ω)", **it)
    for x0, x1, t in ((32, 58, "36"), (244, 286, "600"), (302, 344, "750")):
        f.fit(x0, x1, 172, t, **it)
    f.text(30, 98, "^{3}/_{8}λ", size=T, **it)
    f.fit(220, 278, 98, "0,46λ", **it)
    f.text(50, 272, "λ/4", size=T, **it)
    f.text(145, 272, "^{5}/_{8}λ", size=T, **it)
    f.text(215, 272, "^{3}/_{4}λ", size=T, **it)
    f.text(289, 272, "λ", size=T, **it)
    f.text(334, 272, "λ/2", size=T, **it)
    f.text(85, 308, "λ/8", size=T, **it)
    f.fit(260, 315, 306, "0,54λ", **it)
    f.fit(147, 395, 360, "Diagramme de Smith", **it)
    f.fit(95, 474, 393, "Impédance d’un fouet vertical", **it)
    f.fit(82, 457, 427, "en fonction de la longueur du fil", **it)


GREEN_E = "#00b050"


def _vec(f, x0, y0, x1, y1, color, filled, w=3, size=18):
    if filled:
        a = math.atan2(y1 - y0, x1 - x0)
        f.line((x0, y0), (x1 - 0.8 * size * math.cos(a), y1 - 0.8 * size * math.sin(a)), stroke=color, w=w)
        _arrow_tip(f, x0, y0, x1, y1, color, size=size, filled=True)
    else:
        f.line((x0, y0), (x1, y1), stroke=color, w=w)
        _arrow_tip(f, x0, y0, x1, y1, color, size=size, w=w)


@figure("c083_2#0")
def polarisation(f):
    T = 29
    f.fit(31, 203, 39, "Doublet λ/2 en")
    f.fit(49, 186, 73, "polarisation")
    f.fit(52, 182, 108, "horizontale")
    f.line((6, 125.5), (109, 125.5), (109, 166), w=3.4)
    f.line((233, 125.5), (129, 125.5), (129, 166), w=3.4)
    _vec(f, 260, 124, 260, 49, RED, True)
    _vec(f, 260, 124, 333, 124, GREEN_E, False)
    f.line((260, 124), (360, 27), stroke=BLUE, w=2.2, dash=[6, 4], cap="b")
    _arrow_tip(f, 260, 124, 362, 25, BLUE, size=14, w=2.2)
    f.text(253, 38, "H", size=T, color=RED)
    f.text(307, 112, "E", size=T, color=GREEN_E)
    for x0, x1, y, t in ((368, 475, 31, "Direction"), (364, 475, 66, "du champ"), (389, 475, 99, "électro-"),
                         (342, 475, 132.5, "magnétique")):
        f.fit(x0, x1, y, t, color=BLUE)
    f.fit(553, 650, 34, "Antenne")
    f.fit(553, 651, 69, "verticale")
    f.fit(586, 620, 104, "λ/4")
    f.rect(574, 139, 208, 18, stroke=None, fill="#c0c0c0")
    f.line((678, 24), (678, 106.5), (652, 106.5), w=3.4)
    f.line((652, 132.5), (678, 132.5), (678, 140), w=3.4)
    _vec(f, 705, 101, 705, 27.5, GREEN_E, False)
    _vec(f, 705, 101, 783, 101, RED, True)
    f.line((705, 101), (791, 15), stroke=BLUE, w=2.2, dash=[6, 4], cap="b")
    _arrow_tip(f, 705, 101, 793, 13, BLUE, size=14, w=2.2)
    f.text(712, 36, "E", size=T, color=GREEN_E)
    f.text(760, 92, "H", size=T, color=RED)
    for x0, x1, y, t in ((803, 908, 31, "Direction"), (797, 908, 66, "du champ"), (822, 909, 99, "électro-"),
                         (776, 908, 134, "magnétique")):
        f.fit(x0, x1, y, t, color=BLUE)
    _vec(f, 1044, 149, 1044, 72, RED, True)
    _vec(f, 1044, 149, 1118, 149, GREEN_E, False)
    f.line((1044, 149), (1197, 6), stroke=BLUE, w=2.2, dash=[6, 4], cap="b")
    _arrow_tip(f, 1044, 149, 1200, 4, BLUE, size=14, w=2.2)
    _vec(f, 1122.5, 78.5, 1175, 78.5, RED, True)
    _vec(f, 1122.5, 78.5, 1122.5, 125, GREEN_E, False)
    _vec(f, 1173, 26, 1173, 76, RED, True)
    _vec(f, 1173, 26, 1127, 26, GREEN_E, False)
    f.text(1040, 57.5, "H", size=T, color=RED)
    f.text(1145, 162, "E", size=T, color=GREEN_E)
    for x0, x1, y, t in ((1199, 1337, 48, "Polarisation"), (1223, 1336, 83, "Circulaire"), (1263, 1336, 118, "Droite")):
        f.fit(x0, x1, y, t, color=BLUE)


@figure("c084_1#0")
def multidoublet(f):
    w = 4
    f.line((1, 31.5), (347.5, 31.5), (347.5, 9), w=w)
    f.line((711, 31.5), (369.5, 31.5), (369.5, 8), w=w)
    f.line((347, 32), (85, 93.5), w=w)
    f.line((370, 32), (649, 93.5), w=w)
    f.rect(104.5, 21, 65, 43.5, stroke=BROWN, fill="#ffffff", lw=4)
    f.rect(544, 21, 65, 43.5, stroke=BROWN, fill="#ffffff", lw=4)
    for x0, y0, x1, y1 in ((481, 95, 133, 39), (481, 95, 572, 42)):
        f.line((x0, y0), (x1, y1), stroke=BROWN, w=2.4)
        _arrow_tip(f, x0, y0, x1, y1, BROWN, size=17, w=2.4)
    for x0, y0, x1, y1 in ((208, 145, 46, 38), (210, 113, 189, 77), (313, 114, 437, 55), (342, 128, 518, 40)):
        f.line((x0, y0), (x1, y1), stroke=BLUE, w=2.4)
        _arrow_tip(f, x0, y0, x1, y1, BLUE, size=17, w=2.4)
    f.fit(444, 504, 20, "1 et 2")
    f.text(630, 20, "2", size=28)
    f.text(633, 84, "3", size=28)
    f.fit(215, 318, 145, "Doublets", color=BLUE)
    f.fit(407, 732, 126, "Trappes bloquant la bande 1", color=BROWN)
    f.fit(410, 732, 162, "et modifiant la longueur des", color=BROWN)
    f.fit(462, 679, 191, "brins de la bande 2", color=BROWN)
    f.fit(113, 594, 226, "Antenne 3 bandes multi-doublet à trappes")


@figure("c084_2#0")
def trombone(f):
    _hdarrow(f, 6, 396, 36, s=14, w=2.2)
    f.fit(131, 232, 24, "L = λ / 2", bold=True, color=NAVY)
    f.line((187.5, 129), (187.5, 88.5), (4, 88.5), (4, 61.5), (397.5, 61.5), (397.5, 88.5), (213.5, 88.5),
           (213.5, 129), w=3.6)
    f.rich(136, 143, [("Z =", {"u": 1})], size=27)
    f.rich(229, 143, [("300 Ω", {"u": 1})], size=27)
    f.fit(38, 362, 178, "Exemple d’antenne fermée :")
    f.fit(42, 360, 212, "le doublet demi-onde replié")
    f.text(201, 246, "(trombone)", size=27, anchor="c")


@figure("c084_3#0")
def patch(f):
    f.rect(25, 4.5, 243.5, 128.5, stroke=BLACK, fill="#dbeef4", lw=2)
    f.rect(181, 13, 83, 109.5, stroke=BLACK, fill="#a6a6a6", lw=2)
    f.rect(25, 64, 110, 11.5, stroke=None, fill=BLACK)
    f.line((134, 69.5), (181, 69.5), w=3)
    _hdarrow(f, 139, 179, 80.5, s=10, w=2.2)
    _hdarrow(f, 183, 262, 139.5, s=10, w=2.2)
    f.line((281.5, 24), (281.5, 111), stroke=BLUE, w=2.2)
    f.poly([(281.5, 14), (276, 26), (287, 26)], stroke=None, fill=BLUE)
    f.poly([(281.5, 121), (276, 109), (287, 109)], stroke=None, fill=BLUE)
    it = dict(italic=True)
    f.fit(33, 169, 37, "Substrat (ε)", **it)
    f.fit(190, 255, 57, "patch", **it)
    f.fit(128, 162, 112, "λ/4", **it)
    f.text(304, 100, "W", size=28, rot=-90, anchor="c", va="middle", **it)
    t = "0,5 L < W < 2 L"
    f.text(342, 100, t, size=10.0 * 186 / text_width(t, 10.0, italic=True), rot=-90, anchor="c", va="middle", **it)
    f.fit(155, 306, 172, "L = 0,5 λ/√ε", **it)
    f.fit(7, 305, 205, "Z(Ω) = 90(ε²/(ε-1))(L/W)²", **it)


@figure("c084_4#0")
def parabole(f):
    f.spline([(50, 19), (36, 60), (24, 113), (32, 160), (50, 206)], w=3.6)
    f.line((10.5, 20), (10.5, 209), stroke=BLUE, w=2.4)
    f.poly([(10.5, 8), (4.5, 22), (16.5, 22)], stroke=None, fill=BLUE)
    f.poly([(10.5, 221), (4.5, 207), (16.5, 207)], stroke=None, fill=BLUE)
    _hdarrow(f, 24, 279, 223, s=14, w=2.4)
    _vec(f, 22, 244.5, 63, 244.5, BLUE, True, w=2.4, size=14)
    f.text(13, 194, "D", size=28)
    f.text(137, 210, "F", size=28)
    f.text(72, 255, "Y", size=28)
    nbi = dict(bold=True, italic=True, color=NAVY)
    f.fit(124, 269, 255, "Y = D²/16 F", **nbi)
    f.fit(152, 425, 64, "G (rapport) ≈ 6 (D/λ)²", **nbi)
    f.rect(281.5, 81.5, 108, 55, lw=3.6)
    f.text(335, 117, "Foyer", size=29, anchor="c")
    rd = dict(stroke=RED, w=2.6, dash=[8, 6], cap="b")
    f.line((390, 19), (53, 19), **rd)
    f.line((52, 19), (278, 112), **rd)
    f.line((279, 115), (41, 152), **rd)
    f.line((385, 152), (41, 152), **rd)
    for x0, y0, x1, y1 in ((390, 19, 275, 19), (390, 19, 52, 19), (52, 19, 279, 112), (279, 115, 40, 152),
                           (385, 152, 245, 152), (385, 152, 40, 152)):
        _arrow_tip(f, x0, y0, x1, y1, RED, size=17, w=2.6)


@figure("c085_1#0")
def courants_coax(f):
    f.line((29, 79), (29, 252), w=2)
    f.line((179, 79), (179, 252), w=2)
    f.ellipse(104, 79, 75, 26, lw=2.2)
    f.rect(100, 4, 7, 75, stroke=None, fill=BLACK)
    f.line((103.5, 86), (103.5, 252), w=7, dash=[7, 8], cap="b")
    for x, y0, y1 in ((128.5, 11, 83), (178.5, 53, 5), (128.5, 154, 226), (153, 227, 154), (203, 154, 201)):
        _vec(f, x, y0, x, y1, RED, True, w=2.4, size=16)
    for x0, y0, x1, y1 in ((198, 85, 133, 43), (198, 85, 183, 58), (128, 302, 128, 258), (128, 302, 151, 257),
                           (228, 283, 204, 236)):
        f.line((x0, y0), (x1, y1), stroke=BLUE, w=2.2)
        _arrow_tip(f, x0, y0, x1, y1, BLUE, size=14, w=2.2)
    for x0, x1, y, t in ((200, 298, 39, "Courants"), (200, 240, 72, "non"), (200, 310, 104, "conjugués"),
                         (3, 134, 320, "Courants en"), (74, 133, 353, "mode"), (13, 133, 386, "différentiel"),
                         (174, 294, 320, "Courant de"), (174, 309, 353, "gaine (mode"), (174, 276, 386, "commun)")):
        f.fit(x0, x1, y, t, max_size=30)


@figure("c085_2#0")
def ligne_modele(f):
    w = 2.4
    dot = dict(w=2.4, dash=[2.2, 2.2], cap="b")
    f.line((0, 53), (108, 53), w=w)
    f.line((217, 53), (258, 53), w=w)
    f.line((343, 53), (551, 53), w=w)
    f.line((659, 53), (700, 53), w=w)
    f.line((785, 53), (868, 53), w=w)
    for x0, x1 in ((108, 217), (551, 659)):
        step = (x1 - x0) / 4
        pts = []
        for k in range(4):
            for i in range(17):
                a = math.pi * i / 16
                pts.append((x0 + k * step + step / 2 - math.cos(a) * step / 2 * 1.08, 50 - math.sin(a) * 19))
        f.line([(x0, 53)] + pts + [(x1, 53)], **dot)
    for x0 in (257, 700):
        f.rect(x0, 30, 86, 44, stroke=BLACK, lw=2.4, dash=[2.2, 2.2])
        f.text(x0 + 43, 64, "R2", size=29, anchor="c")
    for x in (383.5, 826):
        f.line((x, 53), (x, 74), w=w)
        f.rect(x - 21, 74, 42, 86, stroke=BLACK, lw=2.4, dash=[2.2, 2.2])
        f.text(x, 117, "R1", size=29, rot=-90, anchor="c", va="middle")
        f.line((x, 160), (x, 178), w=w)
        gnd(f, x - 21, 178, x + 21, 189)
    for x in (67, 510):
        f.line((x, 53), (x, 118), w=w)
        f.line((x - 20, 118), (x + 22, 118), **dot)
        f.line((x - 20, 140), (x + 22, 140), **dot)
        f.line((x, 140), (x, 178), w=w)
        gnd(f, x - 20, 178, x + 22, 189)
    f.text(8, 147, "C", size=29)
    f.text(533, 147, "C", size=29)
    f.text(155, 83, "L", size=29)
    f.text(598, 83, "L", size=29)
    for x0, x1, y, t in ((883, 969, 24, "coaxial"), (1005, 1097, 24, "bifilaire"), (906, 954, 59, "âme"),
                         (1027, 1074, 59, "fil 1"), (884, 1125, 122, "diélectrique (isolant)"),
                         (906, 972, 186, "tresse"), (1032, 1077, 186, "fil 2")):
        f.fit(x0, x1, y, t, max_size=30)


def _vdarrow(f, x, y0, y1, color=BLUE, w=2.4, s=11, half=5.5):
    f.line((x, y0 + s - 2), (x, y1 - s + 2), stroke=color, w=w)
    f.poly([(x, y0), (x - half, y0 + s), (x + half, y0 + s)], stroke=None, fill=color)
    f.poly([(x, y1), (x - half, y1 - s), (x + half, y1 - s)], stroke=None, fill=color)


def _rfit_mixed(f, x0, x1, y, parts, italic=True):
    """Runs of different sizes (ratio) fitted to x0..x1: parts=[(text, rel_size)]."""
    w = sum(text_width(t, 10.0 * r, "serif", False, italic) for t, r in parts)
    k = (x1 - x0) / w
    x = x0
    for t, r in parts:
        size = 10.0 * r * k
        f.text(x, y, t, size=size, italic=italic)
        x += text_width(t, size, "serif", False, italic)


@figure("c085_3#0")
def lignes(f):
    f.rect(10.5, 11.5, 1353, 233, lw=2)
    for x in (374.5, 692, 1047):
        f.line((x, 12), (x, 244), w=2)
    f.line((375, 45), (1364, 45), w=2)
    it = dict(italic=True)
    for x0, x1, y, t in ((35, 352, 40, "ε = coeff. diélectrique utilisé"), (28, 361, 73, "=1,1 à 1,2: air avec écarteurs"),
                         (101, 288, 106, "= 2,3 pour le PE"), (85, 302, 139, "= 2,1 pour le téflon"),
                         (65, 346, 172, "= 4,5 pour la fibre de verre"), (21, 363, 205, "Impédance (valeur approchée)")):
        f.fit(x0, x1, y, t, **it)
    rfit(f, 145, 365, 238, [("Vélocité (", I_), ("v = 1 / √ε", {"b": 1, "i": 1, "color": NAVY}), (")", I_)])
    nbi = dict(bold=True, italic=True, color=NAVY)
    # coaxial
    f.fit(460, 607, 38, "Coaxial rond", **it)
    f.circle(500, 110.5, 50, stroke=BLACK, fill="#d9d9d9", lw=2.4)
    f.circle(500, 110, 24, stroke=None, fill=BLACK)
    f.text(493, 77, "ε", size=27, **it)
    _vdarrow(f, 438.5, 63, 158)
    _vdarrow(f, 562.5, 91, 126)
    f.text(402, 113, "D", size=28, **it)
    f.text(571, 115, "d", size=28, **it)
    f.fit(389, 675, 205, "Z(Ω) = (138/√ε).log(D/d)", **nbi)
    _rfit_mixed(f, 389, 677, 238, [("66% ", 1), ("(PE)", 0.82), (" à 80% ", 1), ("(semi-aéré)", 0.82)])
    # two-wire line
    f.fit(790, 950, 38, "Ligne bifilaire", **it)
    for k in range(23):
        x = 806 + k * 6.5
        x1, y1 = x + 6, 128
        x0, y0 = x - 32, 166
        if x0 < 806:
            y0 = 166 - (806 - x0) * 38 / 38
            x0 = 806
        if x1 > 946:
            x1 = 946
        f.line((x0, y0), (min(x1, x0 + (y0 - 128)), max(128, y0 - (x1 - x0))), stroke="#909090", w=1)
    f.circle(786, 148.5, 19.5, stroke=None, fill=BLACK)
    f.circle(966, 148.5, 19.5, stroke=None, fill=BLACK)
    f.text(871, 152, "ε", size=27, **it)
    _hdarrow(f, 790, 966, 111, s=12)
    f.text(857, 92, "D", size=28, **it)
    _vdarrow(f, 754.5, 131, 167)
    f.text(732, 153, "d", size=28, **it)
    f.fit(720, 1020, 205, "Z(Ω) = (276/√ε).log(2D/d)", **nbi)
    _rfit_mixed(f, 755, 985, 238, [("95% ", 1), ("(écarteurs espacés)", 0.82)])
    # microstrip
    _rfit_mixed(f, 1065, 1345, 38, [("Microstrip ", 1), ("(circuit imprimé)", 0.82)])
    f.rect(1124, 109, 157, 42, stroke=None, fill="#c0c0c0")
    f.rect(1124, 151, 157, 13, stroke=None, fill=BLACK)
    f.rect(1186, 98, 35, 12, stroke=None, fill=BLACK)
    _hdarrow(f, 1185, 1220, 85.5, s=10)
    f.text(1199, 74, "L", size=28, **it)
    _vdarrow(f, 1102, 114, 149)
    f.text(1068, 138, "D", size=28, **it)
    f.text(1194, 135, "ε", size=27, **it)
    f.fit(1060, 1349, 205, "Z(Ω)=(138/√ε).log(4D/L)", **nbi)
    _rfit_mixed(f, 1067, 1345, 238, [("50% ", 1), ("(bakélite, fibre de verre)", 0.82)])


@figure("c086_1#0")
def adaptation_puissance(f):
    T = 30
    for (xa, ya, xl, yl, rb, rn, lab, val, valx, valy, gy, v_x, v_y) in (
            (12.5, 41, 41, 38.5, (66.5, 11.5, 230.5, 75), (247.5, 54.5, 339, 134), "R1", "25 Ω", 350, 93, 162, 28, 119),
            (472.5, 41, 502, 38.5, (527, 10.5, 691, 73.5), (705.5, 54.5, 799, 136.5), "R2", "50 Ω", 807, 94, 162, 487,
             119),
            (960.5, 28, 990, 30.5, (1015.5, 4.5, 1178, 68), (1189, 55.5, 1287, 135), "R3", "75 Ω", 1298, 104, 154, 975,
             120)):
        x0, y0, x1, y1 = rb
        _vec(f, xa, ya + 94 if xa != 960.5 else 129, xa, ya, BLUE, True, w=2.4, size=16)
        f.line((xl, yl), (x0, yl), w=2)
        f.rect(x0, y0, x1 - x0, y1 - y0, lw=4)
        f.text((x0 + x1) / 2, (y0 + y1) / 2 + 10, "R =50 Ω", size=T, anchor="c")
        cx = (rn[0] + rn[2]) / 2 + (-9 if lab != "R3" else -6)
        f.line((x1, yl), (cx, yl), (cx, rn[1]), w=2)
        f.rect(rn[0], rn[1], rn[2] - rn[0], rn[3] - rn[1], lw=4)
        f.text((rn[0] + rn[2]) / 2, (rn[1] + rn[3]) / 2 + 10, lab, size=T, anchor="c")
        f.line((cx, rn[3]), (cx, gy), w=2)
        gnd(f, cx - 26.5, gy, cx + 26.5, gy + 11)
        f.text(valx, valy, val, size=T)
        f.text(v_x, v_y, "141 V", size=T)
    f.fit(14, 1336, 201, "La loi de Joule (P_{R} = R . I²) est appliquée sachant que, pour chacun des cas, "
                         "la loi d’Ohm dit : I = U / (R + Rn)")
    f.fit(50, 360, 236, "P_{R1} = R1 . [U / (R + R1)]²")
    f.fit(49, 363, 268, "= 25 x (141 / 75)² = 89 W")
    f.fit(477, 786, 236, "P_{R2} = R2 . [U / (R + R2)]²")
    rfit(f, 459, 802, 268, [("= 50 x (141 / 100)² = ", {}), ("100 W", {"b": 1})])
    f.fit(1010, 1321, 236, "P_{R3} = R3 . [U / (R + R3)]²")
    f.fit(1015, 1316, 268, "75 x (141 / 125)² = 96 W")


OLIVE = "#76923c"
BROWN2 = "#984806"


@figure("c087_2#0")
def quart_onde_adapt(f):
    f.line((65, 69.5), (308, 69.5), w=2.2)
    f.line((65, 122.5), (308, 122.5), w=2.2)
    f.ellipse(65, 96, 13, 26.5, stroke=BLACK, fill="#ffffff", lw=2.2)
    f.arc(308, 96, 13, 26.5, -90, 90, w=2.2)
    f.arc(308, 96, 13, 26.5, 90, 270, w=2.2)
    f.line((25, 96), (65, 96), w=2)
    f.line((65, 96), (320, 96), w=1.4, dash=[1.4, 2], cap="b")
    f.line((320, 96), (348, 96), w=2)
    _hdarrow(f, 70, 310, 155.5, s=15, w=2.6, )
    f.fit(161, 198, 151, "λ/4", italic=True)
    si = dict(family="sans", italic=True)
    f.text(2, 22, "Z_{e} =", size=25, color=RED, **si)
    f.fit(75, 265, 22, "ROS = 1,125 / 1", **si)
    f.text(280, 22, "Z_{s} =", size=25, color=RED, **si)
    f.fit(3, 62, 56, "50 Ω", color=RED, **si)
    f.text(100, 56, "Z_{c} = 75 Ω", size=25, **si)
    f.fit(283, 356, 57, "100 Ω", color=RED, **si)


@figure("c087_3#0")
def transformation_lignes(f):
    f.rect(107, 54, 917, 14, stroke=None, fill=BLACK)
    f.line((108, 24), (108, 83), w=2)
    f.line((1024, 24), (1024, 83), w=2)
    for x, lab in ((290, "λ/4"), (474, "λ/2"), (657, "3λ/4"), (840, "λ"), (1024, "λ/4")):
        f.line((x, 30), (x, 83), w=2)
        f.text(x, 38, lab, size=29, anchor="c")
    f.text(7, 81, "Z_{e}", size=29)
    for cx, t in ((290, "Z_{s} = Z_{c}² / Z_{e}"), (474, "Z_{s} = Z_{e}"), (657, "Z_{s} = Z_{c}² / Z_{e}"),
                  (840, "Z_{s} = Z_{e}"), (1024, "Z_{s} = Z_{c}² / Z_{e}")):
        f.text(cx, 120, t, size=29, anchor="c")
    f.poly([(1175, 126.5), (1257, 1), (1339, 126.5)], stroke=BLUE, w=2.4)
    f.text(1236, 66, "Z_{c}²", size=29)
    f.text(1211, 121, "Z_{e}", size=29)
    f.text(1275, 121, "Z_{s}", size=29)


@figure("c087_4#0")
def ros_tos(f):
    sans = dict(family="sans")
    rd = dict(stroke=RED, w=2, dash=[1.6, 2.4], cap="b")
    f.line((63, 27.5), (410, 27.5), **rd)
    f.line((85, 44), (410, 44), **rd)
    f.line((23, 60.5), (410, 60.5), **rd)
    f.spline([(135, 53), (155, 36), (176.7, 26.7), (203, 40), (230, 59), (258, 42), (286.7, 27), (318, 42),
              (348, 59), (380, 43), (411.7, 28)], stroke=RED, w=2.2)
    f.spline([(133, 33), (155, 50), (176.7, 60), (203, 46), (230, 29), (258, 43), (286.7, 57), (318, 42),
              (348, 26), (380, 41), (411.7, 58)], stroke=BLUE, w=2.2)
    for x in (176.7, 287, 349):
        f.line((x, 27), (x, 111), w=1.8, dash=[5, 3.5], cap="b")
    f.line((107, 111), (412, 111), w=2.4)
    f.line((411.5, 111), (411.5, 12), w=2.4)
    f.poly([(404, 15), (411.5, 0), (419, 15)], stroke=None, fill=BLACK)
    for x, tip, col, heads in ((11, 60, OLIVE, 1), (63, 28, OLIVE, 1), (80, 31, BROWN2, 2)):
        f.line((x, 112), (x, tip + 12), stroke=col, w=2.4)
        f.poly([(x - 7, tip + 14), (x, tip), (x + 7, tip + 14)], stroke=None, fill=col)
        if heads == 2:
            f.poly([(x - 7, 58), (x, 44), (x + 7, 58)], stroke=None, fill=col)
    f.fit(15, 53, 33, "1,25", color=OLIVE, **sans)
    f.text(15, 60, "1", size=22, color=OLIVE, **sans)
    f.fit(15, 58, 110, "ROS", color=OLIVE, **sans)
    f.fit(95, 128, 33, "11%", color=BROWN2, **sans)
    f.fit(95, 118, 52, "0%", color=BROWN2, **sans)
    f.fit(88, 130, 110, "TOS", color=BROWN2, **sans)
    f.fit(147, 347, 85, "Z_{e} = Z_{cable} = 50Ω", **sans)
    f.text(163, 110, "λ", size=24, **sans)
    f.text(250, 110, "λ/2", size=24, **sans)
    f.text(312, 110, "λ/4", size=24, **sans)
    f.fit(421, 468, 34, "10 V", color=BLUE, **sans)
    f.fit(483, 552, 34, "0,20 A", color=RED, **sans)
    f.fit(433, 467, 61, "8 V", color=BLUE, **sans)
    f.fit(483, 552, 61, "0,16 A", color=RED, **sans)
    f.fit(417, 570, 105, "Z_{charge} = 40Ω", **sans)


@figure("c088_1#0")
def balun(f):
    w = 2.4
    _humps(f, 190, 320, 30.5, 5, 21, w=w)
    f.line((139, 30.5), (190, 30.5), w=w)
    f.line((320, 30.5), (371, 30.5), w=w)
    f.line((320, 31), (196, 55), (190, 55), (190, 82), w=w)
    _humps(f, 190, 320, 82, 5, 21, w=w)
    f.line((320, 82), (196, 107), (190, 107), (190, 142.5), (170, 142.5), w=w)
    _humps(f, 190, 320, 134, 5, 21, w=w)
    f.line((320, 134), (371, 134), w=w)
    gnd(f, 158, 117, 170, 168)
    _humps(f, 320, 475, 298, 6, 26, w=w)
    f.line((320, 298), (320, 360), w=w)
    f.line((372.5, 247), (372.5, 298), w=w)
    f.line((475.5, 247), (475.5, 298), w=w)
    f.line((424.5, 298), (424.5, 319), w=w)
    gnd(f, 399, 319, 450, 330)
    red = dict(color=RED)
    f.fit(94, 140, 49, "âme")
    f.fit(75, 140, 151, "tresse")
    f.fit(5, 74, 82, "entrée", **red)
    f.fit(5, 143, 116, "asymétrique", **red)
    f.fit(343, 405, 67, "sortie", **red)
    f.fit(343, 468, 101, "symétrique", **red)
    f.fit(394, 456, 205, "sortie", **red)
    f.fit(363, 488, 239, "symétrique", **red)
    f.fit(305, 350, 361, "âme")
    f.fit(404, 467, 361, "tresse")
    f.fit(278, 494, 394, "entrée asymétrique", **red)
    for y, x1, t in ((202, 237, "Représentation d’un"), (236, 248, "balun en tension 1/1 :"),
                     (270, 222, "en haut, réalisation"), (304, 255, "d’un bobinage « 3 fils"),
                     (338, 247, "en main » ; ci-contre,"), (372, 193, "les trois fils sont"),
                     (406, 234, "représentés l’un à la"), (440, 180, "suite de l’autre.")):
        f.text(5, y, t, size=29.5)


@figure("c088_2#0")
def stub(f):
    w = 2.2
    f.line((0, 12.5), (404, 12.5), w=w)
    f.line((0, 70.5), (72, 70.5), w=w)
    f.line((250, 70.5), (404, 70.5), w=w)
    f.line((0, 41.5), (57, 41.5), w=1.4, dash=[1.4, 2.2], cap="b")
    f.line((262, 41.5), (404, 41.5), w=1.4, dash=[1.4, 2.2], cap="b")
    f.ellipse(71, 41.5, 14.5, 28.5, lw=w)
    f.ellipse(245, 41.5, 14.5, 28.5, lw=w)
    f.circle(57, 12, 8.5, stroke=None, fill=BLACK)
    f.circle(260, 12, 8.5, stroke=None, fill=BLACK)
    f.spline([(57, 41.5), (90, 47), (118, 65), (136, 88), (143, 110), (144, 127)], w=w)
    f.spline([(261, 41.5), (225, 48), (195, 66), (180, 88), (174, 110), (173, 116)], w=w)
    f.line((114.5, 114), (114.5, 284), w=w)
    f.line((173, 114), (173, 325), (143.5, 325), (143.5, 295), w=w)
    f.ellipse(144, 114, 29.5, 14.5, lw=w)
    f.ellipse(144, 280.5, 29.5, 14.5, lw=w)
    f.line((144, 128), (144, 293), w=1.4, dash=[1.4, 2.2], cap="b")
    _hdarrow(f, 116, 200, 44.5, s=14, w=2.4)
    _vdarrow(f, 202, 123, 283, s=17, half=8, w=2.4)
    f.line((259, 323), (182, 316), stroke=BLUE, w=2.4)
    _arrow_tip(f, 259, 323, 180, 316, BLUE, size=20, w=2.4)
    f.text(139, 92, "Z_{e}", size=29)
    f.fit(226, 465, 161, "Longueur du câble :")
    f.fit(227, 465, 201, "si λ/4, alors Z_{e} = ∞")
    f.fit(227, 463, 241, "si λ/2, alors Z_{e} = 0")
    f.fit(271, 441, 336, "Ligne fermée")


@figure("c088_3#0")
def lignes_ouvertes_fermees(f):
    f.rect(1.5, 1.5, 1361, 256, lw=1.8)
    for y in (111, 184):
        f.line((2, y), (1363, y), w=1.8)
    for x in (283, 577, 953):
        f.line((x, 2), (x, 258), w=1.8)
    f.line((2, 22), (282, 79), w=1.2)
    f.line((306, 135.5), (539, 135.5), w=2.4)
    f.line((306, 156.5), (539, 156.5), w=2.4)
    f.line((306, 216), (541, 216), (541, 236.5), (306, 236.5), w=2.4)
    T = 29
    cells = ((62, 223, 32, "Type de ligne"), (26, 260, 102, "impédance de sortie"), (388, 474, 30, "schéma"),
             (598, 938, 35, "quart d'onde (λ/4) et nombre"), (688, 845, 69, "impair de λ/4"),
             (617, 914, 103, "Inversion de l’impédance"), (998, 1316, 35, "demi-onde (λ/2) et nombre"),
             (1084, 1230, 69, "entier de λ/2"), (1017, 1299, 103, "Recopie de l’impédance"),
             (61, 223, 140, "Ligne ouverte"), (59, 226, 177, "Z_{s} = ∞ (infini)"),
             (617, 914, 140, "Impédance d’entrée nulle"), (612, 916, 177, "Z_{e} = Z_{C}² / Z_{s} = Z_{C}² / ∞ = 0"),
             (998, 1315, 140, "Impédance d’entrée infinie"), (1094, 1221, 177, "Z_{e}= Z_{s} = ∞"),
             (65, 220, 213, "Ligne fermée"), (107, 177, 249, "Z_{s} = 0"),
             (609, 923, 213, "Impédance d’entrée infinie"), (612, 916, 251, "Z_{e} = Z_{C}² / Z_{s} = Z_{C}² / 0 = ∞"),
             (1009, 1306, 213, "Impédance d’entrée nulle"), (1094, 1221, 251, "Z_{e} = Z_{s} = 0"))
    for x0, x1, y, t in cells:
        f.text((x0 + x1) / 2, y, t, size=T, anchor="c")


@figure("c088_4#0")
def filtres_cavites(f):
    w = 2.2
    f.rect(3.5, 11, 879, 393.5, lw=1.8)
    for y in (44, 207, 272, 338):
        f.line((4, y), (883, y), w=1.8)
    for x in (167.5, 524.5):
        f.line((x, 12), (x, 405), w=1.8)
    it = dict(italic=True)
    T = 28
    for cx, y, t in ((85, 36, "Montage"), (346, 36, "Passe bande"), (703, 36, "Réjecteur"), (85, 136, "Schéma"),
                     (85, 232, "Choix des"), (85, 265, "fréquences"), (346, 250, "Écart A / B = 6% minimum"),
                     (703, 250, "Écart A / B = 3% minimum"), (85, 315, "Avantage"), (346, 299, "Filtre par rapport à"),
                     (346, 331, "l’environnement"), (703, 315, "Peu de pertes d’insertion"), (85, 364, "Si plus de 2"),
                     (85, 396, "fréquences"), (346, 364, "Ajout facile d’un autre"), (346, 396, "élément"),
                     (703, 364, "Difficile de séparer plus de 2"), (703, 396, "fréquences")):
        f.text(cx, y, t, size=T, anchor="c", **it)
    red = dict(size=T, color=RED, italic=True)
    # band-pass
    f.text(316, 86, "Entrée", **red)
    f.line((351.5, 99), (351.5, 177), w=w)
    f.line((235, 176.5), (273, 176.5), w=w)
    f.line((313, 176.5), (411, 176.5), w=w)
    f.line((451, 176.5), (489, 176.5), w=w)
    for x0, lab in ((273, "B"), (411, "A")):
        f.rect(x0, 156.5, 40, 40, lw=w)
        f.text(x0 + 20, 186, lab, size=T, anchor="c", **it)
    f.text(198, 184, "B", **red)
    f.text(492, 184, "A", **red)
    # band-stop
    f.text(675, 67, "Entrée", **red)
    f.line((575, 109), (849, 109), w=w)
    f.line((710, 99), (710, 109), w=w)
    for x0, cx, lab in ((613, 633.5, "B"), (771, 790.5, "A")):
        f.line((cx, 109), (cx, 128), w=w)
        f.rect(x0, 128, 40, 40, lw=w)
        f.text(x0 + 20, 158, lab, size=T, anchor="c", **it)
        f.line((cx, 168), (cx, 190), w=w)
        gnd(f, cx - 23, 190, cx + 23, 200)
    f.text(537, 117, "A", **red)
    f.text(851, 117, "B", **red)
    # cavity
    f.line((982, 124.5), (1080, 124.5), w=5)
    f.line((1153, 124.5), (1251, 124.5), w=5)
    f.line((1004.5, 124), (1004.5, 372), (1225.5, 372), (1225.5, 124), w=5, cap="b")
    f.rect(1079, 100, 74, 49, lw=2)
    f.rect(1079, 150, 74, 74, lw=1.6)
    f.rect(1079, 224, 74, 49, stroke=BLACK, fill="#c0c0c0", lw=2)
    f.rect(1079, 25.5, 74, 25, lw=2)
    for k in range(25):
        x = 1081 + k * 3
        f.line((x, 27), (x, 50), w=1)
    for y0, y1 in ((51, 99), (150, 223)):
        f.rect(1103, y0, 25, y1 - y0, stroke=BLACK, fill="#ffffff", lw=1.6)
        k = 0
        y = y0 - 25
        while y < y1:
            ya, yb = max(y, y0), min(y + 25, y1)
            xa = 1103 + (y + 25 - ya) if False else 1103
            # diagonal stripes "/" clipped to the screw
            p0 = (1103 + max(0, y0 - y), min(y + 25, y1))
            p0 = (1103 + (y + 25 - min(y + 25, y1)), min(y + 25, y1))
            p1 = (1103 + (y + 25 - max(y, y0)) if y < y0 else 1128, max(y, y0))
            p1 = (min(1128, 1103 + (y + 25 - max(y, y0))), max(y, y0) if y + 25 - max(y, y0) <= 25 else y0)
            f.line(p0, p1, stroke=BLUE, w=2.4)
            y += 8
    for cx in (1041.5, 1189):
        f.rect(cx - 12.5, 76, 25, 49, lw=1.6)
        f.line((cx - 22, 88.5), (cx + 22, 88.5), w=2.6)
        f.line((cx - 18, 129), (cx - 15, 227), (cx + 1, 227), (cx - 2, 129), w=1.6)
        f.line((cx - 13, 152), (cx - 3, 152), w=1.8)
        f.line((cx - 13, 157), (cx - 3, 157), w=1.8)
    _vdarrow(f, 955.5, 229, 367, s=18, half=9, w=2)
    f.text(943, 298, "λ/4", size=T, rot=-90, anchor="c", va="middle", **it)
    f.line((1127.5, 282), (1127.5, 312), stroke=BLUE, w=1.4, dash=[1.4, 1.6], cap="b")
    f.line((1121, 289), (1127.5, 279), (1134, 289), stroke=BLUE, w=1.6)
    f.line((1121, 305), (1127.5, 315), (1134, 305), stroke=BLUE, w=1.6)
    f.fit(1031, 1184, 20, "vis de réglage", **it)
    f.text(992, 50, "entrée", **red)
    f.text(1162, 50, "sortie", **red)
    f.fit(1008, 1223, 410, "Schéma de principe", **it)
    f.fit(1049, 1183, 439, "d’une cavité", **it)


def _box_label(f, x0, y0, x1, y1, t, size=28, lw=2.6, bold=False):
    f.rect(x0, y0, x1 - x0, y1 - y0, lw=lw)
    f.text((x0 + x1) / 2, (y0 + y1) / 2 + size * 0.35, t, size=size, anchor="c", bold=bold)


def _speaker(f, x0, x1, y0, y1, flare):
    f.rect(x0, y0, x1 - x0, y1 - y0, stroke=None, fill=BLACK)
    f.poly([(x1, y0), (x1 + flare[0], y0 - flare[1]), (x1 + flare[0], y1 + flare[1]), (x1, y1)], w=2.6)


@figure("c089_1#0")
def recepteur_direct(f):
    w = 2.4
    f.line((122, 5), (145.5, 32), (169, 5), w=w)
    f.line((145.5, 6), (145.5, 65.5), (197, 65.5), w=w)
    _box_label(f, 197, 49, 259, 90, "RF1")
    f.line((259, 66.5), (324, 66.5), w=w)
    _box_label(f, 324, 49, 386, 90, "RF2")
    f.line((386, 68), (452, 68), w=w)
    _box_label(f, 452, 49, 555, 90, "Démod")
    f.line((555, 69.5), (588, 69.5), (588, 100), w=w)
    f.rect(580, 100, 26, 51, lw=2.4)
    f.line((593, 151), (593, 172), w=w)
    gnd(f, 581, 172, 605, 180)
    f.line((655, 124.5), (618, 124.5), w=w)
    f.poly([(620, 116), (606, 124.5), (620, 133)], stroke=None, fill=BLACK)
    f.poly([(655.5, 92), (731, 124.5), (655.5, 156)], w=2.6)
    f.text(665, 135, "AF", size=28)
    f.line((731, 124.5), (808, 124.5), w=w)
    _speaker(f, 808, 835, 99, 153, (26, 24))
    f.line((498.5, 0), (498.5, 249), stroke=RED, w=2.4, dash=[6, 3, 1.5, 3], cap="b")
    rb = dict(color=RED, bold=True)
    f.fit(447, 484, 138, "HF", **rb)
    f.fit(509, 542, 138, "BF", **rb)
    f.text(870, 136, "BF", size=28, color=RED)
    f.text(91, 75, "HF", size=28, color=RED)
    f.fit(1, 95, 28, "Antenne")
    f.fit(418, 579, 28, "Démodulateur")
    f.fit(640, 875, 33, "Amplificateur audio-")
    f.fit(616, 900, 66, "fréquences (ou étage AF)")
    f.fit(157, 417, 130, "1^{er} et 2^{ème} amplificateur")
    f.fit(195, 383, 163, "radio-fréquences")
    f.fit(204, 368, 197, "(ou étages RF)")
    f.fit(541, 699, 203, "Potentiomètre")
    f.fit(559, 681, 235, "Niveau BF")
    f.fit(738, 882, 210, "Haut-parleur")
    f.fit(765, 854, 242, "(ou HP)")


@figure("c089_2#0")
def superheterodyne(f):
    w = 2.4
    f.line((108, 0), (153.5, 42), (197, 0), w=w)
    f.line((153.5, 6), (153.5, 113.5), (219, 113.5), w=w)
    _box_label(f, 219, 91, 283, 135, "RF", bold=True)
    f.line((283, 113.5), (370, 113.5), w=w)
    _box_label(f, 370, 91, 456, 135, "Mél", bold=True)
    f.line((456, 113.5), (636, 113.5), w=w)
    _box_label(f, 636, 97.5, 702, 144, "FI", bold=True)
    f.line((702, 113.5), (877, 113.5), w=w)
    _box_label(f, 877, 89, 985, 135, "Démod", bold=True)
    f.line((985, 113.5), (1026, 113.5), w=w)
    _box_label(f, 1026, 89, 1098, 135, "AF", bold=True)
    f.line((1098, 113.5), (1139, 113.5), w=w)
    _speaker(f, 1139, 1163, 91, 136, (22, 22))
    f.line((413, 135), (413, 165), w=2)
    f.circle(413, 208, 42.5, lw=2)
    f.text(413, 218, "OL", size=28, anchor="c", bold=True)
    f.rect(331, 0.5, 495, 257.5, stroke=RED, lw=2.4, dash=[7, 3, 1.5, 3])
    f.poly([(838, 222), (850, 210), (850, 217.5), (888, 217.5), (888, 227), (850, 227), (850, 234)],
           stroke="#ff6060", w=2)
    for x0, x1, y, t in ((11, 105, 36, "Antenne"), (70, 128, 70, "(HF)"), (210, 290, 36, "Etage"),
                         (200, 299, 68, "d’entrée"), (200, 302, 165, "Filtre de"), (212, 290, 198, "bande"),
                         (345, 482, 61, "Mélangeur"), (518, 810, 45, "Fréquence Intermédiaire"),
                         (518, 806, 78, "FI = HF+FO ou HF– FO"), (842, 1020, 70, "Démodulateur"),
                         (1094, 1254, 59, "Haut-parleur"), (999, 1158, 182, "Ampli Audio"),
                         (465, 676, 196, "Oscillateur Local"), (462, 772, 238, "générant la fréquence FO")):
        f.fit(x0, x1, y, t, max_size=31)
    f.text(1191, 120, "BF", size=28)
    f.fit(900, 1374, 220, "Modification du récepteur : évolution récepteur", color=RED)
    f.fit(900, 1347, 251, "sans conversion ⇒ récepteur superhétérodyne", color=RED)


@figure("c090_2#0")
def emetteur(f):
    w = 2.4
    f.circle(45, 83, 20, lw=2.4)
    f.rect(66, 61, 22, 44, stroke=None, fill=BLACK)
    f.line((88, 83), (118, 83), w=w)
    _box_label(f, 118, 61.5, 182, 104.5, "AF", size=29)
    f.line((182, 86.5), (222, 86.5), w=w)
    _box_label(f, 222, 61.5, 286, 104.5, "Mod", size=29)
    f.line((286, 85), (327, 85), w=w)
    _box_label(f, 327, 61.5, 411, 114.5, "Mél", size=29)
    f.line((411, 83.5), (445, 83.5), w=w)
    _box_label(f, 445, 57.5, 509, 99.5, "PA", size=29)
    f.line((509, 81.5), (571, 81.5), w=w)
    _box_label(f, 571, 57.5, 676, 99.5, "Filtre", size=29)
    f.line((676, 79.5), (719, 79.5), (719, 2), w=w)
    f.line((697, 1), (719, 40), (741, 1), w=w)
    f.line((380, 114.5), (380, 167), w=w)
    f.circle(380, 210, 42.5, lw=2.4)
    f.text(380, 220, "OL", size=29, anchor="c")
    f.line((252.5, 0), (252.5, 185), stroke=RED, w=2.2, dash=[6, 3, 1.5, 3], cap="b")
    rb = dict(color=RED, bold=True)
    f.fit(202, 238, 36, "BF", **rb)
    f.fit(261, 300, 36, "HF", **rb)
    for x0, x1, y, t in ((3, 82, 25, "Micro-"), (2, 72, 60, "phone"), (593, 689, 29, "Antenne"),
                         (324, 449, 42, "Mélangeur"), (195, 329, 145, "Modulateur"), (92, 207, 178, "Ampli AF"),
                         (424, 532, 131, "Ampli de"), (421, 535, 165, "puissance"), (564, 685, 131, "Filtre anti-"),
                         (564, 700, 165, "harmonique"), (564, 673, 199, "passe-bas"), (415, 613, 229, "Oscillateur Local")):
        f.fit(x0, x1, y, t, max_size=30)


@figure("c090_3#0")
def filtre_bande_fi(f):
    for x0, x1 in ((8.5, 341), (423.5, 1248)):
        f.line((x0, 38), (x0, 166.5), (x1, 166.5), w=2)
        f.poly([(x0 - 6, 52), (x0, 36), (x0 + 6, 52)], stroke=None, fill=BLACK)
        f.line((x1 - 14, 160), (x1, 166.5), (x1 - 14, 173), w=2)
    f.line((864.5, 63), (864.5, 167), w=2)
    red1 = [(18, 124), (28, 120), (38, 114), (48, 102), (58, 115), (68, 132), (78, 131), (88, 140), (98, 142),
            (108, 144), (115, 134), (123, 148), (128, 155), (138, 132), (148, 143), (163, 141), (183, 138), (193, 108),
            (198, 112), (208, 150), (213, 152), (223, 125), (233, 152), (248, 143), (263, 104), (278, 80), (288, 110),
            (293, 146), (313, 132), (318, 147), (323, 143), (330, 142)]
    f.line(red1, stroke=RED, w=2)
    red2 = [(475, 119), (485, 135), (495, 132), (505, 138), (515, 144), (525, 141), (530, 128), (540, 154),
            (545, 154), (555, 133), (560, 143), (575, 138), (595, 140), (600, 134), (610, 104), (615, 122),
            (625, 153), (635, 133), (640, 124), (650, 152), (670, 131), (680, 100), (690, 82), (700, 97),
            (705, 130), (710, 149), (725, 134), (733, 140)]
    f.line(red2, stroke=RED, w=2)
    f.line([(1048, 127), (1056, 125), (1062, 102), (1068, 91), (1072, 97), (1077, 124), (1083, 140), (1086, 139),
            (1092, 126), (1096, 116)], stroke=RED, w=2)
    bd = dict(stroke=BLUE, w=1.6, dash=[1.6, 2.4], cap="b")
    f.spline([(448, 160), (470, 142), (482, 86), (500, 58), (530, 45), (580, 41), (640, 44), (680, 52), (700, 63),
              (716, 82), (728, 119), (740, 151), (760, 159)], **bd)
    f.spline([(990, 158), (1028, 149), (1044, 135), (1050, 90), (1056, 33), (1068, 28), (1084, 32), (1092, 66),
              (1100, 130), (1108, 152), (1130, 158)], **bd)
    f.line((830, 115), (899, 115), **bd)
    _arrow_tip(f, 860, 115, 817, 115, BLUE, size=15, w=1.8)
    _arrow_tip(f, 860, 115, 911, 115, BLUE, size=15, w=1.8)
    for x0, y0, x1, y1 in ((195.5, 34, 195.5, 88), (646, 11, 582, 36), (1149, 41, 1101, 102)):
        f.line((x0, y0), (x1, y1), stroke=BLUE, w=2)
        _arrow_tip(f, x0, y0, x1, y1, BLUE, size=16, filled=True)
    T = 29
    f.fit(57, 294, 23, "Signal HF à recevoir")
    f.fit(653, 824, 23, "Filtre de bande")
    f.fit(1121, 1295, 27, "Signal adjacent")
    f.fit(32, 318, 196, "Signal reçu par l’antenne")
    f.text(355, 182, "F", size=T)
    f.fit(446, 786, 196, "Signal après le filtre de bande")
    f.fit(847, 885, 196, "OL")
    f.fit(955, 1240, 196, "FI (récepteur supradyne)")
    f.text(1264, 182, "F", size=T)


@figure("c092_1#0")
def modulations(f):
    T = 28
    f.rect(15, 16.5, 1382, 601.5, lw=2.4)
    f.line((15, 88.5), (1397, 88.5), w=2)
    for x in (131.5, 451, 748.5, 1068):
        f.line((x, 17), (x, 89), w=2)
    for cx, l1, l2 in ((73, "Représen", "tation"), (291, "AM - A3E", "Modulation d'Amplitude"),
                       (600, "BLU - J3E", "Bande Latérale Unique"), (908, "CW - A1A", "Télégraphie"),
                       (1232, "FM - F3E", "Modulation de Fréquence")):
        for y, t in ((45, l1), (79, l2)):
            size = min(T, 10.0 * 296 / text_width(t, 10.0)) if cx > 100 else min(T, 10.0 * 112 / text_width(t, 10.0))
            f.text(cx, y, t, size=size, anchor="c")
    for cx, cy, span, t in ((45, 188, 175, "en fonction du"), (80, 190, 168, "temps/oscillo-"), (117, 188, 95, "gramme"),
                            (45, 452, 201, "en fonction de la"), (80, 455, 120, "fréquence"),
                            (117, 455, 186, "spectrogramme")):
        f.text(cx, cy, t, size=10.0 * span / text_width(t, 10.0), rot=-90, anchor="c", va="middle")
    bd = dict(stroke="#6060ff", w=1.6, dash=[1.6, 2], cap="b")
    # AM oscillogram
    amp = lambda x: 56 + 27 * math.cos(2 * math.pi * (x - 205) / 210)
    f.curve(lambda x: 173 - amp(x), 160, 370, n=80, **bd)
    f.curve(lambda x: 173 + amp(x), 160, 370, n=80, **bd)
    f.curve(lambda x: 173 - amp(x) * math.cos(2 * math.pi * (x - 200) / 66), 170, 376, n=300, stroke=RED, w=2)
    f.line((162, 173.5), (396, 173.5), w=2.6)
    f.poly([(384, 166), (400, 173.5), (384, 181)], stroke=None, fill=BLACK)
    f.text(410, 186, "T", size=T)
    # SSB note
    for y, t in ((172, "La BLU ne peut pas"), (208, "être représentée en"), (241, "fonction du temps")):
        f.text(602, y, t, size=T, anchor="c")
    # CW oscillogram
    f.line((772, 108), (1032, 108), **bd)
    f.line((765, 235), (1027, 235), **bd)
    f.curve(lambda x: 173 - 64 * math.sin(2 * math.pi * (x - 783) / 47), 783, 877, n=120, stroke=RED, w=2)
    f.curve(lambda x: 173 - 64 * math.sin(2 * math.pi * (x - 930) / 47), 930, 1027, n=120, stroke=RED, w=2)
    f.line((775, 173.5), (1027, 173.5), w=2.6)
    f.poly([(1016, 166), (1032, 173.5), (1016, 181)], stroke=None, fill=BLACK)
    f.text(1040, 186, "T", size=T)
    # FM oscillogram
    f.line((1088, 108), (1350, 108), stroke="#6060ff", w=1.6)
    f.line((1088, 241), (1350, 241), stroke="#6060ff", w=1.6)
    pts = [(1090, 240), (1100, 140), (1112, 108), (1124, 160), (1135, 240), (1148, 150), (1160, 108), (1178, 160),
           (1197, 241), (1218, 150), (1238, 108), (1250, 170), (1260, 241), (1271, 150), (1282, 108), (1295, 175),
           (1307, 241), (1318, 210), (1325, 178)]
    f.spline(pts, stroke=RED, w=2, n=8)
    f.line((1090, 173.5), (1342, 173.5), w=2.6)
    f.poly([(1330, 166), (1346, 173.5), (1330, 181)], stroke=None, fill=BLACK)
    f.text(1352, 186, "T", size=T)
    # AM spectrum
    f.rect(190, 427, 172, 43, stroke=BLACK, fill="#a6a6a6", lw=2.4)
    f.line((191, 428), (275.5, 470), (361, 428), w=1.6)
    f.line((168, 470.5), (392, 470.5), w=2.2)
    f.poly([(390, 464), (404, 470.5), (390, 477)], stroke=None, fill=BLACK)
    f.text(410, 482, "f", size=T)
    f.line((275.5, 380), (275.5, 469), stroke=RED, w=2)
    f.line((330, 358), (293, 393), stroke=BLUE, w=2.2)
    _arrow_tip(f, 330, 358, 290, 396, BLUE, size=14, filled=True)
    f.text(286, 350, "Porteuse HF", size=T, anchor="c")
    f.text(233, 415, "BF", size=T, anchor="c")
    f.text(323, 415, "BF", size=T, anchor="c")
    f.text(215, 523, "BLI", size=T, anchor="c")
    f.text(331, 523, "BLS", size=T, anchor="c")
    # SSB spectrum
    f.rect(602, 486, 76, 45, stroke=BLACK, fill="#a6a6a6", lw=2.4)
    f.line((602, 531), (678, 486), w=1.6)
    f.line((504, 486), (504, 530), stroke="#808080", w=1.4, dash=[1.4, 1.6], cap="b")
    f.line((504, 487), (590, 530), stroke="#606060", w=1.2, dash=[2, 1.6], cap="b")
    f.line((588.5, 447), (588.5, 530), stroke="#808080", w=1.6)
    f.line((487, 530.5), (721, 530.5), w=2.2)
    f.poly([(719, 524), (733, 530.5), (719, 537)], stroke=None, fill=BLACK)
    f.text(738, 542, "f", size=T)
    for x1, y1 in ((528, 485), (591, 464)):
        f.line((550, 422), (x1, y1), stroke=BLUE, w=2.2)
        _arrow_tip(f, 550, 422, x1, y1, BLUE, size=14, filled=True)
    f.text(615, 367, "Porteuse et bande", size=T, anchor="c")
    f.text(615, 400, "latérale supprimées", size=T, anchor="c")
    f.text(643, 472, "BF", size=T, anchor="c")
    f.text(637, 578, "BLS", size=T, anchor="c")
    # CW note
    for y, t in ((441, "La CW ne peut pas être"), (474, "représentée en fonction"), (508, "de la fréquence")):
        f.text(908, y, t, size=T, anchor="c")
    # FM spectrum
    for x in (1123, 1252):
        f.line((x, 318), (x, 578), stroke="#4040ff", w=1.6, dash=[1.6, 2], cap="b")
    f.rect(1184, 330, 6, 107, stroke=None, fill=RED)
    f.line((1080, 442.5), (1306, 442.5), w=2.2)
    f.poly([(1302, 436), (1316, 442.5), (1302, 449)], stroke=None, fill=BLACK)
    f.text(1335, 455, "f", size=T)
    _hdarrow(f, 1123, 1250, 395, s=13, w=3.4, color="#5050ff")
    _hdarrow(f, 1190, 1247, 372.5, s=9, w=1.6)
    f.line((1187, 446), (1187, 566), w=1.4, dash=[1.6, 1.6], cap="b")
    f.poly([(1182, 562), (1187, 573), (1192, 562)], stroke=None, fill=BLACK)
    f.spline([(1187, 446), (1250, 466), (1205, 480), (1145, 505), (1175, 515), (1208, 522), (1170, 532), (1123, 540),
              (1185, 548), (1252, 560), (1187, 572)], w=1.4, n=8)
    f.text(1158, 470, "BF", size=24, rot=90, anchor="c", va="middle")
    f.text(1175, 584, "T", size=22, rot=90, anchor="c", va="middle")
    f.text(1156, 352, "HF", size=T, anchor="c")
    f.text(1303, 344, "Excursion", size=T, anchor="c")
    f.text(1310, 383, "ou swing", size=T, anchor="c")


def _crich(f, cx, y, parts, size=30, maxw=None):
    """Centered rich line (parts = [(text, style)]), shrunk to maxw if needed."""
    wsum = sum(text_width(t, 10.0, "serif", st.get("b"), st.get("i")) for t, st in parts) / 10.0
    if maxw and wsum * size > maxw:
        size = maxw / wsum
    f.rich(cx - wsum * size / 2, y, parts, size=size)


def _arrow_r(f, x0, x1, y, w=2.4, filled=False):
    if filled:
        f.line((x0, y), (x1 - 12, y), w=w)
        f.poly([(x1 - 14, y - 7), (x1, y), (x1 - 14, y + 7)], stroke=None, fill=BLACK)
    else:
        f.line((x0, y), (x1, y), w=w)
        f.line((x1 - 14, y - 8), (x1, y), (x1 - 14, y + 8), w=w)


@figure("c093_1#0")
def demodulateurs_modulateurs(f):
    T = 30
    N = {}
    f.rect(1, 1, 1363, 573, lw=2)
    f.line((1, 36), (1364, 36), w=1.8)
    f.line((1, 272), (1364, 272), w=1.8)
    for y, x0 in ((103, 75), (171, 75), (373, 75), (506, 75)):
        f.line((x0, y), (1364, y), w=1.8)
    for x in (75, 225, 515, 1084):
        f.line((x, 1), (x, 574), w=1.8)
    f.line((814, 1), (814, 36), w=1.8)
    f.line((814, 272), (814, 574), w=1.8)
    f.text(37, 154, "Démodulateurs", size=T, rot=-90, anchor="c", va="middle")
    f.text(37, 423, "Modulateurs", size=T, rot=-90, anchor="c", va="middle")
    for cx, t in ((370, "AM"), (665, "BLU"), (949, "CW"), (1224, "FM")):
        f.text(cx, 29, t, size=T, anchor="c")
    for y, t in ((80, "Nom"), (130, "Schéma"), (163, "synoptique"), (215, "Autres"), (248, "notions"),
                 (316, "Principe/"), (349, "Nom"), (433, "Schéma"), (466, "synoptique"), (534, "Autres"),
                 (567, "notions")):
        f.text(150, y, t, size=T, anchor="c")
    # AM
    _crich(f, 370, 64, [("Détection", BU), (" ou", N)], maxw=280)
    _crich(f, 370, 97, [("détecteur d’enveloppe", N)], maxw=280)
    f.text(252, 152, "FI", size=T)
    f.line((293, 142), (334, 142), w=2.4)
    _box_label(f, 334, 122, 398, 163, "Dét", size=T, lw=2.4)
    _arrow_r(f, 398, 437, 142, filled=True)
    f.text(443, 152, "BF", size=T)
    _crich(f, 370, 197, [("Contrôle Automatique", N)], maxw=280)
    _crich(f, 370, 230, [("de Gain (", N), ("CAG", BU), (")", N)], maxw=280)
    _crich(f, 370, 316, [("la HF de l’oscillateur", N)], maxw=280)
    _crich(f, 370, 349, [("est mélangée à la BF", N)], maxw=280)
    f.text(229, 412, "BF", size=T)
    f.line((270, 403), (311, 403), w=2.4)
    _box_label(f, 311, 383, 376, 424, "Mél", size=T, lw=2.4)
    _arrow_r(f, 376, 436, 403)
    f.text(462, 412, "FI", size=T)
    f.line((333, 424), (333, 464), w=2.4)
    f.text(316, 494, "Osc HF", size=T, anchor="c")
    _crich(f, 370, 534, [("Taux de Modulation", BU)], maxw=280)
    _crich(f, 370, 567, [("et surmodulation", BU)], maxw=280)
    # SSB / CW demodulator
    _crich(f, 800, 64, [("Oscillateur de battement de fréquence (", N), ("BFO", BU), (")", N)], maxw=560)
    _crich(f, 800, 97, [("et détecteur de produit", BU), (" (DP) ou mélangeur", N)], maxw=560)
    f.text(620, 152, "FI", size=T)
    f.line((669, 142), (732, 142), w=2.4)
    _box_label(f, 732, 122, 881, 163, "DP ou Mél", size=T, lw=2.4)
    _arrow_r(f, 881, 921, 142, filled=True)
    f.text(949, 152, "BF", size=T)
    f.line((800, 163), (800, 182), w=2.4)
    f.ellipse(797, 206, 40, 24, lw=2.4)
    f.text(797, 216, "BFO", size=T, anchor="c")
    _crich(f, 800, 265, [("Fréquence BFO ≈ Fréquence FI", N)], maxw=560)
    # SSB modulator
    _crich(f, 665, 316, [("Mélangeur équilibré", BU)], maxw=290)
    _crich(f, 665, 349, [("et ", N), ("filtre à quartz", BU), (" (Q)", N)], maxw=290)
    f.text(519, 412, "BF", size=T)
    f.line((554, 403), (579, 403), w=2.4)
    _box_label(f, 579, 383, 686, 424, "Mél éq", size=T, lw=2.4)
    f.line((686, 403), (728, 403), (728, 424), w=2.4)
    _box_label(f, 707, 424, 749, 465, "Q", size=T, lw=2.4)
    f.line((728, 465), (728, 485), w=2.4)
    _arrow_r(f, 728, 767, 485)
    f.text(773, 494, "FI", size=T)
    f.line((621, 424), (621, 464), w=2.4)
    f.text(625, 494, "Osc HF", size=T, anchor="c")
    # CW modulator
    for y, t in ((302, "Coupure de l’alimen-"), (334, "tation d’un étage ou"), (366, "entre les étages")):
        _crich(f, 949, y, [(t, N)], maxw=262)
    f.text(830, 401, "+", size=24)
    f.line((866, 405.5), (912, 405.5), (948, 389), w=2.4)
    f.line((952, 406), (972, 406), (972, 446), w=2.4)
    _box_label(f, 887, 446, 1058, 487, "Osc ou PA", size=T, lw=2.4)
    _crich(f, 949, 534, [("Piaulements et", BU)], maxw=262)
    _crich(f, 949, 567, [("claquements", BU)], maxw=262)
    # FM
    _crich(f, 1224, 64, [("Discriminateur", BU), (" ou", N)], maxw=272)
    _crich(f, 1224, 97, [("détecteur de pente", N)], maxw=272)
    f.text(1123, 150, "FI", size=T)
    f.line((1145, 142), (1186, 142), w=2.4)
    _box_label(f, 1186, 122, 1250, 163, "Disc", size=T, lw=2.4)
    _arrow_r(f, 1250, 1289, 142, filled=True)
    f.text(1295, 152, "BF", size=T)
    for y, t in ((200, "Foster-Seeley ;"), (232, "Squelch ; limiteur et"), (265, "désaccentuateur")):
        _crich(f, 1224, y, [(t, BU)], maxw=268)
    for y, t in ((302, "La BF est appliquée à"), (334, "un VCO (oscillateur à"), (366, "réactance)")):
        _crich(f, 1224, y, [(t, N)], maxw=268)
    f.text(1100, 437, "BF", size=T)
    f.line((1135, 428), (1160, 428), w=2.4)
    f.circle(1202, 428, 42, lw=2.4)
    f.text(1202, 438, "VCO", size=T, anchor="c")
    _arrow_r(f, 1244, 1284, 428, filled=True)
    f.text(1290, 437, "FI", size=T)
    f.text(1120, 494, "δU", size=T)
    f.text(1270, 494, "δF", size=T)
    _crich(f, 1224, 534, [("Indice de Modulation", BU)], maxw=272)
    _crich(f, 1224, 567, [("Préaccentuateur", BU)], maxw=272)


@figure("c093_2#0")
def detection_am(f):
    w = 2.2
    f.line((50, 76), (86, 76), w=w)
    f.poly([(86, 62), (112, 76), (86, 90)], stroke=None, fill=BLACK)
    f.line((115.5, 54), (115.5, 97), w=w)
    f.line((115, 76), (223, 76), (223, 131), w=w)
    f.line((158, 76), (158, 143), w=w)
    f.line((137, 143), (180, 143), w=2.6)
    f.line((137, 165), (180, 165), w=2.6)
    f.line((158, 165), (158, 226), w=w)
    gnd(f, 136, 226, 180, 237)
    f.rect(200.5, 131.5, 43, 66.5, lw=2.2)
    f.line((223, 198), (223, 226), w=w)
    gnd(f, 202, 226, 245, 237)
    f.line((307, 165), (248, 165), w=w)
    f.line((265, 155), (248, 165), (265, 176), w=w)
    f.fit(70, 141, 45, "Diode")
    f.fit(11, 37, 89, "FI", color=RED)
    f.text(97, 162, "C", size=27)
    f.text(205, 162, "R", size=27)
    f.fit(315, 348, 173, "BF", color=RED)
    upper = [(345, 66), (400, 38), (440, 22), (500, 11), (560, 16), (620, 42), (660, 62), (700, 75), (760, 49),
             (810, 18), (840, 11), (880, 29), (920, 55), (950, 72), (980, 72), (1010, 50), (1050, 15), (1075, 10),
             (1110, 20), (1150, 45), (1200, 68), (1250, 79), (1290, 62), (1320, 40), (1342, 28)]
    f.spline(upper, stroke="#6060ff", w=1.6, dash=[1.6, 2], cap="b")

    def up(x):
        for (x0, y0), (x1, y1) in zip(upper, upper[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return upper[-1][1]
    lower = [(x, 105 + (105 - y) * 0.75) for x, y in upper if x <= 705]
    f.spline(lower, stroke="#6060ff", w=1.6, dash=[1.6, 2], cap="b")
    per = 44.0

    def carrier(x):
        s = math.sin(2 * math.pi * (x - 358) / per)
        if x > 702:
            s = max(0.0, s)
        return 105 - (105 - up(x)) * s
    f.curve(carrier, 345, 965, n=900, stroke=RED, w=2)
    f.line((336, 104.5), (1318, 104.5), w=2.2)
    f.line((1300, 96), (1318, 104.5), (1300, 113), w=2.2)
    f.text(1333, 111, "T", size=27)
    f.line((575, 17), (512, 12.5), stroke=BLUE, w=2)
    _arrow_tip(f, 575, 17, 500, 12, BLUE, size=14, filled=True)
    f.line((628, 48), (586, 160), stroke=BLUE, w=2)
    _arrow_tip(f, 628, 48, 581, 173, BLUE, size=14, filled=True)
    f.fit(588, 760, 28, "Enveloppe BF")
    f.fit(1083, 1193, 130, "Effet RC")
    f.fit(937, 1342, 166, "Fréq FI > R(Ω) x C(F) > Fréq BF")
    f.fit(370, 650, 210, "AM à la sortie de la FI")
    f.fit(754, 871, 210, "Détection")
    f.fit(1083, 1193, 210, "Filtre BF")


@figure("c093_3#0")
def detection_cag(f):
    w = 2.4
    T = 29
    # first IF amplifier (dual-gate MOSFET)
    f.circle(168.5, 150, 77, lw=3.2)
    f.line((70, 120), (136, 120), w=w)
    f.line((136, 100), (136, 140), w=w)
    f.line((91, 297), (91, 185), (136, 185), w=w)
    f.line((136, 165), (136, 205), w=w)
    f.rect(152, 98, 11, 107, stroke=None, fill=BLACK)
    f.line((163, 119), (201.5, 119), (201.5, 55), (276, 55), w=w)
    f.line((262, 47), (278, 55), (262, 63), w=w)
    f.line((175, 165), (201.5, 165), (201.5, 260), w=w)
    f.poly([(178, 157), (164, 165), (178, 173)], stroke=None, fill=BLACK)
    f.line((163, 185), (201.5, 185), w=w)
    gnd(f, 175, 260, 229, 271)
    f.fit(9, 54, 129, "Mél", color=RED)
    f.fit(315, 341, 58, "FI", color=RED)
    f.fit(260, 356, 136, "Premier")
    f.fit(261, 362, 172, "ampli FI")
    # detection
    f.line((381, 55), (423, 55), w=w)
    f.poly([(423, 40), (452, 55.5), (423, 71)], stroke=None, fill=BLACK)
    f.line((453.5, 39), (453.5, 72), w=w)
    f.line((453, 55.5), (759, 55.5), w=w)
    f.line((518.5, 55), (518.5, 95), w=w)
    f.line((497, 95.5), (541, 95.5), w=2.6)
    f.line((497, 116), (541, 116), w=2.6)
    f.line((518.5, 116), (518.5, 176), w=w)
    gnd(f, 497, 176, 541, 187)
    f.line((606, 55), (606, 72), w=w)
    f.rect(583.5, 72.5, 45, 85.5, lw=2.4)
    f.line((606, 158), (606, 176), w=w)
    gnd(f, 585, 176, 629, 187)
    f.line((694, 116), (632, 116), w=w)
    f.line((650, 106), (632, 116), (650, 126), w=w)
    f.fit(698, 732, 133, "BF", color=RED)
    f.text(632, 157, "Niveau", size=T)
    f.text(632, 193, "BF", size=T)
    f.fit(520, 638, 26, "Détection", color=RED)
    # AGC
    f.rect(759.5, 27.5, 89.5, 43.5, lw=2.4)
    f.text(804, 59, "R", size=T, anchor="c")
    f.line((849, 55.5), (874, 55.5), w=w)
    f.poly([(874, 40), (903, 55.5), (874, 71)], stroke=None, fill=BLACK)
    f.line((904.5, 39), (904.5, 72), w=w)
    f.line((904, 55.5), (1046, 55.5), (1046, 72), w=w)
    f.line((958, 55), (958, 95), w=w)
    f.line((936, 95.5), (980, 95.5), w=2.6)
    f.line((914, 95), (914, 116), (1002, 116), (1002, 95), w=2.4)
    f.line((958, 116), (958, 176), w=w)
    gnd(f, 936, 176, 980, 187)
    f.rect(1022.5, 72.5, 45.5, 85.5, lw=2.4)
    f.line((1046, 158), (1046, 176), w=w)
    gnd(f, 1024, 176, 1068, 187)
    f.line((1172, 116), (1072, 116), w=w)
    f.line((1090, 106), (1072, 116), (1090, 126), w=w)
    f.fit(1074, 1110, 157, "RF")
    f.fit(1071, 1129, 193, "Gain")
    f.fit(981, 1043, 26, "CAG", color=RED)
    f.circle(1200, 115, 45, lw=3.2)
    f.rect(1172, 95, 11, 42, stroke=None, fill=BLACK)
    f.line((1183, 107), (1221.5, 74), (1221.5, 29.5), (1286, 29.5), w=w)
    f.line((1183, 125), (1240, 160), (1244, 165), (1244, 213), w=w)
    _arrow_tip(f, 1183, 125, 1229, 154, BLACK, size=16, filled=True)
    gnd(f, 1218, 213, 1262, 224)
    f.rect(1287, 7.5, 67, 43, lw=2.4)
    f.line((1354, 29.5), (1375, 29.5), w=w)
    f.text(1386, 40, "+", size=26, anchor="c")
    f.line((1272.5, 29.5), (1272.5, 297), w=w)
    f.line((91, 297), (1286, 297), w=w)
    f.circle(1309, 290, 23, lw=3)
    f.line((1332, 297), (1349, 297), w=w)
    f.rect(1349, 271, 11, 41, stroke=None, fill=BLACK)
    f.fit(1277, 1370, 263, "S-mètre")
    for x in (405, 751):
        f.line((x, 0), (x, 334), stroke=RED, w=2, dash=[1.6, 2], cap="b")


def _npn(f, cx, cy, r, bar, base_x0, base_y, c_end, e_mid, e_end):
    f.circle(cx, cy, r, lw=3.2)
    gnd(f, *bar)
    f.line((base_x0, base_y), (bar[0], base_y), w=2.4)
    f.line((bar[2], cy - 9), c_end, w=2.4)
    f.line((bar[2], cy + 9), e_mid, e_end, w=2.4)
    a = math.atan2(e_mid[1] - cy - 9, e_mid[0] - bar[2])
    tip = (bar[2] + (e_mid[0] - bar[2]) * 0.62, cy + 9 + (e_mid[1] - cy - 9) * 0.62)
    _arrow_tip(f, bar[2], cy + 9, tip[0], tip[1], BLACK, size=17, filled=True)


@figure("c094_1#0")
def modulateurs_am(f):
    w = 2.4
    it = dict(italic=True, color=RED)
    # collector modulation
    _npn(f, 117, 153, 45, (89, 134, 100, 175), 8, 155.5, (138, 112), (161, 201), (161, 250))
    f.line((138, 112), (138, 46.5), (160, 46.5), w=w)
    gnd(f, 135, 250, 178, 261)
    _humps(f, 160, 248, 46.5, 4, 22, w=w)
    f.line((248, 46.5), (248, 172), w=w)
    _humps(f, 269, 357, 46.5, 4, 22, w=w)
    f.line((269, 46.5), (269, 172), w=w)
    f.line((269, 112), (291.5, 112), w=w)
    f.line((291.5, 91), (291.5, 132), w=w)
    f.line((312.5, 91), (312.5, 132), w=w)
    f.line((313, 112), (351, 112), w=w)
    gnd(f, 351, 91, 362, 132)
    f.text(244, 205, "+", size=22, anchor="c")
    f.text(270, 205, "+", size=22, anchor="c")
    f.line((357, 47), (575, 47), w=w)
    f.text(5, 143, "BF", size=30, **it)
    # second stage
    f.line((575, 25), (575, 66), w=w)
    f.line((596, 25), (596, 66), w=w)
    gnd(f, 612, 25, 623, 66)
    _npn(f, 527, 153, 45, (503, 134, 514, 175), 444, 155.5, (552, 111), (571, 201), (571, 250))
    f.line((552, 111), (552, 47), w=w)
    gnd(f, 544, 250, 587, 261)
    f.line((552, 90), (640.5, 90), w=w)
    f.line((640.5, 68), (640.5, 109), w=w)
    f.line((662, 68), (662, 109), w=w)
    f.line((662, 90), (684, 90), (684, 134), w=w)
    vcoil(f, 684, 134, 198, 3, 15, side=1, w=w)
    f.line((684, 198), (684, 236), w=w)
    gnd(f, 662, 236, 706, 247)
    vcoil(f, 749, 134, 198, 3, 15, side=-1, w=w)
    f.line((749, 134), (749, 90), (785, 90), w=w)
    f.line((771, 80), (787, 90), (771, 100), w=w)
    f.line((749, 198), (749, 236), w=w)
    gnd(f, 727, 236, 771, 247)
    f.text(415, 143, "HF", size=30, **it)
    f.text(799, 97, "AM", size=30, **it)
    # dual-gate MOSFET modulator
    f.circle(1127.5, 104, 77, lw=3.2)
    f.line((1031, 73), (1096, 73), w=w)
    f.line((1096, 52), (1096, 94), w=w)
    f.line((1031, 138.5), (1096, 138.5), w=w)
    f.line((1096, 118), (1096, 159), w=w)
    f.rect(1112, 52, 11, 104, stroke=None, fill=BLACK)
    f.line((1123, 73), (1161.5, 73), (1161.5, 8), (1227, 8), (1227, 51), w=w)
    vcoil(f, 1227, 51, 117, 3, 16, side=1, w=w)
    f.line((1227, 117), (1227, 222), w=w)
    f.line((1227, 182), (1271, 182), w=w)
    f.line((1271, 161), (1271, 202), w=w)
    f.line((1292, 161), (1292, 202), w=w)
    f.line((1292, 182), (1309, 182), w=w)
    gnd(f, 1309, 161, 1320, 202)
    f.text(1232, 250, "+", size=22, anchor="c")
    f.line((1135, 117), (1161.5, 117), (1161.5, 242), w=w)
    f.poly([(1137, 105), (1123, 117), (1137, 129)], stroke=None, fill=BLACK)
    f.line((1123, 138.5), (1161.5, 138.5), w=w)
    gnd(f, 1140, 242, 1184, 253)
    gnd(f, 1047, 204, 1058, 245)
    f.line((1058, 225), (1073.5, 225), w=w)
    f.line((1073.5, 204), (1073.5, 245), w=w)
    f.line((1096, 204), (1096, 245), w=w)
    f.line((1096, 225), (1161.5, 225), w=w)
    vcoil(f, 1292, 51, 117, 3, 16, side=-1, w=w)
    f.line((1292, 51), (1292, 8), (1337, 8), w=w)
    f.line((1323, 0), (1339, 8), (1323, 16), w=w)
    f.line((1292, 117), (1292, 133), w=w)
    gnd(f, 1271, 133, 1314, 144)
    f.text(969, 82, "BF", size=30, **it)
    f.text(969, 147, "HF", size=30, **it)
    f.text(1348, 27, "AM", size=30, **it)


_AM_RED = [(36, 283.4), (40, 269.7), (54, 184.4), (59, 168.3), (62, 163.7), (67, 174.7), (82, 290.1), (86, 303.9), (89, 306.8), (93, 296.5), (110, 187.2), (115, 166.3), (118, 161.6), (121, 164.8), (125, 182.3), (137, 272.3), (142, 298.3), (146, 307), (148, 305), (150, 298), (164, 191.3), (169, 169.7), (171, 166.3), (175, 172), (191, 263.7), (198, 285.3), (201, 284), (204, 276.1), (221, 187.8), (224, 180.3), (226, 179.9), (228, 182.4), (233, 203.3), (245, 281.7), (250, 299.2), (252, 301.3), (256, 294.7), (270, 194.2), (276, 161), (280, 152.5), (283, 160.2), (297, 291.2), (302, 322.2), (304, 327.7), (306, 327.8), (310, 313.8), (324, 179.8), (329, 144.3), (332, 136.2), (338, 138.8), (344, 180.2), (351, 259), (356, 300.9), (360, 319.7), (362, 320.8), (366, 309.4), (383, 186.2), (387, 171), (389, 169.8), (393, 180.3), (405, 261.7), (412, 289.8), (415, 289.7), (418, 283.5), (432, 209.3), (436, 198.4), (448, 198.4), (452, 209.7), (459, 255.3), (466, 283.2), (469, 285.9), (472, 280.7), (479, 246.2), (486, 194.8), (491, 169.8), (495, 161.8), (498, 166.4), (501, 182.1), (513, 285.8), (520, 324.9), (523, 328.6), (528, 305.9), (545, 143.6), (547, 132.3), (549, 127.5), (551, 126.5), (558, 162.5), (572, 308.1), (574, 320.2), (578, 327.7), (580, 323.7), (585, 300.3), (599, 180), (601, 170), (605, 161.9), (607, 164.6), (612, 182.7), (623, 256.2), (630, 284.5), (632, 285.5), (634, 283.2), (639, 268.7), (653, 195.4), (655, 189.3), (658, 186.5), (661, 190), (666, 205.3), (680, 276.9), (683, 284.1), (686, 285.3), (693, 265.2), (707, 189.2), (709, 182.8), (712, 179.6), (715, 184.6), (720, 206.5), (732, 287.4), (734, 295.1), (737, 299.7), (740, 295.1), (742, 287.4), (759, 172.5), (762, 158), (765, 152.2), (767, 153.4), (769, 160.2), (774, 191.2), (786, 309.6), (790, 334.8), (793, 338.1), (796, 329.6), (801, 294), (815, 135.8), (821, 107.1), (825, 117.6), (827, 132.1), (841, 327.6), (847, 364.4), (850, 356.4), (854, 327.4), (869, 124.7), (873, 103.1), (875, 100.5), (880, 123.5), (896, 339), (900, 361.8), (902, 364.5), (907, 340.3), (923, 127.2), (927, 104.5), (929, 100.4), (933, 114.2), (936, 137.3), (950, 307.5), (954, 332.6), (957, 339.8), (960, 336.8), (963, 325.4), (977, 226), (984, 204.2), (987, 201.6), (990, 203.9), (1004, 230), (1011, 237.5), (1014, 237.2), (1031, 215.2), (1036, 215.7), (1042, 228.3), (1056, 279.7), (1059, 285.1), (1062, 286.1), (1064, 283.8), (1069, 268), (1083, 173.7), (1088, 154.6), (1090, 152.3), (1094, 159.7), (1110, 291.3), (1117, 319.4), (1120, 317.1), (1123, 303.7), (1137, 185.2), (1142, 158.5), (1145, 153.2), (1148, 157.7), (1158, 221.3), (1164, 279.8), (1171, 311.8), (1174, 311), (1177, 302.7), (1191, 209), (1196, 185.5), (1199, 179), (1202, 179.2), (1206, 188.3), (1218, 238.5), (1225, 258.5), (1233, 258.5), (1245, 238.5), (1249, 234.4), (1258, 230.7), (1270, 228), (1296, 228), (1302, 229.7), (1306, 232.1), (1312, 239.6), (1319, 256.7), (1326, 280.8), (1332, 290.3), (1337, 284.3), (1339, 277.4), (1356, 173.4), (1359, 162.4), (1362, 158.5), (1366, 163.8), (1373, 188.5), (1393, 305.6)]
_AM_UP = [(36, 153.5), (72, 151.5), (149, 152.8), (166, 159.2), (168, 163.3), (176, 166.7), (181, 172.3), (193, 174), (205, 172.1), (248, 157.5), (267, 148.7), (269, 145.8), (279, 144), (306, 125.2), (320, 120), (324, 120), (326, 124.5), (345, 129.1), (349, 135.3), (356, 130.6), (359, 118.3), (364, 115.9), (372, 131.9), (373, 142.6), (412, 157.3), (414, 171.5), (420, 174.8), (450, 176.5), (473, 168.7), (479, 162.3), (486, 159.7), (492, 151.6), (498, 148.9), (503, 140.4), (509, 137.7), (515, 131.2), (522, 128.8), (528, 123), (542, 120), (552, 121.8), (565, 128.2), (582, 145.4), (590, 148.7), (594, 155.8), (601, 158.2), (603, 163.5), (613, 166.5), (621, 173.2), (634, 177.5), (639, 162.9), (680, 175.2), (681, 178.1), (691, 177.2), (721, 167.2), (726, 161.4), (745, 150.8), (751, 142.6), (759, 140.1), (776, 124.6), (784, 121.9), (789, 115), (797, 112.3), (803, 104.4), (820, 92.6), (826, 84.2), (833, 81.8), (839, 75.2), (847, 72.8), (853, 67.7), (866, 66), (890, 71.2), (893, 73.3), (895, 79.9), (917, 85.5), (922, 99.7), (939, 106.8), (941, 114.2), (950, 122.5), (961, 147.7), (965, 152.3), (981, 202.8), (995, 224.8), (1000, 226.9), (1009, 226.3), (1020, 218.7), (1026, 210.2), (1031, 207.2), (1035, 198.4), (1040, 195), (1055, 172.3), (1061, 168.6), (1064, 160.7), (1070, 157.9), (1076, 150), (1083, 148.5), (1089, 143.2), (1119, 138), (1135, 139.9), (1164, 147), (1185, 160.6), (1190, 170.2), (1196, 175.2), (1197, 180.7), (1209, 186.8), (1211, 195), (1216, 198.3), (1220, 206.5), (1236, 223.5), (1242, 237.1), (1258, 251.1), (1262, 264.7), (1266, 268), (1274, 260.2), (1276, 251.1), (1281, 248.7), (1290, 235.5), (1306, 203.1), (1313, 193.8), (1316, 184), (1322, 180.1), (1325, 172.2), (1333, 169.4), (1339, 161.4), (1353, 154.5), (1380, 147)]
_AM_LOW4 = [(990, 255), (992, 246), (1013, 239), (1015, 234.5), (1022, 236.5), (1028, 243.9), (1034, 247.1), (1037, 255.3), (1044, 259.5), (1048, 284.9), (1133, 303.6), (1134, 315.6), (1144, 321.2), (1176, 312.8), (1179, 307.4), (1187, 304.6), (1193, 295.8), (1198, 293.3), (1202, 285.3), (1207, 282.3), (1213, 272.1), (1218, 269.2), (1222, 261.7), (1228, 258.2), (1233, 247.8), (1239, 244.2), (1242, 238.5), (1254, 246.2), (1258, 251.1), (1263, 266.6), (1266, 268), (1274, 260.2), (1276, 251.1), (1281, 248.7), (1293, 231.7), (1302, 233.9), (1317, 263.2), (1319, 280.8), (1379, 296.2), (1382, 311.5)]


@figure("c094_2#0")
def zones_am(f):
    grey = "#7f7f7f"
    f.line((36, 93), (1335, 93), stroke=grey, w=2.2)
    f.line((36, 363.5), (1335, 363.5), stroke=grey, w=2.2)
    up = _AM_UP
    low = [(x, 459 - y) for x, y in up if x < 990] + _AM_LOW4
    bd = dict(stroke="#3030ff", w=2, dash=[5, 4], cap="b")
    f.line(up, **bd)
    f.line(low, **bd)
    f.line(_AM_RED, stroke=RED, w=2)
    f.line((36, 224), (1380, 224), w=2.4)
    f.poly([(1372, 217), (1388, 224), (1372, 231)], stroke=None, fill=BLACK)
    f.text(1393, 232, "T", size=27)
    f.text(6, 215, "0", size=27)
    for x0, x1 in ((39, 171), (174, 685), (688, 1036), (1039, 1360)):
        _hdarrow(f, x0, x1, 18.5, s=10, w=1.6)
    for x0, t in ((59, "Zone 1"), (372, "Zone 2"), (734, "Zone 3"), (1142, "Zone 4")):
        f.fit(x0, x0 + 87, 54, t)
    def up_arrow(x, y0, y1, both=False):
        f.line((x, y0 - (12 if both else 0)), (x, y1 + 12), w=2.6)
        f.poly([(x - 7, y1 + 16), (x, y1), (x + 7, y1 + 16)], stroke=None, fill=BLACK)
        if both:
            f.poly([(x - 7, y0 - 16), (x, y0), (x + 7, y0 - 16)], stroke=None, fill=BLACK)
    up_arrow(90.5, 227, 96)
    up_arrow(143.5, 225, 154)
    up_arrow(335, 225, 120)
    up_arrow(442, 225, 175)
    up_arrow(442, 173, 120, both=True)
    up_arrow(901.5, 225, 71, both=True)
    up_arrow(1278.5, 248, 138, both=True)
    T = 28
    f.text(59, 131, "B", size=T)
    f.text(122, 131, "B/2", size=T)
    f.text(348, 131, "A", size=T)
    f.text(468, 150, "b", size=T)
    f.text(468, 210, "a", size=T)
    f.text(872, 157, "b", size=T)
    f.text(1250, 162, "b", size=T)
    for x0, y0, x1, y1 in ((390, 458, 438, 295), (390, 458, 581, 156), (600, 436, 645, 96), (598, 436, 587, 369),
                           (806, 393, 815, 369), (1228, 362, 1262, 258)):
        f.line((x0, y0), (x1, y1), stroke=BLUE, w=2)
        _arrow_tip(f, x0, y0, x1, y1, BLUE, size=15, filled=True)
    for x0, x1, y, t in ((52, 155, 401, "Porteuse"), (46, 163, 435, "AM sans"), (47, 164, 469, "signal BF"),
                         (259, 366, 418, "K = 40%"), (200, 375, 482, "Enveloppe BF"),
                         (462, 728, 459, "Tension maximum de"), (477, 718, 493, "sortie de l’ampli RF"),
                         (715, 928, 423, "K>100% car b>B"), (953, 1390, 391, 'Distorsion à cause de BF "négative"'),
                         (1004, 1340, 423, "sans toutefois que K>100%"),
                         (763, 1367, 478, "Taux de modulation impossible à calculer avec A"),
                         (797, 1329, 511, "et a car l’enveloppe BF n’est pas « centrée »")):
        f.fit(x0, x1, y, t, max_size=30)


_PM = [(22, 214.3), (30, 192.7), (34, 187.6), (36, 189.6), (38, 195), (49, 239.2), (51, 243.4), (53, 244.3), (56, 239.5), (61, 223.9), (68, 194), (71, 187.3), (73, 186.7), (76, 192.9), (80, 208.2), (86, 238.9), (88, 244.4), (90, 245.5), (96, 226.1), (102, 192.9), (104, 188.1), (106, 187.2), (110, 195.8), (121, 237.4), (124, 244.2), (127, 246.1), (133, 237.3), (148, 193.8), (151, 188.2), (154, 186.6), (158, 194.2), (163, 212.8), (167, 234.4), (171, 243.8), (173, 242.3), (179, 221.8), (184, 193.9), (186, 187.5), (188, 185.8), (190, 189.9), (194, 207.8), (199, 239.3), (201, 244.8), (203, 245.8), (206, 240), (218, 193.8), (221, 186.1), (223, 183.9), (226, 187.2), (229, 196.1), (239, 238.4), (241, 242.9), (243, 243.8), (249, 226.7), (256, 191.8), (259, 186.6), (264, 204.7), (269, 238.1), (272, 244.6), (277, 228.6), (282, 198.5), (285, 188.7), (287, 191.6), (290, 205.8), (294, 237.8), (296, 243.7), (298, 240.1), (308, 191.3), (310, 186), (312, 184.3), (314, 186.4), (317, 194.2), (328, 235.6), (331, 242.4), (333, 243.5), (339, 225.9), (345, 191.2), (347, 185.6), (349, 184.4), (353, 192.8), (365, 239.9), (368, 246.6), (370, 247.8), (372, 245.4), (375, 236.6), (384, 196.9), (388, 186.1), (389, 185.8), (391, 189.4), (400, 237.2), (402, 243.3), (404, 244.8), (407, 239.8), (413, 220.9), (420, 192.3), (423, 185.9), (425, 184.3), (429, 189.4), (437, 214.6), (441, 231.6), (444, 239.2), (447, 242.9), (449, 242.5), (452, 238.3), (466, 198.9), (470, 190.1), (473, 187), (476, 188.3), (480, 195.6), (487, 214.6), (493, 235.7), (498, 244.1), (500, 242.8), (507, 221), (511, 198.3), (515, 188.4), (517, 189.9), (520, 198.1), (528, 233.4), (532, 244.2), (534, 244.4), (537, 238.2), (542, 221.2), (547, 195.7), (550, 188.2), (552, 189), (554, 195.4), (561, 238.2), (564, 245.3), (566, 243.9), (573, 228.8)]
_FM = [(22, 304.7), (30, 278.8), (33, 274.8), (37, 283.1), (47, 328.4), (50, 335.6), (52, 336.3), (57, 323.4), (67, 281.2), (71, 274.3), (73, 276.2), (76, 284.7), (86, 328.4), (88, 333.5), (90, 334.4), (94, 321.7), (101, 281.8), (103, 275.7), (105, 273.8), (109, 280.9), (121, 326.4), (126, 337), (129, 334.1), (131, 328.1), (139, 283.2), (141, 276.4), (143, 273.9), (147, 281.1), (160, 333.6), (162, 335.6), (165, 326.3), (171, 283.9), (174, 276.7), (178, 290.4), (184, 325.3), (187, 334.2), (188, 334.1), (190, 328), (196, 285.5), (199, 276.2), (202, 281.6), (214, 332.7), (216, 335.2), (220, 322.9), (226, 285.1), (228, 278.1), (230, 276.4), (234, 285.9), (243, 324.6), (247, 333.7), (249, 332.2), (251, 325.8), (258, 285.4), (260, 278.1), (262, 275.9), (266, 287.1), (274, 325.6), (278, 334.3), (281, 332.8), (284, 326.8), (297, 285), (300, 278.1), (303, 274.5), (306, 276.1), (309, 281.3), (323, 326.7), (326, 332.8), (328, 334.3), (331, 331.4), (334, 323.7), (345, 282.8), (348, 277), (350, 275.6), (353, 278.1), (356, 283.4), (371, 325.1), (375, 333.4), (378, 336.4), (380, 335.2), (383, 328.9), (393, 286.4), (396, 278.1), (398, 276), (400, 277.4), (403, 283.8), (414, 323.5), (417, 331.3), (420, 334.9), (422, 334.2), (425, 329.2), (438, 286.7), (441, 279.3), (444, 276.1), (446, 277.6), (449, 284.7), (458, 323.6), (461, 332.7), (463, 334.4), (465, 333.2), (467, 326.9), (475, 284.2), (479, 273.6), (481, 276.3), (483, 283.4), (491, 326.9), (494, 333.3), (497, 323.9), (503, 284.4), (506, 274.9), (508, 276.4), (510, 282.9), (518, 323.4), (522, 335), (524, 333.6), (526, 326.7), (533, 284.3), (536, 275.8), (539, 284.7), (547, 331.7), (549, 327.8), (555, 286.9), (558, 275.6), (559, 275.4), (561, 279.7), (568, 304.9)]
_MODBF = [(15, 47.5), (91, 48.5), (118, 46.3), (132, 41.6), (146, 25.7), (155, 20.7), (185, 17.5), (222, 18.6), (249, 23.1), (258, 26.1), (264, 29.5), (274, 40.4), (291, 67.3), (299, 74.8), (305, 78.1), (316, 81.5), (340, 85.4), (391, 86.5), (420, 82.9), (433, 78.9), (440, 74.8), (449, 63.8), (465, 29.4), (470, 23.3), (477, 19.2), (486, 16.7), (505, 15.5), (561, 20.5)]


@figure("c094_3#0")
def pm_fm(f):
    green = "#00a050"
    for x in (70.5, 195.5, 379.5, 522.5):
        f.line((x, 20), (x, 310), stroke="#808080", w=1.2, dash=[1.4, 2], cap="b")
    for x in (130, 279, 460):
        f.line((x, 0), (x, 343), stroke=RED, w=1.4, dash=[5, 4], cap="b")
    f.spline(_MODBF, stroke="#0000ff", w=2.4, n=6)
    f.curve(lambda x: 134.5 - 31 * math.cos(2 * math.pi * (x - 33) / 36.2), 18, 576, n=600, stroke=RED, w=2.2)
    f.line(_PM, stroke=green, w=2.2)
    f.line(_FM, stroke=green, w=2.2)
    for y, x0 in ((50, 15), (134.5, 17), (217.5, 17), (308, 15)):
        f.line((x0, y), (580, y), w=2.4)
        f.poly([(574, y - 8), (592, y), (574, y + 8)], stroke=None, fill=BLACK)
    f.circle(17, 134.5, 2.5, stroke=None, fill="#808080")
    f.fit(613, 806, 50, "Modulation BF")
    f.fit(614, 781, 130, "Porteuse (HF")
    f.fit(614, 788, 166, "non modulée)")
    f.text(614, 225, "PM", size=30)
    f.text(614, 312, "FM", size=30)


@figure("c095_1#0")
def demod_pll(f):
    T = 30
    it = dict(italic=True)
    w = 2.4
    f.rect(108.5, 6.5, 201, 50, lw=2.6)
    f.text(209, 40, "comparateur", size=T, anchor="c", **it)
    f.rect(354.5, 6.5, 121, 50, lw=2.6)
    f.text(415, 40, "filtre", size=T, anchor="c", **it)
    f.rect(181.5, 74.5, 168, 50, lw=2.6)
    f.text(265, 110, "VCO", size=T, anchor="c", **it)
    f.line((63, 18), (106, 18), w=w)
    f.line((93, 10), (107, 18), (93, 26), w=w)
    f.line((61, 48), (106, 48), w=w)
    f.line((93, 40), (107, 48), (93, 56), w=w)
    f.line((61, 48), (61, 104), (181, 104), w=w)
    f.line((310, 29), (351, 29), w=w)
    f.line((337, 21), (351, 29), (337, 37), w=w)
    f.line((397, 57), (397, 104), w=w)
    f.line((352, 104), (442, 104), w=w)
    f.line((366, 96), (352, 104), (366, 112), w=w)
    f.line((428, 96), (442, 104), (428, 112), w=w)
    f.text(4, 34, "FM", size=T, color=RED, **it)
    f.text(442, 120, "BF", size=T, color=RED, **it)


@figure("c095_2#0")
def spectre_fm(f):
    for x in (49.5, 178):
        f.line((x, 64), (x, 300), stroke="#3030ff", w=1.6, dash=[1.6, 1.8], cap="b")
    f.rect(110, 23, 6, 107, stroke=None, fill=RED)
    f.line((7, 130.5), (236, 130.5), w=2.6)
    f.poly([(228, 124), (242, 130.5), (228, 137)], stroke=None, fill=BLACK)
    f.text(247, 140, "f", size=27)
    _hdarrow(f, 52, 177, 87, s=12, w=2.4, color="#3030ff")
    _hdarrow(f, 116, 177, 44, s=8, w=1.4)
    f.fit(128, 250, 32, "Excursion")
    f.text(55, 74, "δF", size=26)
    f.text(108, 155, "Fo", size=26)
    f.line((113, 160), (113, 280), w=1.4, dash=[1.6, 1.6], cap="b")
    f.poly([(108, 276), (113, 287), (118, 276)], stroke=None, fill=BLACK)
    f.spline([(115, 161), (183, 175), (70, 205), (135, 220), (48, 233), (183, 250), (115, 263)], w=1.4, n=10)
    f.text(165, 203, "BF", size=24, rot=90, anchor="c", va="middle")
    f.text(135, 285, "T", size=22, rot=90, anchor="c", va="middle")


@figure("c095_2#1")
def modulateurs_fm(f):
    w = 2.4
    T = 30
    it = dict(italic=True)
    redi = dict(italic=True, color=RED)
    navi = dict(italic=True, color=NAVY)

    def open_r(x0, x1, y):
        f.line((x0, y), (x1, y), w=w)
        f.line((x1 - 14, y - 8), (x1, y), (x1 - 14, y + 8), w=w)

    def open_l(x0, x1, y):
        f.line((x0, y), (x1, y), w=w)
        f.line((x1 + 14, y - 8), (x1, y), (x1 + 14, y + 8), w=w)
    # ---- Hartley oscillator with capacitive microphone
    f.circle(48, 185.5, 21.5, lw=2.4)
    gnd(f, 65, 164, 88, 207)
    f.line((88, 165), (120, 165), (120, 51), w=w)
    _humps(f, 120, 185, 51, 3, 16, w=w)
    f.line((185, 51), (185, 204), (88, 204), w=w)
    f.line((163.5, 36), (163.5, 14), (246, 14), (246, 92), w=w)
    f.line((246, 111), (246, 186), (290, 186), w=w)
    gnd(f, 75, 79, 85, 120)
    f.line((85, 100), (142, 100), w=w)
    f.line((142.5, 79), (142.5, 120), w=w)
    f.line((163, 79), (163, 120), w=w)
    f.line((163, 100), (287, 100), w=w)
    f.line((287.5, 79), (287.5, 120), w=w)
    f.line((308, 79), (308, 120), w=w)
    open_r(308, 380, 100)
    f.text(389, 98, "FM", size=T, **redi)
    f.circle(316, 181, 41, lw=3.2)
    gnd(f, 290, 163, 300, 203)
    f.line((300, 174), (336, 148), (336, 75), w=w)
    f.rect(323.5, 27.5, 30.5, 47.5, lw=2.4)
    f.line((336, 4), (336, 27), w=w)
    f.text(345, 18, "+", size=24, anchor="c")
    f.line((300, 193), (354, 239), (354, 288), w=w)
    _arrow_tip(f, 300, 193, 330, 218, BLACK, size=17, filled=True)
    gnd(f, 328, 288, 369, 299)
    f.fit(4, 143, 232, "Microphone", **redi)
    f.fit(4, 110, 266, "capacitif", **redi)
    f.fit(164, 292, 232, "Oscillateur", **navi)
    f.fit(164, 252, 266, "Hartley", **navi)
    # ---- Colpitts VXO with varicap
    f.fit(506, 832, 92, "VXO type Colpitts à Varicap", **navi)
    f.text(450, 133, "BF", size=T, **redi)
    f.line((473, 141.5), (509, 141.5), w=w)
    f.line((509, 120), (509, 160), w=w)
    f.line((530, 120), (530, 160), w=w)
    f.line((530, 142.5), (641, 142.5), w=w)
    f.line((641, 120), (641, 160), w=w)
    _box_label(f, 653.5, 118.5, 696, 161.5, "Q", size=28, lw=2.4)
    f.line((710.5, 121), (710.5, 162), w=w)
    f.line((711, 142.5), (821, 142.5), w=w)
    f.line((553.5, 142), (553.5, 183), w=w)
    f.rect(532.5, 183.5, 42, 63.5, lw=2.4)
    f.line((535, 245), (572, 186), w=1.8)
    _arrow_tip(f, 535, 245, 573, 185, BLACK, size=13, w=1.8)
    f.line((553.5, 247), (553.5, 286), w=w)
    gnd(f, 534, 286, 575, 297)
    f.line((615, 142), (615, 188.5), w=w)
    f.line((590, 189), (640, 189), w=2.6)
    f.line((590, 214.5), (640, 214.5), w=2.6)
    f.poly([(602, 243), (615, 216), (628, 243)], stroke=None, fill=BLACK)
    f.line((615, 243), (615, 287), w=w)
    gnd(f, 594, 287, 635, 298)
    for cx, cy, t, st in ((470, 215, "Niveau", it), (510, 205, "BF", it), (652, 222, "Varicap", redi)):
        f.text(cx, cy, t, size=T, rot=-90, anchor="c", va="middle", **st)
    f.line((739.5, 142), (739.5, 154.5), w=w)
    f.rect(723.5, 154.5, 34.5, 63.5, lw=2.4)
    f.line((740, 218), (740, 231), (889, 231), w=w)
    f.line((793, 142), (793, 182.5), w=w)
    f.line((773, 182.5), (813, 182.5), w=2.4)
    f.line((773, 198), (813, 198), w=2.4)
    f.line((793, 198), (793, 246), w=w)
    f.line((773, 246), (813, 246), w=2.4)
    f.line((773, 260.5), (813, 260.5), w=2.4)
    f.line((793, 261), (793, 288), w=w)
    gnd(f, 779, 288, 820, 299)
    f.circle(848, 141, 41, lw=3.2)
    gnd(f, 821, 123, 832, 163)
    f.line((832, 133), (867, 102), (910, 102), w=w)
    f.line((881, 102), (881, 80), w=w)
    f.rect(867.5, 35.5, 33, 44.5, lw=2.4)
    f.line((881, 16), (881, 36), w=w)
    f.text(890, 22, "+", size=24, anchor="c")
    f.line((909.5, 80), (909.5, 121), w=w)
    f.line((930.5, 80), (930.5, 121), w=w)
    open_r(931, 968, 101)
    f.text(931, 132, "FM", size=T, **redi)
    f.line((832, 151), (889, 207), (889, 288), w=w)
    _arrow_tip(f, 832, 151, 866, 185, BLACK, size=17, filled=True)
    gnd(f, 869, 288, 910, 299)
    # ---- PLL modulator
    f.rect(997.5, 30.5, 140.5, 42.5, lw=2.4)
    f.text(1067, 62, "VCO", size=T, anchor="c", **it)
    f.rect(1223.5, 30.5, 189, 86.5, lw=2.4)
    f.text(1318, 62, "Diviseur", size=T, anchor="c", **it)
    f.text(1318, 98, "programmable", size=T, anchor="c", **it)
    open_r(1138, 1221, 57.5)
    f.line((1156.5, 57), (1156.5, 12), w=w)
    f.line((1148.5, 26), (1156.5, 11), (1164.5, 26), w=w)
    f.text(1167, 33, "FM", size=T, **redi)
    f.rect(989.5, 137.5, 103.5, 121.5, lw=2.4)
    f.text(1041, 170, "Filtre", size=T, anchor="c", **it)
    f.text(1041, 205, "passe-", size=T, anchor="c", **it)
    f.text(1041, 237, "bas", size=T, anchor="c", **it)
    f.line((1043.5, 137), (1043.5, 75), w=w)
    f.line((1035.5, 89), (1043.5, 74), (1051.5, 89), w=w)
    f.line((1094, 105.5), (1046, 105.5), w=w)
    f.line((1060, 97.5), (1045, 105.5), (1060, 113.5), w=w)
    f.text(1097, 116, "BF", size=T, **redi)
    f.rect(1114.5, 171.5, 170, 43.5, lw=2.4)
    f.text(1199, 203, "comparateur", size=T, anchor="c", **it)
    open_l(1114, 1094, 190)
    f.line((1321, 117), (1321, 181.5), (1287, 181.5), w=w)
    f.line((1301, 173.5), (1286, 181.5), (1301, 189.5), w=w)
    f.rect(1335.5, 180.5, 77.5, 42.5, lw=2.4)
    f.text(1374, 213, "VXO", size=T, anchor="c", **it)
    open_l(1335, 1287, 201)
    f.fit(1097, 1310, 156, "Modulateur à PLL", **navi)


@figure("c096_1#0")
def manipulation_cw(f):
    w = 2.4
    T = 28
    for x0, x1, y0, y1, t in ((10, 191, 127, 170, "Oscillateur"), (235, 371, 127, 170, "Ampli 1"),
                              (415, 552, 127, 170, "Ampli 2"), (596, 685, 127, 170, "Filtre"),
                              (242, 444, 37, 80, "Alimentation"), (818, 977, 121, 163, "Oscillateur"),
                              (1085, 1197, 118, 161, "Ampli"), (1244, 1333, 118, 161, "Filtre"),
                              (996, 1197, 17, 60, "Alimentation")):
        f.rect(x0, y0, x1 - x0, y1 - y0, lw=2.6)
        f.text((x0 + x1) / 2, (y0 + y1) / 2 + 10, t, size=T, anchor="c")
    for x0, x1 in ((191, 235), (371, 415), (552, 596)):
        f.line((x0, 150), (x1, 150), w=w)
    f.line((685, 150), (753.5, 150), (753.5, 39), w=w)
    f.line((729, 38), (753.5, 58), (777, 37), w=w)
    f.line((326, 80), (326, 127), w=w)
    f.line((444, 58), (460, 127), w=w)
    f.line((56, 127), (56, 62), (124, 39), w=w)
    f.circle(124, 38.5, 4, stroke=None, fill=BLACK)
    f.circle(122, 60.5, 4, stroke=None, fill=BLACK)
    f.line((122, 60.5), (242, 60.5), w=w)
    f.fit(66, 232, 92, "Manipulateur")
    f.fit(82, 585, 201, "Rupture de l'alimentation de l'oscillateur")
    f.line((995, 40), (904, 121), w=1.6)
    f.line((977, 140.5), (1000, 140.5), (1040, 122), w=w)
    f.circle(1041, 121.5, 4, stroke=None, fill=BLACK)
    f.circle(1041, 140.5, 4, stroke=None, fill=BLACK)
    f.line((1041, 140.5), (1085, 140.5), w=w)
    f.line((1183, 60), (1183, 118), w=w)
    f.line((1197, 140.5), (1244, 140.5), w=w)
    f.line((1333, 140.5), (1377.5, 140.5), (1377.5, 30), w=w)
    f.line((1353, 27), (1377.5, 46), (1401, 27), w=w)
    f.fit(969, 1138, 99, "Manipulateur")
    f.fit(843, 1290, 201, "Rupture du circuit entre deux étages")


@figure("c096_2#0")
def spectres_am_dbl_bli(f):
    T = 28
    f.line((52, 128), (52, 16), w=2.6)
    f.line((44, 30), (52, 12), (60, 30), w=2.6)
    f.text(15, 42, "V", size=T)
    f.line((52, 127.5), (1150, 127.5), w=2.6)
    f.line((1136, 119), (1152, 127.5), (1136, 136), w=2.6)
    f.text(1160, 135, "f", size=T)
    for x0, x1 in ((137, 392), (497, 752)):
        f.rect(x0, 63, x1 - x0, 64.5, stroke=BLACK, fill="#d0d0d0", lw=2.6)
        cx = (x0 + x1) / 2
        f.line((x0, 63), (cx, 127.5), (x1, 63), w=2.6)
    f.rect(900, 63, 127, 64.5, stroke=BLACK, fill="#d0d0d0", lw=2.6)
    f.line((900, 63), (1027, 127.5), w=2.6)
    f.rect(262, 19, 5, 107, stroke=None, fill=RED)
    for x0, y0, x1, y1 in ((348, 33, 270, 41), (700, 21, 393, 80), (700, 21, 614, 53), (709.5, 21, 709.5, 55),
                           (986.5, 27, 986.5, 55)):
        f.line((x0, y0), (x1, y1), stroke=BLUE, w=2)
        _arrow_tip(f, x0, y0, x1, y1, BLUE, size=15, filled=True)
    f.fit(350, 453, 36, "Porteuse")
    f.fit(713, 1008, 23, "BF = signal à transmettre")
    f.fit(111, 398, 162, "Modulation d'Amplitude")
    f.fit(489, 760, 162, "Double Bande Latérale")
    f.fit(865, 1166, 162, "Bande Latérale Inférieure")


@figure("c096_3#0")
def formules_am(f):
    nb = {"b": 1, "i": 1, "color": NAVY}
    i_ = {"i": 1}
    T = 34
    rfit(f, 3, 525, 30, [("S(t) = P . cos (2π.F.t) . [1 + K cos (2π.f.t)]", nb)], cap=T)
    rfit(f, 555, 1333, 30, [("donc S(t) = P . cos (2π.F.t) + P . K . [cos (2π.f.t) . cos (2π.F.t)]", i_)], cap=T)
    for cx, t in ((177, "Porteuse"), (451, "BF"), (808, "Porteuse"), (1155, "Bandes latérales")):
        f.text(cx, 60, t, size=30, anchor="c", italic=True)
    rfit(f, 5, 880, 103, [("On sait par ailleurs que : cos α . cos β = ½ [cos (α + β) + cos (α – β)]", i_)], cap=T)
    rfit(f, 4, 1065, 138, [("donc : ", i_), ("S(t) = P . cos (2π.F.t) + ½ . P . K . [cos (2π.F.t + 2π.f.t) + "
                                             "cos (2π.F.t – 2π.f.t)]", nb)], cap=T)
    for cx, t in ((263, "Porteuse"), (656, "BLS"), (960, "BLI")):
        f.text(cx, 170, t, size=30, anchor="c", italic=True)


@figure("c097_1#0")
def recepteur_conversion_directe(f):
    w = 2.4
    T = 28
    it = dict(italic=True)
    f.line((2, 1), (45, 40), (88, 1), w=w)
    f.line((45, 2), (45, 90.5), (61, 90.5), w=w)
    for x0, x1, t in ((61, 126, "RF"), (139, 224, "mél"), (236, 308, "AF")):
        f.rect(x0, 69.5, x1 - x0, 43, lw=2.6)
        f.text((x0 + x1) / 2, 101, t, size=T, anchor="c", **it)
    for x0, x1 in ((126, 139), (224, 236), (308, 327)):
        f.line((x0, 91), (x1, 91), w=w)
    gnd(f, 327, 67, 350, 115)
    f.poly([(350, 69), (370, 48), (370, 134), (350, 113)], w=2.6)
    f.line((169, 113), (169, 131), w=w)
    f.circle(172.5, 173.5, 42.5, lw=2.6)
    f.text(172, 184, "OL", size=T, anchor="c", **it)
    f.fit(80, 199, 33, "signal HF", **it)
    f.text(376, 101, "BF", size=T, **it)
    f.fit(21, 117, 145, "filtre de", **it)
    f.fit(47, 117, 180, "bande", **it)
    f.fit(232, 340, 172, "OL ≈ HF", **it)


def _diode_r(f, xa, xb, y, half=12.5, bar=17):
    f.poly([(xa, y - half), (xb, y), (xa, y + half)], stroke=None, fill=BLACK)
    f.line((xb + 1, y - bar), (xb + 1, y + bar), w=2.4)


@figure("c095_3#0")
def discriminateurs(f):
    w = 2.4
    T = 28
    red = dict(color=RED)
    # ---- Travis
    f.text(4, 63, "FM", size=T, **red)
    f.text(6, 118, "FI", size=T, **red)
    f.line((13, 86), (72, 86), w=w)
    vcoil(f, 72, 86, 145, 3, 18, side=1, w=w)
    f.line((72, 145), (72, 183), w=w)
    gnd(f, 52, 183, 91, 193)
    f.line((131, 85), (131, 24), (282, 24), w=w)
    vcoil(f, 131, 85, 145, 3, 18, side=-1, w=w)
    f.line((131, 145), (131, 228), (282, 228), w=w)
    _diode_r(f, 282, 305, 24)
    _diode_r(f, 282, 307, 228)
    f.line((306, 24), (468, 24), (468, 83), w=w)
    f.line((308, 228), (468, 228), (468, 145), w=w)
    vcoil(f, 468, 83, 145, 3, 18, side=1, w=w)
    f.line((230, 24), (230, 45), w=w)
    vcoil(f, 230, 45, 105, 3, 18, side=-1, w=w)
    f.line((230, 105), (230, 147), w=w)
    vcoil(f, 230, 147, 207, 3, 18, side=-1, w=w)
    f.line((230, 207), (230, 228), w=w)
    f.line((269.5, 24), (269.5, 65), w=w)
    f.line((250, 65), (289, 65), w=2.6)
    f.line((250, 86), (289, 86), w=2.6)
    f.line((269.5, 86), (269.5, 167), w=w)
    f.line((250, 167), (289, 167), w=2.6)
    f.line((250, 188), (289, 188), w=2.6)
    f.line((269.5, 188), (269.5, 228), w=w)
    f.line((230, 126.5), (423, 126.5), w=w)
    gnd(f, 423, 106, 432, 145)
    f.line((388, 24), (388, 43.5), w=w)
    f.rect(367.5, 43.5, 40.5, 60, lw=2.4)
    f.line((388, 103.5), (388, 145.5), w=w)
    f.rect(367.5, 145.5, 40.5, 60.5, lw=2.4)
    f.line((388, 206), (388, 228), w=w)
    vcoil(f, 527, 100, 145, 2, 18, side=-1, w=w)
    f.line((527, 100), (527, 86), (561, 86), w=w)
    f.line((547, 76), (562, 86), (547, 96), w=w)
    f.line((527, 145), (527, 224), w=w)
    gnd(f, 507, 224, 546, 233)
    f.text(135, 75, "FI–δF", size=T)
    f.text(135, 198, "FI+δF", size=T)
    f.text(432, 52, "A", size=T)
    f.text(432, 216, "B", size=T)
    f.text(570, 92, "BF", size=T, **red)
    f.fit(185, 250, 256, "Travis", italic=True, color=NAVY)
    # ---- Foster-Seeley
    f.text(40, 331, "PM", size=T, **red)
    f.text(40, 378, "FI", size=T, **red)
    f.line((47, 352), (165, 352), w=w)
    f.line((165.5, 330), (165.5, 368), w=w)
    f.line((184, 330), (184, 368), w=w)
    f.line((184, 352), (227.5, 352), (227.5, 432), w=w)
    f.text(201, 341, "C", size=T)
    f.line((126, 352), (126, 392), w=w)
    f.line((86, 392), (126, 392), w=w)
    vcoil(f, 126, 392, 475, 4, 19, side=1, w=w)
    f.line((86, 392), (86, 435), w=w)
    f.line((67, 434.5), (106, 434.5), w=2.6)
    f.line((67, 454), (106, 454), w=2.6)
    f.line((86, 454), (86, 475), (126, 475), (126, 510), w=w)
    gnd(f, 107, 510, 145, 520)
    vcoil(f, 185, 392, 475, 4, 19, side=-1, w=w)
    f.line((185, 392), (217, 392), w=w)
    f.line((185, 433.5), (421, 439), w=w)
    f.line((185, 475), (187, 510), (348, 510), w=w)
    f.line((234, 391), (285, 391), w=w)
    f.line((285, 352), (285, 429), w=w)
    f.line((285, 441), (285, 474.5), w=w)
    f.line((265, 474.5), (303, 474.5), w=2.6)
    f.line((265, 494.5), (303, 494.5), w=2.6)
    f.line((285, 494.5), (285, 510), w=w)
    f.line((285, 352), (336, 352), w=w)
    _diode_r(f, 336, 361, 352, half=13, bar=16)
    f.line((362, 352), (461, 352), w=w)
    _diode_r(f, 348, 371, 510, half=13, bar=24)
    f.line((372, 510), (443, 510), w=w)
    f.line((421, 352), (421, 372.5), w=w)
    f.rect(402, 372.5, 40, 40, lw=2.4)
    f.line((421, 412.5), (421, 453.5), w=w)
    f.rect(402, 453.5, 40, 41, lw=2.4)
    f.line((421, 494.5), (421, 510), w=w)
    f.text(465, 349, "A", size=T)
    f.text(465, 522, "B", size=T)
    f.text(486, 441, "BF", size=T, **red)
    f.fit(200, 350, 541, "Foster-Seeley", italic=True, color=NAVY)


@figure("c095_4#0")
def detecteur_pente(f):
    lav = "#6e6eb4"
    f.line((34.5, 169), (34.5, 36), w=2.4)
    f.poly([(26.5, 38), (34.5, 22), (42.5, 38)], stroke=None, fill=BLACK)
    f.line((34, 169.5), (172, 169.5), w=2.4)
    f.poly([(170, 162), (186, 169.5), (170, 177)], stroke=None, fill=BLACK)
    f.text(40, 34, "U", size=26)
    f.text(175, 206, "f", size=26)
    f.spline([(38, 163), (47, 163), (56, 158), (65, 148), (73, 135), (85, 110), (99, 82), (110, 67), (119, 61),
              (128, 65), (138, 85), (150, 118), (160, 147), (164, 154)], stroke=RED, w=1.8)
    f.line((34, 84.5), (99, 84.5), (99, 224), stroke=lav, w=2.2)
    f.line((34, 135.5), (73, 135.5), (73, 224), stroke=lav, w=2.2)
    f.line((34, 107), (86, 107), (86, 288), stroke=NAVY, w=1.6, dash=[5, 4], cap="b")
    f.poly([(80, 286), (86, 298), (92, 286)], stroke=None, fill=NAVY)
    f.pcurve(lambda t: (86 + 13 * math.cos(2 * math.pi * t / 40), 198 + t), 0, 80, n=120, w=1.4)
    f.fit(110, 183, 245, "Signal")
    f.fit(110, 150, 278, "FM")
    f.text(45, 305, "T", size=26)


@figure("c096_4#0")
def melangeurs_equilibres(f):
    w = 2.4
    T = 28
    red = dict(color=RED)
    # ---- MOSFET balanced mixer
    f.text(2, 145, "BF", size=T, **red)
    f.line((42, 136.5), (84, 136.5), w=w)
    vcoil(f, 84, 136, 220, 4, 20, side=1, w=w)
    f.line((84, 220), (84, 284), w=w)
    gnd(f, 63, 282, 104, 292)
    vcoil(f, 146, 136, 220, 4, 20, side=-1, w=w)
    f.line((146, 136), (146, 115), (333, 115), w=w)
    f.line((146, 220), (146, 244), (333, 244), w=w)
    f.line((146, 178.5), (183, 178.5), w=w)
    gnd(f, 183, 158, 193, 198)
    for y0, y1 in ((49, 92), (135, 221), (264, 373)):
        f.line((229.5, y0), (229.5, y1), w=w)
    f.line((229.5, 49.5), (333, 49.5), w=w)
    f.line((229.5, 309), (333, 309), w=w)
    f.line((82, 372), (146, 372), w=w)
    f.line((146.5, 352), (146.5, 392), w=w)
    f.line((167, 352), (167, 392), w=w)
    f.line((167, 372), (229.5, 372), w=w)
    f.text(35, 376, "HF", size=T, **red)
    for cy, ga, gb in ((80, 49.5, 115), (274, 244, 309)):
        f.circle(365, cy, 74, lw=3.4)
        f.line((333.5, ga - 20), (333.5, ga + 20), w=w)
        f.line((333.5, gb - 21), (333.5, gb + 19), w=w)
        f.rect(349, ga - 21, 11, 104, stroke=None, fill=BLACK)
        ys = cy + 12
        f.line((362, ys), (396.5, ys), (396.5, ys + 88 if cy < 200 else 372), w=w)
        f.poly([(360, ys), (372, ys - 8), (372, ys + 8)], stroke=None, fill=BLACK)
    gnd(f, 376, 174, 416, 185)
    gnd(f, 376, 367, 416, 377)
    f.line((360, 50), (542, 50), (542, 116), w=w)
    f.line((360, 244), (542, 244), (542, 199), w=w)
    vcoil(f, 542, 116, 199, 4, 21, side=1, w=w)
    f.line((501, 157), (542, 157), w=w)
    f.text(480, 164, "+", size=22, anchor="c")
    vcoil(f, 604, 116, 199, 4, 20, side=-1, w=w)
    f.line((604, 116), (604, 112.5), (665, 112.5), w=w)
    f.line((604, 199), (604, 367), w=w)
    gnd(f, 584, 367, 624, 377)
    f.rect(665.5, 71.5, 126, 84, lw=3.4)
    f.text(728.5, 103, "Filtre", size=T, anchor="c")
    f.text(728.5, 136, "à Quartz", size=T, anchor="c")
    f.line((729, 156), (729, 367), w=w)
    gnd(f, 709, 367, 749, 377)
    f.line((792, 115), (833, 115), w=w)
    f.text(798, 108, "BLU", size=T, **red)
    f.text(504, 37, "DBL", size=T, **red)
    f.fit(90, 730, 418, "Mélangeur équilibré à MosFet suivi d’un filtre à Quartz")
    # ---- diode ring mixer
    f.text(903, 54, "BF", size=T, **red)
    f.line((917, 65), (917, 116), w=w)
    vcoil(f, 917, 116, 220, 4, 18, side=1, w=w)
    f.line((917, 220), (917, 296), w=w)
    gnd(f, 892, 293, 943, 304)
    vcoil(f, 996, 116, 220, 4, 18, side=-1, w=w)
    f.line((996, 116), (996, 64), (1152, 64), (1152, 117), w=w)
    f.line((996, 220), (996, 299), (1152, 299), (1152, 246), w=w)
    f.line((996, 168), (1018, 168), w=w)
    gnd(f, 1018, 143, 1026, 194)
    f.rect(1074, 117, 156, 129.5, lw=2.4)
    for xa, xb in ((1098, 1126), (1176, 1204)):
        f.poly([(xa, 103), (xb, 117), (xa, 131)], stroke=None, fill=BLACK)
        f.line((xb + 1, 91), (xb + 1, 142), w=w)
    for xa, xb in ((1128, 1100), (1206, 1178)):
        f.poly([(xa, 233), (xb, 246.5), (xa, 260)], stroke=None, fill=BLACK)
        f.line((xb - 1, 221), (xb - 1, 272), w=w)
    f.line((1074, 168), (1048, 168), (1048, 288), w=w)
    f.line((1048, 310), (1048, 351), (1282, 351), (1282, 273), w=w)
    f.line((1230, 168), (1282, 168), w=w)
    vcoil(f, 1282, 168, 273, 4, 20, side=1, w=w)
    f.line((1255.5, 64), (1255.5, 159), w=w)
    f.line((1255.5, 178), (1255.5, 220), (1282, 220), w=w)
    f.text(1242, 54, "HF", size=T, **red)
    f.line((1361, 64), (1361, 168), w=w)
    vcoil(f, 1361, 168, 273, 4, 18, side=-1, w=w)
    f.line((1361, 273), (1361, 348), w=w)
    gnd(f, 1335, 347, 1385, 355)
    f.text(1330, 49, "DBL", size=T, **red)
    f.fit(895, 1354, 418, "Mélangeur équilibré en anneau à diodes")


@figure("c097_2#0")
def demodulation_blu_cw(f):
    lg, dg = "#d9d9d9", "#bfbfbf"
    for cy, span, t in ((145, 240, "Démodulation BLU"), (412, 215, "Démodulation CW")):
        f.text(28, cy, t, size=10.0 * span / text_width(t, 10.0), rot=-90, anchor="c", va="middle")
    for y, x0, x1 in ((190, 116, 1308), (470, 116, 1332)):
        f.line((x0, y), (x1, y), w=3)
        f.poly([(x1 - 4, y - 8), (x1 + 14, y), (x1 - 4, y + 8)], stroke=None, fill=BLACK)
    f.text(1328, 197, "f", size=28)
    f.text(1350, 478, "f", size=28)
    # ---- SSB blocks
    for x0, x1 in ((222, 379), (612, 769)):
        f.rect(x0, 82, x1 - x0, 108, stroke=None, fill=lg)
        f.poly([(x0, 80), (x1 + 3, 190), (x0, 190)], stroke=None, fill=dg)
        f.line((x0 - 1, 79), (x0 - 1, 192), w=5)
        f.line((x0, 80), (x1 + 3, 190), w=4)
    f.line((221, 190), (221, 218), w=2)
    f.line((394.5, 185), (394.5, 218), w=2)
    f.spline([(160, 210), (192, 202), (200, 175), (204, 120), (212, 75), (232, 58), (300, 50), (360, 54), (384, 66),
              (392, 110), (396, 165), (402, 192), (420, 207), (455, 215)], stroke="#3030ff", w=1.8)
    for x0, x1 in ((797, 955), (1105, 1255)):
        f.rect(x0, 80, x1 - x0, 107, stroke=None, fill=lg)
        f.poly([(x0, 187), (x1, 80), (x1, 187)], stroke=None, fill=dg)
        f.line((x1 + 0.5, 81), (x1 + 0.5, 190), stroke="#606060", w=3)
    f.line((797, 187), (955, 80), w=1.8)
    f.line((1105, 187), (1255, 80), w=1.4, dash=[3, 2], cap="b")
    f.line((784.5, 60), (784.5, 176), stroke="#ff9090", w=3)
    f.line((784.5, 176), (784.5, 215), stroke="#606060", w=2.4)
    f.line((1104, 187), (1104, 209), w=2)
    f.line((1255, 185), (1255, 206), w=2)
    for x0, y0, x1, y1 in ((304, 250, 302, 153), (720, 42, 777, 68), (878, 250, 888, 165), (1143, 60, 1190, 158)):
        f.line((x0, y0), (x1, y1), stroke=BLUE, w=2)
        _arrow_tip(f, x0, y0, x1, y1, BLUE, size=16, filled=True)
    for x0, x1, y, t in ((194, 462, 40, "Courbe filtre à Quartz"), (149, 285, 237, "7,197 MHz"),
                         (322, 462, 237, "7,200 MHz"), (142, 457, 268, "Bande Latérale Inférieure"),
                         (599, 1018, 40, "Reconstitution de l'AM par le BFO"), (716, 856, 240, "7,200 MHz"),
                         (590, 1011, 268, "Bande Latérale Supérieure rétablie"), (1067, 1184, 47, "BF Audio"),
                         (1077, 1165, 225, "200 Hz"), (1211, 1317, 225, "3000 Hz"),
                         (1085, 1270, 280, "après détection")):
        f.fit(x0, x1, y, t, max_size=30)
    # ---- CW
    f.spline([(262, 500), (280, 490), (287, 440), (295, 372), (305, 345), (320, 338), (338, 345), (350, 372),
              (360, 440), (366, 485), (380, 500), (402, 502)], stroke="#3030ff", w=1.8)
    f.rect(326, 382, 6, 86, stroke=None, fill=RED)
    f.rect(804, 382, 4, 86, stroke=None, fill=RED)
    f.line((1190, 381), (1190, 490), w=4)
    f.line((1146.5, 470), (1146.5, 488), stroke=RED, w=1.4)
    f.line((286.5, 470), (286.5, 493), w=2)
    f.line((374, 470), (374, 489), w=2)
    f.line((761.5, 345), (761.5, 470), w=1.2, dash=[1.6, 1.6], cap="b")
    f.line((761.5, 470), (761.5, 493), w=2)
    for x0, y0, x1, y1 in ((243, 337, 285, 420), (436, 383, 333, 425), (698, 351, 760, 420), (1150, 360, 1188, 415)):
        f.line((x0, y0), (x1, y1), stroke=BLUE, w=1.8)
        _arrow_tip(f, x0, y0, x1, y1, BLUE, size=15, filled=True)
    for x0, x1, y, t in ((135, 504, 337, "Filtre étroit pour CW (500 Hz)"),
                         (567, 961, 337, "Porteuse reconstituée par le BFO"), (1108, 1281, 355, "Battement BF"),
                         (441, 648, 393, "Message CW sur"), (441, 594, 425, "7,0300 MHz"),
                         (115, 285, 524, "7,02975 MHz"), (376, 545, 524, "7,03025 MHz"), (1183, 1263, 520, "800 Hz")):
        f.fit(x0, x1, y, t, max_size=30)
    f.text(718, 524, "7,0292 MHz", size=28)
    f.text(1122, 520, "0 Hz", size=28)
