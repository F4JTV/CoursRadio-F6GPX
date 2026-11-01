"""Chapter 3 (transformers, cells, meters) figures."""
import math

from figdsl import BLACK, RED, figure

from .t02_alternatif import BLUE, NAVY, GREY, NB, BU, I_

S = 30


def vcoil(f, x, y0, y1, n, depth, side=1, w=2.2):
    """Vertical coil from y0 to y1 made of n half loops bulging to side (+1 right, -1 left)."""
    step = (y1 - y0) / n
    pts = []
    for k in range(n):
        for i in range(17):
            a = math.pi * i / 16
            pts.append((x + side * math.sin(a) * depth, y0 + k * step + step / 2 - math.cos(a) * step / 2 * 1.06))
    f.line(pts, w=w)


def blue_chevron(f, x, y, left=False, size=11):
    d = -1 if left else 1
    f.line((x - d * size * 2, y - size), (x, y), (x - d * size * 2, y + size), stroke=BLUE, w=2.6)


@figure("c053_1#0")
def tableau_rapports(f):
    f.rect(2, 2, 281, 132, lw=2.2)
    k = dict(size=31, bold=True, color=NAVY)
    for x, t in ((25, "N"), (60, "U_{s}"), (110, "I_{p}"), (152, "n_{s}"), (198, "√Z_{s}")):
        f.text(x, 43, t, **k)
    for x, t in ((26, "1"), (60, "U_{p}"), (112, "I_{s}"), (152, "n_{p}"), (200, "√Z_{p}")):
        f.text(x, 112, t, **k)


@figure("c053_1#1")
def transformateur(f):
    f.line((204, 19), (322, 19), w=2.4)
    vcoil(f, 322, 19, 251, 6, 16, side=1)
    f.line((204, 251), (322, 251), w=2.4)
    f.rect(359, 22, 8, 193, stroke=None, fill=BLACK)
    f.line((371, 22), (371, 215), w=2.4)
    f.line((398, 42), (588, 44), w=2.4)
    vcoil(f, 398, 42, 148, 3, 15, side=-1)
    f.line((398, 148), (477, 213), (588, 213), w=2.4)
    f.line((588, 44), (588, 70), w=2.4)
    f.line((588, 185), (588, 213), w=2.4)
    f.rect(558.5, 71.5, 57, 112, lw=3.5)
    f.text(587, 127, "Charge", size=S, rot=-90, anchor="c", va="middle")
    f.line((184.5, 14), (184.5, 250), stroke=BLUE, w=2.6)
    f.line((172, 230), (184.5, 250), (197, 230), stroke=BLUE, w=2.6)
    f.line((647.5, 66), (647.5, 194), stroke=BLUE, w=2.6)
    f.line((635, 174), (647.5, 194), (660, 174), stroke=BLUE, w=2.6)
    blue_chevron(f, 263, 19)
    blue_chevron(f, 501, 43, left=True)
    f.text(248, 59, "I_{p}", size=S)
    f.text(134, 106, "U_{p}", size=S)
    f.text(673, 126, "U_{s}", size=S)
    f.text(501, 77, "I_{s}", size=S)
    f.text(382, 207, "n_{s}", size=S)
    f.text(284, 240, "n_{p}", size=S)
    f.text(10, 247, "P_{p} = U_{p} . I_{p}", size=S)
    f.text(480, 248, "P_{s} = U_{s} . I_{s}", size=S)
    s = 31
    f.rich(792, 37, [("N = Rapport de transformation = n_{s} / n_{p}", NB)], size=s)
    f.text(792, 72, "P_{s} = U_{s} . I_{s} = U_{p}. I_{p} = P_{p} ⇒ η = 100%", size=s)
    f.rich(792, 108, [("U_{s} = U_{p} . N", NB), ("     ou  U_{p} = U_{s} / N", {})], size=s)
    f.text(792, 145, "N = U_{s} / U_{p}  ou  N = I_{p} / I_{s}", size=s)
    f.rich(792, 182, [("I_{s} = I_{p} / N", NB), ("   ou  I_{p} = I_{s} . N", {})], size=s)
    f.rich(792, 220, [("Z_{s} = Z_{p} . N²", NB), ("    ou  Z_{p} = Z_{s} / N² ou N = √(Z_{s} / Z_{p})", {})], size=s)


@figure("c053_2#0")
def transfo_non_parfait(f):
    s = 31
    it = dict(size=s, italic=True)
    f.line((66, 19), (206, 19), w=2.4)
    vcoil(f, 206, 19, 232, 6, 15, side=1)
    f.line((66, 232), (206, 232), w=2.4)
    f.rect(230, 25, 9, 200, stroke=None, fill=BLACK)
    f.line((242.5, 25), (242.5, 225), w=3)
    f.line((272, 61), (410, 61), w=2.4)
    vcoil(f, 272, 61, 190, 4, 14, side=-1)
    f.line((272, 190), (410, 190), w=2.4)
    f.text(24, 95, "Primaire", **it)
    f.text(285, 115, "Secondaire", **it)
    f.text(102, 222, "n_{p}", **it)
    f.text(291, 215, "n_{s}", **it)
    f.rich(10, 268, [("Rapport de transformation : ", {}), ("N = n_{s} / n_{p}", {"b": 1})], size=s)
    f.rich(21, 305, [("Rendement", BU), (" : ", {"b": 1}), ("η(%) = (P_{s} / P_{p}) x 100", NB)], size=s)
    lines = ["P_{s} = U_{s} . I_{s} = P_{p} . η", "P_{p} = U_{p} . I_{p}", "U_{s} = U_{p} . N",
             "I_{s} = (I_{p} . η) / N", "Z_{p} = U_{p} / I_{p}", "Z_{s} = U_{s} / I_{s}"]
    for y, t in zip((42, 78, 113, 150, 185, 220), lines):
        f.text(524, y, t, **it)
    f.text(565, 258, "= (U_{p} . N) / [(I_{p} . η) / N ]", **it)
    f.text(565, 293, "= (U_{p} . N²) / (I_{p} . η) = Z_{p} . (N² / η)", **it)
    # autotransformer
    f.line((1036, 16.5), (1200, 16.5), w=2.4)
    vcoil(f, 1200, 16.5, 231, 6, 15, side=-1)
    f.line((1036, 231), (1200, 231), w=2.4)
    f.line((1087, 103.5), (1190, 103.5), w=2.4)
    f.line((1218, 17), (1218, 232), w=2.4)
    f.rect(1223, 17, 7, 215, stroke=None, fill=BLACK)
    f.text(1022, 120, "Primaire", rot=-90, anchor="c", va="middle", **it)
    f.text(1131, 165, "Secon-", rot=-90, anchor="c", va="middle", **it)
    f.text(1165, 165, "daire", rot=-90, anchor="c", va="middle", **it)
    f.text(1259, 62, "I_{P}", rot=-90, anchor="c", va="middle", **it)
    f.text(1259, 168, "I_{S} + I_{P}", rot=-90, anchor="c", va="middle", **it)
    f.text(1004, 260, "Autotransformateur", **it)


@figure("c053_3#0")
def produit_en_croix(f):
    f.ellipse(89, 52, 26, 42, stroke=None, fill="#c8c8c8")
    f.circle(243, 124, 41, stroke=None, fill="#c8c8c8")
    f.ellipse(62, 87, 56, 70, stroke=BLUE, lw=3)
    f.circle(216, 95, 68, stroke=RED, lw=2.4, dash=[2, 3])
    f.text(28, 60, "N···U_{s}···I_{p}···n_{s}···√Z_{s}¶", size=30)
    f.text(28, 95, "¶", size=30)
    f.text(28, 133, "1···U_{p}···I_{s}···n_{p}···√Z_{p}¶", size=30)


@figure("c054_1#0")
def pile(f):
    s = 31
    f.line((74, 70), (74, 5), (383, 5), (383, 45), w=2.4)
    f.rect(52, 70, 44, 42, lw=2.4, dash=[2, 2.5])
    f.text(74, 104, "Ri", size=s, anchor="c")
    f.line((74, 112), (74, 137), w=2.4)
    f.line((30, 136.5), (118, 136.5), w=3.4)
    f.rect(52, 151, 44, 17, stroke=None, fill=BLACK)
    f.line((74, 168), (74, 203), (383, 203), (383, 167), w=4)
    f.rect(340.5, 46.5, 65, 119, lw=3.5)
    f.text(373, 106, "Charge", size=s, rot=-90, anchor="c", va="middle")
    f.rect(9, 29, 131, 151, stroke=RED, lw=1.4, dash=[2, 2])
    f.text(46, 19, "+", size=s)
    f.text(83, 64, "Pile", size=s)
    f.arrow(162.5, 175, 162.5, 114, stroke=BLUE, w=2.6, size=16, open_=True)
    f.text(170, 165, "E", size=s)
    f.arrow(426.5, 165, 426.5, 41, stroke=BLUE, w=2.6, size=16, open_=True)
    f.text(437, 108, "U", size=s)
    blue_chevron(f, 259, 203, left=True)
    f.text(265, 188, "I", size=s)
    f.text(70, 249, "Ri = (E - U) / I = (E / I) – R", size=s, bold=True, color=NAVY)
    f.text(70, 285, "E = (R + Ri) . I", size=s, bold=True, color=NAVY)
    f.text(70, 321, "Q (en Ah) = I . t (en heures)", size=s)
    f.text(70, 357, "Q (en C) = I . t (en secondes)", size=s)


@figure("c054_2#0")
def pile_exemple(f):
    k = dict(size=26, family="sans")
    f.text(11, 50, "E = 4,5 V", **k)
    f.text(11, 84, "ri = 10 Ω", **k)
    f.text(394, 25, "P = ?", bold=True, **k)
    f.rect(250, 13, 133, 54, lw=4)
    f.text(316, 50, "35 Ω", anchor="c", **k)
    f.line((250, 39.5), (167.5, 39.5), (167.5, 61), w=2)
    f.rect(142, 61, 51, 13, stroke=None, fill=BLACK)
    f.line((115, 95), (220, 95), w=4)
    f.line((167.5, 95), (167.5, 120.5), (411.5, 120.5), (411.5, 39.5), (383, 39.5), w=2)


@figure("c055_2#0")
def voltmetre_galva(f):
    s = 31
    f.rect(37.5, 19.5, 89, 45, lw=3.5)
    f.text(82, 52, "R", size=s, anchor="c")
    f.line((14, 37.5), (37.5, 37.5), w=2.2)
    f.line((126.5, 37.5), (239, 37.5), w=2.2)
    f.line((190, 30), (201, 37.5), (190, 45), stroke=BLUE, w=2.6)
    f.circle(260, 38, 20.5, lw=3)
    f.text(260, 48, "G", size=s, anchor="c")
    f.line((280.5, 38), (371, 38), w=2.2)
    f.text(180, 25, "I_{g}", size=s)
    f.text(286, 72, "Ri", size=s)
    f.arrow(320, 83.5, 21, 83.5, stroke=BLUE, w=2.6, size=18, open_=True)
    f.text(86, 118, "U_{calibre} = U_{T}", size=s)
    f.text(6, 175, "Q = (R + Ri) / U_{T} = Ω / V", size=s, bold=True, color=NAVY)
    f.text(111, 210, "Q = 1 / I_{g}", size=s, bold=True, color=NAVY)


@figure("c055_3#0")
def voltmetre_calibre(f):
    k = dict(size=28, family="sans")
    f.path("M30 5.5H175Q199.5 5.5 199.5 30V148Q199.5 172 175 172H30Q5.5 172 5.5 148V30Q5.5 5.5 30 5.5Z",
           stroke=RED, w=2.4)
    f.text(32, 41, "0", **k)
    f.text(120, 41, "10 V", **k)
    f.path("M26 75Q102 10 176 75", stroke=RED, w=2.2, dash=[2, 3])
    f.arrow(89, 117, 143, 63, stroke=RED, w=2.6, size=18)
    f.text(61, 140, "5 kΩ/V", **k)
    f.text(46, 196, "voltmètre", **k)
    f.rect(284, 34, 166, 55, lw=4)
    f.text(367, 72, "R = ?", anchor="c", **k)
    f.line((202, 61.5), (284, 61.5), w=2.2)
    f.line((450, 61.5), (505, 61.5), w=2.2)
    f.line((200, 153.5), (504, 153.5), w=2.2)
    f.arrow(532.5, 144, 532.5, 67, stroke=BLUE, w=2.4, size=16, open_=True)
    f.text(558, 96, "Calibre =", **k)
    f.text(559, 130, "100 V", **k)


@figure("c055_4#0")
def galvanometre(f):
    s = 28
    f.path("M56 139Q169 18 294 119", stroke=RED, w=2.2, dash=[5, 4])
    f.text(198, 25, "cadran", size=s)
    f.arrow(249, 34, 219, 79, w=2, size=14)
    f.text(24, 149, "0", size=s)
    f.text(299, 140, "I_{g}", size=s)
    f.path("M150 152L192 121Q228 96 252 138Q266 168 232 240", stroke="#7f7f7f", w=14, cap=None)
    f.text(129, 159, "N", size=s)
    f.text(276, 248, "S", size=s)
    f.line((167.5, 212), (167.5, 92), stroke=RED, w=2.2)
    f.poly((161, 93), (174, 93), (167.5, 77), stroke=None, fill=RED)
    f.circle(167.5, 212, 6, stroke=None, fill=RED)
    pts = []
    for k in range(3):
        for i in range(17):
            a = math.pi * i / 16
            pts.append((154 + k * 19 + 9.5 - math.cos(a) * 11, 230 - math.sin(a) * 30))
    f.line(pts, w=2.2)
    f.line((129.5, 230), (129.5, 317), w=2.4)
    f.line((210.5, 230), (210.5, 310), w=2.4)
    f.line((205, 262), (210.5, 252), (216, 262), w=1.8)
    f.circle(131, 246, 8, stroke=None, fill=BLACK)
    f.arrow(131, 246, 55, 312, w=1.8, size=14, both=True, dash=[5, 4])
    f.text(5, 192, "Ressort", size=s)
    f.text(5, 233, "de rappel", size=s)
    f.arrow(66, 248, 94, 279, stroke=BLUE, w=2.4, size=14)
    f.text(188, 272, "I", size=s)
    f.arrow(251, 279, 171, 228, stroke=BLUE, w=2.4, size=14)
    f.text(259, 296, "bobine", size=s)
    f.text(268, 332, "mobile", size=s)
    f.arrow(303, 188, 266, 188, stroke=BLUE, w=2.6, size=14)
    f.text(311, 194, "aimant", size=s)


def _galva(f, cx, cy, r=21):
    f.circle(cx, cy, r, lw=3.2)
    f.text(cx, cy + 10, "G", size=31, anchor="c")


@figure("c055_1#0")
def voltmetre_amperemetre(f):
    s = 31
    left = [(21, [("Voltmètre", BU)], 92), (57, [("U_{T} = U_{R} + U_{g}", NB)], 92), (92, ["U_{g} = Ri . I_{g}"], 92),
            (128, ["U_{R} = R . I_{g}"], 92), (164, [("R = (U_{T} / I_{g}) – Ri", NB)], 92),
            (200, ["= (U_{T} / I_{g}) – (U_{g} / I_{g})"], 116), (236, ["= (U_{T} – U_{g}) / I_{g}"], 116),
            (272, ["= (U_{T} – U_{g}) . (Ri / U_{g})"], 116), (308, ["I_{g} doit être le plus faible possible"], 92)]
    for y, parts, x in left:
        f.rich(x, y, parts, size=s)
    f.line((340, 66), (428, 66), w=2.4)
    blue_chevron(f, 391, 66, left=True, size=13)
    f.rect(428, 39, 66, 44, lw=4)
    f.text(461, 75, "R", size=s, anchor="c")
    f.line((494, 66), (540, 66), w=2.4)
    _galva(f, 561, 61)
    f.line((582, 66), (653, 66), w=2.4)
    f.text(387, 47, "I_{g}", size=s)
    f.text(587, 101, "Ri", size=s)
    f.arrow(385, 116.5, 511, 116.5, stroke=BLUE, w=2.4, size=18, open_=True)
    f.arrow(539, 116.5, 600, 116.5, stroke=BLUE, w=2.4, size=18, open_=True)
    f.arrow(385, 192.5, 600, 192.5, stroke=BLUE, w=2.4, size=18, open_=True)
    f.text(410, 151, "U_{R}", size=s)
    f.text(543, 157, "U_{g}", size=s)
    f.text(455, 225, "U_{T}", size=s)
    f.line((695, 35), (695, 315), stroke=GREY, w=1.2, dash=[1.5, 2])
    # ammeter
    f.line((826, 65.5), (871, 65.5), w=2.4)
    _galva(f, 892, 61)
    f.line((913, 65.5), (958.5, 65.5), (958.5, 162), (938, 162), w=2.4)
    f.line((826, 65.5), (826, 162.5), (868, 162.5), w=2.4)
    f.rect(870, 142, 66, 44, lw=4)
    f.text(903, 175, "R", size=s, anchor="c")
    f.line((760, 116), (826, 116), w=2.4)
    f.line((958.5, 116), (1002, 116), w=2.4)
    for x, y in ((833, 65.5), (789, 116), (838, 162.5)):
        blue_chevron(f, x, y, left=True, size=13)
    f.text(823, 48, "I_{g}", size=s)
    f.text(918, 101, "Ri", size=s)
    f.text(782, 145, "I_{T}", size=s)
    f.text(823, 197, "I_{R}", size=s)
    right = [(21, [("Ampèremètre", BU)], 1049), (57, [("I_{T} = I_{g} + I_{R}", NB)], 1049),
             (92, ["I_{g} = U_{g} / Ri"], 1049), (128, ["I_{R} = U_{g} / R"], 1049),
             (164, [("R = U_{g} / (I_{T} – Ig)", NB)], 1049), (200, ["= (Ri . I_{g}) / (I_{T} – Ig)"], 1079),
             (236, ["= Ri / ((I_{T} / Ig) – 1)"], 1079), (308, ["Ri doit être la plus faible possible"], 831)]
    for y, parts, x in right:
        f.rich(x, y, parts, size=s)


@figure("c056_1#0")
def ohmmetre_wattmetre(f):
    s = 31
    it = dict(size=s, italic=True)
    f.text(17, 95, "Ohmmètre", rot=-90, anchor="c", va="middle", **it)
    f.line((113.5, 117), (113.5, 38), (143, 38), w=2.4)
    _galva(f, 164, 27, 21)
    f.line((185, 38), (223, 38), w=2.4)
    f.rect(225, 11, 82, 55, lw=3.5)
    f.text(266, 47, "R", **it)
    f.line((307, 38), (392, 38), w=2.4)
    f.ellipse(392, 38, 6, 8, stroke=None, fill=BLACK)
    f.line((197, 38), (197, 94), (252, 94), (252, 70), w=2)
    f.line((243, 79), (252, 68), (261, 79), w=2)
    f.line((59, 115.5), (168, 115.5), w=3.4)
    f.rect(86, 138, 55, 11, stroke=None, fill=BLACK)
    f.line((113.5, 149), (113.5, 171), (392, 171), w=2.4)
    f.ellipse(392, 171, 6, 8, stroke=None, fill=BLACK)
    f.arrow(182.5, 147, 182.5, 97, stroke=BLUE, w=2.4, size=16, open_=True)
    f.text(192, 140, "E", **it)
    f.line((363, 38), (363, 58), w=2.4)
    f.rect(335, 60, 44, 66, lw=3.5)
    f.text(357, 93, "Rc", rot=-90, anchor="c", va="middle", **it)
    f.line((363, 128), (363, 171), w=2.4)
    f.rect(418, 60, 51, 71, stroke=RED, lw=2.4)
    f.text(443, 95, "Rx", rot=-90, anchor="c", va="middle", color=RED, **it)
    f.line((446, 60), (446, 39), (424, 39), stroke=RED, w=2.4)
    f.line((432, 31), (423, 39), (432, 47), stroke=RED, w=2.4)
    f.line((446, 131), (446, 170), (424, 170), stroke=RED, w=2.4)
    f.line((432, 162), (423, 170), (432, 178), stroke=RED, w=2.4)
    # wattmeter
    f.text(17, 358, "Wattmètre", rot=-90, anchor="c", va="middle", **it)
    f.text(78, 291, "Entrée", color=RED, **it)
    f.text(394, 291, "Sortie", color=RED, **it)
    f.line((169, 282), (390, 282), w=2.4)
    f.line((280, 282), (280, 303), w=2.4)
    f.rect(258, 304, 44, 43, lw=3.5)
    f.text(280, 335, "R", anchor="c", **it)
    f.line((280, 349), (280, 370), w=2.4)
    _galva(f, 280, 391, 21)
    f.line((280, 412), (280, 431), w=2.4)
    f.rect(254, 431, 43, 11, stroke=None, fill=BLACK)
    f.text(176, 358, "U", **it)
    f.arrow(213.5, 414, 213.5, 308, stroke=BLUE, w=2.4, size=16, open_=True)
    f.text(313, 425, "Ri", **it)
    f.text(63, 451, "P = U² / Z", **it)


@figure("c056_2#0")
def microphone(f):
    f.circle(47, 30, 21, lw=3.2)
    f.rect(70, 6, 24, 47, stroke=None, fill=BLACK)
    f.line((94, 29), (154, 29), w=2.6)
    for y, t in ((99, "Microphone"), (135, "(représentation"), (171, "synoptique)")):
        f.text(95, y, t, size=31, anchor="c")


@figure("c056_3#0")
def haut_parleur(f):
    f.rect(80, 28, 30, 63, stroke=None, fill=BLACK)
    f.line((81, 28), (53, 4), (53, 116), (81, 91), w=3.2)
    f.line((110, 58), (192, 58), w=2.6)
    for y, t in ((148, "Haut-parleur"), (185, "(représentation"), (221, "synoptique)")):
        f.text(96, y, t, size=31, anchor="c")


@figure("c056_4#0")
def relais(f):
    it = dict(size=31, italic=True)
    f.rect(4, 60, 138, 7, stroke=None, fill=BLACK)
    f.line((4, 72.5), (142, 72.5), w=2.2)
    pts = []
    n, x0, x1, base, h = 4, 4, 115, 130, 38
    step = (x1 - x0) / n
    for k in range(n):
        for i in range(17):
            a = math.pi * i / 16
            pts.append((x0 + k * step + step / 2 - math.cos(a) * step / 2, base - 20 - math.sin(a) * h * 0.55))
    f.line(pts, w=2.4)
    f.line((4, 110), (4, 221), (59, 221), w=2.4)
    f.line((115, 110), (115, 175), w=2.4)
    f.rect(88, 175, 54, 5, stroke=None, fill=BLACK)
    f.line((62, 196), (114, 221), w=2.4)
    f.line((111, 221), (170, 221), w=2.4)
    f.text(202, 228, "+", size=31, anchor="c")
    f.line((252, 178), (171, 178), (171, 141), (198, 18), w=2.4)
    f.circle(184, 84, 6, stroke=None, fill=BLACK)
    f.line((184, 84), (250, 84), w=2, dash=[2, 3])
    f.line((242, 79), (252, 84), (242, 89), w=2)
    f.text(249, 105, "ressort", **it)
    f.text(222, 168, "Commun", **it)
    f.line((88, 39), (151, 39), stroke=RED, w=2.4)
    f.circle(142, 39, 8, stroke=None, fill=RED)
    f.text(112, 22, "T", color=RED, **it)
    f.line((189, 39), (253, 39), stroke=BLUE, w=2.4)
    f.circle(197, 39, 8, stroke=None, fill=BLUE)
    f.text(220, 22, "R", color=BLUE, **it)


@figure("c056_5#0")
def circulateur(f):
    cx, cy = 124.5, 80.5

    def port(angle, d0, d1, half):
        u = (math.cos(math.radians(angle)), math.sin(math.radians(angle)))
        n = (-u[1], u[0])
        pts = [(cx + u[0] * d + n[0] * s * half, cy + u[1] * d + n[1] * s * half)
               for d, s in ((d0, 1), (d1, 1), (d1, -1), (d0, -1))]
        f.poly(pts, w=3.2, fill="#ffffff")
    port(-150, 60, 112, 17)
    port(-32, 60, 104, 17)
    f.rect(107, 150, 33, 43, lw=3.2, fill="#ffffff")
    f.circle(cx, cy, 70, lw=3.4, fill="#ffffff")
    f.arrow(82, 42, 169, 42, stroke=RED, w=3.4, size=18)
    f.arrow(178, 67, 139, 137, stroke=RED, w=3.4, size=18)
    f.arrow(109, 137, 67, 67, stroke=RED, w=3.4, size=18)
    it = dict(size=31, italic=True, color=BLUE)
    f.text(1, 33, "1", **it)
    f.text(232, 40, "2", **it)
    f.text(154, 179, "3", **it)
