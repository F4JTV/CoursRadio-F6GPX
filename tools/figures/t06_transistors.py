"""Chapter 6 (transistors and tubes) figures."""
import math

from figdsl import BLACK, RED, figure

from .t02_alternatif import BLUE, NAVY, GREY, NB, BU, I_
from .t05_diodes import gnd

S = 31
W = 2.4


def bjt(f, cx, cy, r, base_x, c_end, e_end, pnp=False, lw=3, base_y=None, arrow=16):
    """Bipolar transistor drawn as in the course: circle, thick base bar,
    collector and emitter diagonals ending at c_end / e_end."""
    f.circle(cx, cy, r, lw=lw)
    bx = cx - r * 0.51
    gnd(f, bx - 2.5, cy - r * 0.49, bx + 2.5, cy + r * 0.49)
    by = cy if base_y is None else base_y
    f.line((base_x, by), (bx, by), w=W)
    c0 = (bx + 1, cy - r * 0.24)
    e0 = (bx + 1, cy + r * 0.24)
    f.line(c0, c_end, w=W)
    f.line(e0, e_end, w=W)
    ang = math.degrees(math.atan2(e_end[1] - e0[1], e_end[0] - e0[0]))
    if pnp:
        t = 0.35
        f.head(e0[0] + (e_end[0] - e0[0]) * t, e0[1] + (e_end[1] - e0[1]) * t, ang + 180, size=arrow)
    else:
        t = 0.75
        f.head(e0[0] + (e_end[0] - e0[0]) * t, e0[1] + (e_end[1] - e0[1]) * t, ang, size=arrow)


@figure("c067_1#0")
def jonctions(f):
    for (y0, y1, letters, lead) in ((5.5, 48.5, "NPN", (49, 67)), (128.5, 170.5, "PNP", (110, 128))):
        f.rect(83.5, y0, 173, y1 - y0, lw=3)
        f.line((148, y0), (148, y1), w=3)
        f.line((191, y0), (191, y1), w=3)
        for x, l in zip((115, 169, 223), letters):
            f.text(x, (y0 + y1) / 2 + 11, l, size=S, anchor="c")
        f.line((169, lead[0]), (169, lead[1]), w=W)
    f.line((83, 26), (19, 26), (19, 67), w=W)
    f.line((257, 26), (320, 26), (320, 67), w=W)
    f.line((83, 149.5), (19, 149.5), (19, 109), w=W)
    f.line((257, 150), (320, 150), (320, 109), w=W)
    f.text(4, 91, "Émetteur", size=S)
    f.text(135, 91, "Base", size=S)
    f.text(215, 91, "Collecteur", size=S)
    # NPN
    bjt(f, 620, 102, 42, 491, (641.5, 63), (665, 162))
    f.line((641.5, 63), (641.5, 0), w=W)
    f.line((665, 162), (665, 186), w=W)
    gnd(f, 636, 185, 689, 196)
    f.text(568, 22, "+ + +", size=S)
    f.text(667, 28, "Collecteur", size=S)
    f.text(689, 90, "Transistor NPN", size=S)
    f.text(472, 89, "+", size=S)
    f.text(474, 133, "Base", size=S)
    f.text(671, 168, "Émetteur", size=S)
    # PNP
    bjt(f, 1115, 102, 42, 986, (1136.5, 63), (1136.5, 140), pnp=True)
    f.line((1136.5, 63), (1136.5, 3), w=W)
    gnd(f, 1115, 0, 1158, 5)
    f.line((1136.5, 140), (1136.5, 174), w=W)
    f.text(967, 89, "+", size=S)
    f.text(988, 133, "Base", size=S)
    f.text(1140, 48, "Collecteur", size=S)
    f.text(1182, 111, "PNP", size=S)
    f.text(1140, 172, "Émetteur", size=S)
    f.text(1109, 195, "+ + +", size=S)


@figure("c067_2#0")
def montages(f):
    for y in (1, 36, 345):
        f.line((1, y), (1448, y), w=2)
    for x in (1, 259, 655, 1052, 1448):
        f.line((x, 1), (x, 345), w=2)
    for x, t in ((130, "Montage"), (457, "Émetteur commun"), (853, "Collecteur commun"), (1250, "Base commune")):
        f.text(x, 30, t, size=S, anchor="c")
    f.text(247, 142, "Schémas", size=S, anchor="r")
    f.rich(247, 208, [("Caractéristiques :", {"u": 1})], size=S, anchor="r")
    f.rich(247, 242, [("Gain", BU), (" en intensité", {})], size=S, anchor="r")
    f.text(247, 277, "en tension", size=S, anchor="r")
    f.rich(247, 311, [("Z Entrée / Sortie", BU)], size=S, anchor="r")
    f.rich(247, 345 - 5, [("Déphasage", BU)], size=S, anchor="r")
    red = dict(size=S, color=RED)
    # common emitter
    bjt(f, 463, 110, 45, 350, (485, 72), (509, 162))
    f.line((485, 72), (485, 47), (554, 47), w=W)
    f.line((509, 162), (509, 190), w=W)
    f.line((397, 190), (578, 190), w=W)
    f.text(511, 76, "Sortie", **red)
    f.text(306, 139, "Entrée", **red)
    # common collector
    bjt(f, 839, 133, 44.5, 703, (862, 95), (846, 168))
    f.line((862, 95), (862, 50), w=W)
    f.line((725, 50), (952, 50), w=W)
    f.line((846, 168), (846, 195), (952, 195), w=W)
    f.text(685, 120, "Entrée", **red)
    f.text(912, 183, "Sortie", **red)
    # common base
    bjt(f, 1234, 130, 44.5, 1097, (1256, 95), (1270, 190))
    f.line((1256, 95), (1256, 68), (1324, 68), w=W)
    f.line((1270, 190), (1242, 190), w=W)
    f.text(1331, 76, "Sortie", **red)
    f.text(1157, 203, "Entrée", **red)
    f.rect(1074, 68, 46, 41.5, lw=2.4)
    f.rect(1074, 143, 46, 41.5, lw=2.4)
    f.text(1088, 99, "R", size=S)
    f.text(1088, 174, "R", size=S)
    f.line((1097, 50), (1097, 68), w=W)
    f.line((1097, 109.5), (1097, 143), w=W)
    f.line((1097, 184.5), (1097, 201), w=W)
    gnd(f, 1075, 200, 1119, 205)
    f.text(1110, 63, "+", size=S)
    rows = [("I_{c} = I_{b}.β, Gain = β", "Moyen", "Moyenne / Élevée", "180° (signal inversé)"),
            ("I_{e} = I_{b}.(β+1), Gain = β+1", "Pas de gain (<1)", "Élevée / Basse", "Pas de déphasage"),
            ("I_{c} ≈ I_{e}, Gain = β/(β+1) < 1", "Élevé", "Basse / Très élevée", "Pas de déphasage")]
    for cx, lines in zip((457, 853, 1250), rows):
        for y, t in zip((242, 277, 311, 340), lines):
            f.text(cx, y, t, size=S, anchor="c")


@figure("c067_3#0")
def to18(f):
    f.circle(137, 98, 49, stroke="#000000", fill="#c0c0c0", lw=13)
    f.rect(194, 90, 17, 14, stroke=None, fill=BLACK)
    f.line((50, 35), (106, 82), w=4)
    f.circle(122, 121, 6.5, lw=2.4, fill="#ffffff")
    f.circle(160, 111, 6.5, lw=2.4, fill="#ffffff")
    f.line((119, 128), (98, 175), w=3)
    f.line((166, 114), (237, 142), w=3)
    it = dict(size=S, italic=True)
    f.text(8, 23, "Collecteur", **it)
    f.text(157, 166, "Émetteur", **it)
    f.text(56, 201, "Base", **it)
    f.text(24, 252, "Brochage d’un boîtier", **it)
    f.text(43, 286, "TO18 vu du dessus", **it)


def chev_down(f, x, y, size=10, color=BLUE):
    f.line((x - size, y - size * 1.6), (x, y), (x + size, y - size * 1.6), stroke=color, w=2.4)


@figure("c067_4#0")
def polarisation(f):
    bjt(f, 211, 192, 38.5, 2, (230.5, 159), (236, 230))
    f.line((230.5, 159), (230.5, 37), w=W)
    f.line((236, 230), (236, 347), w=W)
    gnd(f, 212, 346, 250, 356)
    f.text(223, 20, "+", size=S)
    chev_down(f, 230.5, 87)
    f.line((102, 178), (124, 192), (102, 206), stroke=BLUE, w=2.4)
    chev_down(f, 236, 296)
    f.arrow(270.5, 231, 270.5, 134, stroke=BLUE, w=2.4, size=14)
    f.arrow(191, 247, 152, 213, stroke=BLUE, w=2.2, size=14)
    f.text(27, 30, "I_{b} = I_{c} / β", size=S)
    f.text(27, 65, "I_{b} = I_{e} / (β+1)", size=S)
    f.text(42, 129, "COLLECTEUR", size=S, color=RED)
    f.text(1, 183, "BASE", size=S, color=RED)
    f.text(110, 177, "I_{b}", size=S)
    f.text(53, 244, "V_{be} ≈ 1 V", size=S)
    f.text(55, 303, "EMETTEUR", size=S, color=RED)
    f.text(25, 330, "β = I_{c} / I_{b}", size=S)
    f.text(25, 365, "β = (I_{e} / I_{b}) – 1", size=S)
    f.text(254, 82, "I_{c} = I_{b}.β", size=S, bold=True, color=NAVY)
    f.text(275, 177, "V_{ce}", size=S)
    f.text(254, 270, "I_{e} = I_{c} + I_{b}", size=S, bold=True, color=NAVY)
    f.text(280, 303, "= I_{b}.(β+1)", size=S)
    f.poly((339.5, 327), (414, 474.5), (265, 474.5), stroke=BLUE, w=3)
    f.text(330, 392, "I_{c}", size=S)
    f.text(304, 457, "I_{b}", size=S)
    f.text(360, 457, "β", size=S)


IT = dict(size=S, italic=True)


@figure("c068_1#0")
def jfet(f):
    f.circle(135.5, 130, 57.5, lw=3)
    gnd(f, 131, 92, 140, 168)
    f.line((1, 129.5), (112, 129.5), w=W)
    f.poly((110, 117), (110, 142), (131, 129.5), stroke=None, fill=BLACK)
    f.line((140, 112), (159.5, 112), (159.5, 36), w=W)
    f.line((140, 148.5), (159.5, 148.5), (159.5, 250), w=W)
    gnd(f, 122, 249, 193, 259)
    f.text(147, 16, "+", size=S)
    f.fit(92, 153, 50, "Drain")
    f.fit(4, 60, 110, "Porte")
    f.fit(80, 152, 218, "Source")
    # internal structure
    f.fit(215, 531, 20, "Structure interne d’un J-FET", italic=True)
    f.rect(289.5, 43.5, 154, 77, lw=3)
    f.line((213, 80), (289.5, 80), w=W)
    f.line((443.5, 80), (520, 80), w=W)
    f.rect(347.5, 45, 40, 17, stroke="#404040", fill="#a6a6a6", lw=1.6)
    f.rect(347.5, 100, 40, 19, stroke="#404040", fill="#a6a6a6", lw=1.6)
    f.line((366.5, 120), (366.5, 156), w=W)
    f.fit(207, 281, 64, "Source", italic=True)
    f.fit(451, 515, 64, "Drain", italic=True)
    f.arrow(331, 134, 365, 109, stroke=BLUE, w=2.4, size=14)
    f.arrow(448, 133, 402, 88, stroke=BLUE, w=2.4, size=14)
    f.fit(234, 321, 163, "Bague P", italic=True)
    f.fit(403, 495, 163, "Canal N", italic=True)
    f.fit(362, 421, 184, "Porte", italic=True)
    # characteristic
    f.arrow(16, 422.5, 532, 422.5, w=2.4, size=18)
    f.arrow(352, 423, 352, 262, w=2.4, size=18)
    f.text(330, 280, "I_{d}", size=S)
    f.text(500, 452, "+V_{g}", size=S)
    f.spline([(16, 418), (100, 418), (120, 414), (220, 355), (300, 300), (360, 272), (400, 262), (460, 261)],
             stroke=RED, w=2.2, dash=[2, 3])
    f.line((111.5, 399), (111.5, 419), stroke=RED, w=2)
    f.line((400, 407), (400, 420), stroke=RED, w=2)
    f.rich(66, 304, [("Pente", {"i": 1, "u": 1}), (" d’un", {"i": 1})], size=26)
    f.text(68, 337, "transistor J-FET =", size=26, italic=True)
    f.text(66, 370, "I_{d} / V_{g}", size=27, italic=True)
    f.arrow(160, 352, 202, 373, stroke=BLUE, w=2.4, size=14)
    f.text(437, 320, "Conduction", rot=-90, anchor="c", va="middle", **IT)
    f.text(470, 320, "porte > drain", rot=-90, anchor="c", va="middle", **IT)
    f.fit(12, 226, 452, "cut-off ou décollage", italic=True)
    f.fit(346, 452, 452, "saturation", italic=True)


@figure("c068_2#0")
def mosfet(f):
    f.circle(162, 135, 70, lw=3)
    f.line((17, 105.5), (132, 105.5), w=W)
    f.line((132, 84), (132, 124), w=2.6)
    f.line((20, 163.5), (132, 163.5), w=W)
    f.line((132, 144), (132, 183), w=2.6)
    gnd(f, 147, 84, 157, 184)
    f.line((157, 104), (192.5, 104), (192.5, 6), w=W)
    f.line((178, 143.5), (190, 143.5), (190, 250), w=W)
    f.poly((178, 131), (178, 156), (158, 143.5), stroke=None, fill=BLACK)
    gnd(f, 164, 249, 213, 259)
    f.fit(123, 178, 33, "Drain", italic=True)
    f.text(205, 33, "+", size=S)
    f.text(57, 92, "G1", **IT)
    f.fit(9, 82, 133, "Portes.", italic=True)
    f.text(57, 197, "G2", **IT)
    f.fit(112, 177, 235, "Source", italic=True)
    f.rich(45, 285, [("MOS-FET", {"i": 1, "u": 1})], size=27)
    f.fit(36, 160, 318, "à substrat P", italic=True)
    f.fit(3, 204, 352, "(la flèche pénètre)", italic=True)
    # internal structure
    f.fit(312, 502, 117, "Structure interne", italic=True)
    f.fit(320, 497, 150, "d’un MOS-FET", italic=True)
    f.text(312, 186, "–", size=S)
    f.text(369, 186, "Portes", **IT)
    f.text(493, 186, "+", size=S)
    f.text(293, 228, "Source", **IT)
    f.text(469, 228, "Drain", **IT)
    f.rect(267.5, 333, 277, 125.5, lw=3.5)
    f.rect(344, 334, 125, 12, stroke=None, fill="#c0c0c0")
    for x in (355, 382, 430, 457):
        f.line((x - 7, 338), (x + 7, 338), w=1.6)
    f.rect(294, 333, 49.5, 50, stroke=BLACK, fill="#c0c0c0", lw=1.6)
    f.rect(469.5, 333, 50, 50, stroke=BLACK, fill="#c0c0c0", lw=1.6)
    f.text(318, 367, "N", **IT, anchor="c")
    f.text(494, 367, "N", **IT, anchor="c")
    f.line((318, 233), (318, 333), w=W)
    f.line((494, 233), (494, 333), w=W)
    gnd(f, 344, 302, 393, 314)
    gnd(f, 419, 302, 468, 314)
    f.line((368.5, 208), (368.5, 302), w=W)
    f.line((444, 208), (444, 302), w=W)
    for x in (354, 384, 427, 457):
        f.text(x, 296, "+", size=S, anchor="c")
    f.line((318, 308), (242.5, 308), (242.5, 408.5), (267, 408.5), w=W)
    f.fit(348, 466, 444, "Substrat P", italic=True)


@figure("c068_3#0")
def ujt(f):
    f.circle(182.5, 101.5, 59.5, lw=3)
    gnd(f, 178, 61, 188, 140)
    f.line((207.5, 3), (207.5, 81.5), (188, 81.5), w=W)
    f.line((188, 115.5), (207, 115.5), (207, 200), w=W)
    gnd(f, 169, 199, 242, 209)
    f.line((9, 41.5), (110, 41.5), (165, 85), w=W)
    f.poly((152, 73), (160, 97), (178, 92), stroke=None, fill=BLACK)
    f.text(157, 18, "+", size=S)
    f.fit(217, 292, 44, "Base 2", italic=True)
    f.fit(4, 105, 64, "Émetteur", italic=True)
    f.rich(26, 126, [("UJT", {"i": 1, "u": 1})], size=S)
    f.fit(217, 290, 168, "Base 1", italic=True)


ELL = "#5050ff"


def bulb(f, cx, cy, rx, ry):
    f.ellipse(cx, cy, rx, ry, stroke=ELL, lw=1.6, dash=[1.5, 2.5])


def cathode_arc(f, xt, yt, xr, xb, yb, w=3):
    c = 2 * xr - (xt + xb) / 2
    f.path(f"M{xt} {yt}Q{c} {(yt + yb) / 2} {xb} {yb}", w=w)


def grid(f, x, y0, y1, y2):
    """Grid: dotted from y0 to y1, solid from y1 to y2."""
    f.line((x, y0), (x, y1), w=1.4, dash=[1.5, 2.5])
    f.line((x, y1), (x, y2), w=2.4)


@figure("c069_1#0")
def thyristor_triac(f):
    f.ellipse(172, 77, 52, 38, lw=2.4)
    f.line((172.5, 12), (172.5, 141), w=W)
    f.poly((159, 62), (186, 62), (172.5, 86), stroke=None, fill=BLACK)
    gnd(f, 147, 85, 198, 93)
    f.line((121, 115.5), (148, 115.5), (172, 94), w=W)
    f.fit(183, 253, 20, "anode", italic=True)
    f.rich(4, 46, [("Thyristor", {"i": 1, "u": 1})], size=27)
    f.fit(11, 109, 128, "gâchette", italic=True)
    f.fit(183, 274, 134, "cathode", italic=True)
    f.ellipse(94, 258.5, 53, 38.5, lw=2.4)
    f.line((94, 195), (94, 250), w=W)
    f.line((94, 268), (94, 324), w=W)
    gnd(f, 52, 244, 134, 250)
    gnd(f, 54, 268, 137, 273)
    f.poly((55, 251), (81, 251), (68, 267), stroke=None, fill=BLACK)
    f.poly((107, 267), (133, 267), (120, 251), stroke=None, fill=BLACK)
    f.line((98, 273), (121, 298), (146, 298), w=W)
    f.fit(105, 195, 203, "anode 1", italic=True)
    f.rich(158, 255, [("Triac", {"i": 1, "u": 1})], size=27)
    f.fit(155, 254, 310, "gâchette", italic=True)
    f.fit(90, 182, 343, "anode 2", italic=True)
    f.rect(355.5, 62.5, 157, 157, lw=2.6)
    for y in (115, 167.5):
        f.line((355.5, y), (512.5, y), w=2.6)
    f.line((407.5, 219.5), (407.5, 272.5), (486.5, 272.5), (486.5, 219.5), w=2.6)
    f.line((433.5, 37), (433.5, 62.5), w=W)
    f.line((433.5, 272.5), (433.5, 324), w=W)
    f.line((381.5, 219.5), (381.5, 297), w=W)
    for x, y, t in ((433, 100, "P"), (433, 152, "N"), (433, 205, "P"), (452, 258, "N")):
        f.text(x, y, t, size=27, italic=True, anchor="c")
    f.fit(399, 469, 29, "anode", italic=True)
    f.fit(320, 419, 318, "gâchette", italic=True)
    f.fit(380, 471, 350, "cathode", italic=True)


@figure("c069_2#0")
def diode_tube(f):
    bulb(f, 252, 128, 147, 94)
    f.line((4, 100.5), (191, 100.5), w=W)
    f.line((4, 183), (192, 183), w=W)
    f.line((192, 100.5), (234, 141), (192, 183), stroke=RED, w=2.4)
    cathode_arc(f, 237, 75, 281, 244, 229)
    f.line((244.5, 229), (244.5, 299), w=W)
    gnd(f, 219, 298, 260, 308)
    gnd(f, 313, 95, 365, 190)
    f.line((365, 142), (402, 142), w=W, dash=[6, 4])
    f.line((402, 142), (402, 267), w=W)
    f.fit(31, 137, 24, "Ampoule")
    f.arrow(114, 41, 136, 64, stroke=BLUE, w=2.2, size=12, open_=True)
    f.fit(4, 142, 116, "Filament de")
    f.fit(29, 142, 151, "chauffage")
    f.fit(385, 497, 70, "Anode ou")
    f.fit(403, 481, 104, "plaque")
    f.fit(431, 519, 175, "DIODE")
    f.fit(136, 229, 253, "Cathode")
    f.fit(428, 481, 273, "+HT")


@figure("c069_3#0")
def triode(f):
    bulb(f, 148, 81, 126, 66)
    cathode_arc(f, 80, 30, 105, 79, 125)
    f.line((80, 125), (80, 199), w=W)
    gnd(f, 54, 198, 95, 208)
    grid(f, 148, 40, 151, 213)
    f.text(158, 216, "-", size=24)
    gnd(f, 189, 47, 232, 133)
    f.line((232, 91), (273, 91), (273, 214), w=W)
    f.fit(278, 339, 220, "+ HT")
    f.fit(243, 354, 22, "Anode ou", italic=True)
    f.fit(259, 339, 56, "plaque", italic=True)
    f.fit(320, 422, 127, "TRIODE", italic=True)
    f.fit(6, 102, 257, "Cathode", italic=True)
    f.fit(136, 204, 257, "Grille", italic=True)


@figure("c069_4#0")
def tetrode_pentode(f):
    bulb(f, 134, 66, 133, 63)
    cathode_arc(f, 42, 10, 62, 41, 104)
    f.line((42, 104), (42, 181), w=W)
    gnd(f, 22, 180, 62, 190)
    grid(f, 103.5, 15, 104, 165)
    grid(f, 144.5, 15, 104, 146)
    f.line((144.5, 145), (205, 145), w=W)
    gnd(f, 185, 23, 227, 107)
    f.line((227, 62), (288, 62), (288, 206), w=W)
    f.fit(258, 381, 31, "TETRODE", italic=True)
    f.fit(147, 218, 168, "Écran", italic=True)
    bulb(f, 405, 290, 175, 81)
    cathode_arc(f, 313, 235, 334, 313, 350)
    f.line((313.5, 350), (313.5, 406), w=W)
    gnd(f, 293, 405, 334, 415)
    f.line((313.5, 235), (313.5, 228.5), (458, 228.5), w=W)
    f.line((458, 228.5), (458, 335), w=1.4, dash=[1.5, 2.5])
    grid(f, 375, 247, 335, 411)
    grid(f, 415.5, 247, 336, 387)
    f.line((415.5, 386), (468, 386), w=W)
    gnd(f, 497, 248, 540, 332)
    f.line((540, 289), (559.5, 289), (559.5, 433), w=W)
    f.line((467, 182), (475, 202), (483, 182), stroke=BLUE, w=2.4)
    f.line((475, 174), (475, 202), stroke=BLUE, w=2.4)
    f.fit(392, 546, 166, "Suppresseuse", italic=True)
    f.fit(161, 288, 399, "PENTODE", italic=True)


@figure("c069_5#0")
def double_tubes(f):
    bulb(f, 361, 100, 171, 94)
    cathode_arc(f, 283, 20, 304.5, 283, 154)
    f.line((282, 154), (282, 214), w=W)
    grid(f, 351, 40, 177, 214)
    grid(f, 407, 120, 177, 214)
    gnd(f, 435, 45, 482, 89)
    gnd(f, 435, 124, 482, 167)
    f.line((482, 67), (687, 67), w=W)
    f.line((482, 146), (687, 146), w=W)
    f.fit(22, 137, 99, "TRIODE-", italic=True)
    f.fit(14, 149, 134, "TETRODE", italic=True)
    f.fit(496, 636, 52, "Oscillateur", italic=True)
    f.fit(496, 633, 183, "Mélangeur", italic=True)
    bulb(f, 1115, 78, 113, 73)
    cathode_arc(f, 1072, 20, 1093.5, 1072, 150)
    f.line((1071, 150), (1071, 214), w=W)
    gnd(f, 1138, 29, 1184, 72)
    gnd(f, 1138, 91, 1184, 133)
    f.line((1184, 50.5), (1296, 50.5), w=W)
    f.line((1184, 112), (1296, 112), w=W)
    f.fit(849, 972, 80, "DOUBLE", italic=True)
    f.fit(848, 946, 114, "DIODE", italic=True)
    f.fit(849, 982, 148, "ou VALVE", italic=True)
