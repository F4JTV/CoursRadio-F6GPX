"""Chapter 5 (diodes) figures."""
import math

from figdsl import BLACK, RED, figure, text_width

from .t02_alternatif import BLUE, NAVY, GREY, NB, BU, I_, _humps

S = 31
IT = dict(size=S, italic=True)


@figure("c064_1#0")
def caracteristique_diode(f):
    f.arrow(198, 194.5, 972, 194.5, w=2.4, size=18, open_=True)
    f.arrow(729.5, 274, 729.5, 9, w=2.4, size=18, open_=True)
    f.text(679, 24, "I_{d}", size=S)
    f.text(980, 226, "U_{d}", size=S)
    f.line((850, 248), (921, 4), stroke=RED, w=1.8, dash=[2, 3])
    f.spline([(290, 445), (289, 300), (290, 210), (300, 204), (340, 205), (600, 198), (800, 190), (845, 186),
              (858, 176), (872, 130), (895, 65), (915, 6)], stroke=RED, w=6, n=8)
    f.text(786, 34, "0,6 V", size=S)
    f.text(981, 76, "0,7 V", size=S)
    f.arrow(805, 48, 838, 172, stroke=BLUE, w=2.6, size=18, open_=True)
    f.arrow(977, 68, 880, 182, stroke=BLUE, w=2.6, size=18, open_=True)
    f.text(297, 55, "Tension Zener", size=S, anchor="c")
    f.text(297, 90, "ou d'avalanche", size=S, anchor="c")
    f.arrow(284.5, 110, 284.5, 191, stroke=BLUE, w=2.6, size=18, open_=True)
    f.text(9, 161, "SENS INVERSE", size=S)
    f.text(982, 161, "SENS DIRECT", size=S)
    f.text(440, 288, "Zone VARICAP", size=S)
    f.text(786, 288, "Zone REDRESSEMENT", size=S)
    f.text(207, 360, "Zone", size=S)
    f.text(297, 360, "ZENER", size=S)
    lines = ["Une des polémiques les plus courantes concerne la tension de seuil : 0,6",
             "ou 0,7 V pour les diodes au Silicium ? Les deux réponses sont exactes :",
             "0,6 V est la tension à partir de laquelle l’intensité augmente et 0,7 V est",
             "la tension pour laquelle la pente de la diode croise l’axe de la tension."]
    for i, t in enumerate(lines):
        f.text(482, 342 + i * 35.3, t, **IT)


SI_BLUE = "#3030ff"
SI_RED = "#ff2020"


@figure("c064_2#0")
def cristal_dope(f):
    r = 89.0
    xs = [157, 330, 524, 720, 893, 1086]
    ys = [126, 306]
    labels = [["Si", "Si", "Si", "Si", "As", "Si"], ["Si", "Ga", "Si", "Si", "Si", "Si"]]
    atoms = {}
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            color = SI_BLUE if i < 3 else SI_RED
            atoms[(i, j)] = (x, y, color)
            f.ellipse(x, y, r, r * 1.04, stroke=color, lw=2)
            f.text(x, y + 11, labels[j][i], **IT, anchor="c")

    def outer_arc(x, y, d, color):
        # arc of the neighbouring (not drawn) atom, crossing the circle at the bond point
        cx, cy = x + d[0] * 2 * r, y + d[1] * 2 * r * 1.04
        base = math.degrees(math.atan2(-d[1], -d[0]))
        f.arc(cx, cy, r, r * 1.04, base - 24, base + 24, stroke=color, w=2)

    def pair(x, y, d, k, missing=False):
        perp = (-d[1], d[0])
        p1 = (x + d[0] * (r - 9) + perp[0] * 12 * k, y + d[1] * (r - 9) * 1.04 + perp[1] * 12 * k)
        p2 = (x + d[0] * (r + 9) - perp[0] * 12 * k, y + d[1] * (r + 9) * 1.04 - perp[1] * 12 * k)
        f.circle(*p1, 10, stroke=None, fill=BLACK)
        if not missing:
            f.circle(*p2, 10, stroke=None, fill=BLACK)

    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for (i, j), (x, y, color) in atoms.items():
        for d in dirs:
            ni, nj = i + d[0], j + d[1]
            inside = (ni, nj) in atoms
            if not inside:
                outer_arc(x, y, d, color)
            if d in ((1, 0), (0, 1)) or not inside:
                k = 1 if (i + j) % 2 else -1
                missing = (i, j) == (0, 1) and d == (1, 0)   # hole next to Ga
                pair(x, y, d, k, missing)
    f.line((637, 18), (637, 418), w=1.4, dash=[2, 3])
    f.text(14, 213, "trou", **IT)
    f.arrow(90, 212, 248, 284, stroke=BLUE, w=2.4, size=16)
    f.circle(952, 185, 10, stroke=None, fill=RED)
    f.line((1201, 178), (968, 178), stroke=RED, w=2.4)
    f.line((988, 168), (966, 178), (988, 188), stroke=RED, w=2.2)
    f.text(1204, 182, "électron", **IT)
    f.text(1204, 218, "libre", **IT)
    f.text(191, 458, "CRISTAL dopé P", **IT)
    f.text(819, 458, "CRISTAL dopé N", **IT)


@figure("c064_3#0")
def jonction_pn(f):
    f.text(8, 68, "+", size=S)
    f.text(395, 92, "–", size=S)
    f.line((4, 89.5), (69, 89.5), w=2.4)
    f.rect(69, 67, 133, 45, lw=3)
    f.line((136, 67), (136, 112), w=3)
    f.text(102, 101, "P", size=S, anchor="c")
    f.text(169, 101, "N", size=S, anchor="c")
    f.line((202, 89.5), (379, 89.5), w=2.4)
    f.line((302, 78), (326, 89.5), (302, 101), stroke=BLUE, w=2.6)
    f.text(285, 27, "sens conventionnel", size=S, anchor="c")
    f.text(285, 62, "du courant", size=S, anchor="c")
    f.line((26, 155.5), (128, 155.5), w=2.4)
    f.poly((128, 140), (128, 171), (157, 155.5), stroke=None, fill=BLACK)
    f.line((158, 134), (158, 177), w=3)
    f.line((158, 155.5), (268, 155.5), w=2.4)
    f.text(29, 208, "Anode", size=S)
    f.text(184, 208, "Cathode", size=S)
    f.arrow(235, 226, 85, 226, stroke=BLUE, w=2.6, size=18, open_=True)
    f.text(30, 266, "0,65 V (Si) ou 0,3 V (Ge)", size=S)
    f.line((9, 353.5), (36, 353.5), w=2.4)
    f.rect(36.5, 326.5, 111, 55, fill="#c0c0c0", lw=4)
    f.rect(115, 328, 8, 52, stroke=None, fill="#ffffff")
    f.line((148, 353.5), (174, 353.5), w=2.4)
    f.line((230, 354), (258, 354), w=2.4)
    f.rect(258, 326.5, 47, 55, fill="#c0c0c0", lw=2)
    f.rect(305, 300, 13, 110, stroke=None, fill="#c0c0c0")
    for k in range(9):
        x0 = 318 + k * 7
        f.line((x0, 382), (min(368, x0 + 56), 382 - (min(368, x0 + 56) - x0)), w=2.6, cap=None)
    for k in range(1, 8):
        y0 = 382 - k * 7
        f.line((318, y0), (318 + (y0 - 326), 326), w=2.6, cap=None)


from .t03_transfo import vcoil  # noqa: E402

W = 2.4


def diode_r(f, x0, x1, y, h=13.5, bar=None):
    """Diode pointing right: triangle from x0 to x1, bar at x1."""
    f.poly((x0, y - h), (x0, y + h), (x1, y), stroke=None, fill=BLACK)
    f.line((x1, y - h - 1.5), (x1, y + h + 1.5), w=bar or 2.2, cap=None)


def charge_box(f, x0, y0, x1, y1, size=26):
    f.rect(x0, y0, x1 - x0, y1 - y0, lw=2.4)
    f.text((x0 + x1) / 2, (y0 + y1) / 2, "Charge", size=size, rot=-90, anchor="c", va="middle")


def gnd(f, x0, y0, x1, y1):
    f.rect(x0, y0, x1 - x0, y1 - y0, stroke=None, fill=BLACK)


def zener_up(f, x, y_bar, y_base, half, hook):
    """Zener pointing up (cathode bar at the top) with a 'Z' hook."""
    f.poly((x - half, y_base), (x + half, y_base), (x, y_bar), stroke=None, fill=BLACK)
    hook(f)


@figure("c065_1#0")
def tableau_diodes(f):
    f.rect(1, 1, 1365, 710, lw=2.2)
    f.line((1, 38), (1366, 38), w=2)
    for x in (140.5, 597, 1008):
        f.line((x, 1), (x, 711), w=2)
    for x, a, b in ((71, "Diodes", "Fonctions"), (368, "Redressement", "Redresse le courant alternatif"),
                    (802, "Varicap", "condensateur à capacité variable"), (1187, "Zener", "stabilisateur de tension")):
        f.text(x, 30, a, size=S, anchor="c")
        f.text(x, 66, b, size=S, anchor="c")
    f.text(71, 350, "Schémas", size=S, anchor="c")
    # --- mono alternance
    vcoil(f, 226, 117, 192, 3, 25, side=-1)
    gnd(f, 244, 114, 249, 194)
    vcoil(f, 300, 113.5, 194.5, 3, 25, side=-1)
    f.line((300, 113.5), (350, 113.5), w=W)
    diode_r(f, 350, 380.5, 113.5)
    f.line((380, 113.5), (519, 113.5), (519, 119), w=W)
    f.line((300, 194.5), (350, 194.5), w=W)
    gnd(f, 348, 168, 358, 221)
    f.line((461.5, 113.5), (461.5, 140), w=W)
    gnd(f, 436, 139, 485, 142.5)
    gnd(f, 436, 166, 485, 169.5)
    f.line((461.5, 169), (461.5, 190), w=W)
    gnd(f, 436, 189, 485, 200)
    charge_box(f, 497, 119.5, 533, 195.5, size=22)
    f.line((515, 196), (515, 203), w=W)
    gnd(f, 498, 202, 540, 212)
    f.text(545, 172, "U_{s}", size=S)
    f.text(586, 241, "Mono alternance", size=S, anchor="r")
    # --- double alternance, centre tap
    vcoil(f, 226, 305, 402, 3, 25, side=-1)
    gnd(f, 244, 303, 249, 410)
    vcoil(f, 300, 303, 411, 4, 25, side=-1)
    f.line((300, 303), (352, 303), w=W)
    diode_r(f, 352, 384, 303)
    f.line((384, 303), (530, 303), (530, 319), w=W)
    f.line((300, 411), (353, 411), w=W)
    diode_r(f, 353, 384, 411)
    f.line((384, 411), (408.5, 411), (408.5, 303), w=W)
    f.line((300, 356.5), (322, 356.5), w=W)
    gnd(f, 321, 330, 333, 383)
    f.line((463, 303), (463, 329), w=W)
    gnd(f, 436, 328, 489, 331.5)
    gnd(f, 436, 355, 489, 358.5)
    f.line((461.5, 358), (461.5, 403), w=W)
    gnd(f, 432, 402, 485, 414)
    charge_box(f, 508, 320, 544, 395, size=22)
    f.line((529.5, 395), (529.5, 408), w=W)
    gnd(f, 509, 407, 551, 418)
    f.text(552, 360, "U_{S}", size=S)
    f.text(370, 452, "Double alternance avec point milieu", size=S, anchor="c")
    # --- bridge
    vcoil(f, 199, 520, 598, 3, 26, side=-1)
    gnd(f, 214, 518, 219, 598)
    f.line((270.5, 516), (270.5, 490), (393.5, 490), (393.5, 517), w=W)
    vcoil(f, 270, 516, 599, 3, 26, side=-1)
    f.line((268.5, 599), (268.5, 625), (393.5, 625), (393.5, 598.5), w=W)
    gnd(f, 290, 545, 302, 598)
    f.line((302, 571.5), (322.5, 571.5), w=W)
    f.line((322.5, 517), (322.5, 598.5), w=W)
    for y in (517, 598.5):
        f.line((322.5, y), (348, y), w=W)
        diode_r(f, 348, 376.5, y)
        f.line((376.5, y), (431, y), w=W)
        diode_r(f, 431, 459.5, y)
    f.line((459.5, 517), (561.5, 517), (561.5, 533), w=W)
    f.line((459.5, 598.5), (485.5, 598.5), (485.5, 517), w=W)
    f.line((512.5, 517), (512.5, 543), w=W)
    gnd(f, 493, 543, 539, 546.5)
    gnd(f, 495, 569, 539, 572.5)
    f.line((512.5, 572), (512.5, 593), w=W)
    gnd(f, 497, 592, 539, 604)
    charge_box(f, 544, 533.5, 579, 609.5, size=22)
    f.line((564.5, 610), (564.5, 622), w=W)
    gnd(f, 544, 621, 586, 632)
    f.text(552, 510, "U_{S}", size=S)
    f.text(405, 665, "Redressement double alternance", size=S, anchor="c")
    f.text(585, 700, "avec pont à 4 diodes", size=S, anchor="r")
    # --- varicap
    f.line((748, 295), (748, 142), (792, 142), w=W)
    _humps(f, 792, 899, 142, 4, 22, w=W)
    f.line((899, 142), (943, 142), (943, 207), (857, 207), w=W)
    f.line((943, 164), (982, 164), w=W)
    gnd(f, 981, 143, 991, 185)
    f.text(817, 108, "L", size=S)
    f.line((748, 207), (834.5, 207), w=W)
    gnd(f, 833, 186, 836.5, 228)
    gnd(f, 855, 186, 858.5, 228)
    f.text(862, 198, "C", size=S)
    gnd(f, 727, 292, 769, 295.5)
    gnd(f, 727, 313.5, 769, 317)
    f.line((748, 317), (748, 401), w=W)
    f.text(700, 286, "Ci", size=S)
    f.line((748, 337), (834.5, 337), w=W)
    gnd(f, 833, 316, 836.5, 358)
    gnd(f, 855, 315, 858.5, 358)
    f.poly((884, 323), (884, 351), (858.5, 337), stroke=None, fill=BLACK)
    f.line((884, 337), (916, 337), w=W)
    gnd(f, 915, 315, 926, 358)
    f.text(817, 306, "Varicap", size=S)
    f.text(791, 430, "Tension de commande", size=S, anchor="c")
    f.text(791, 465, "du circuit", size=S, anchor="c")
    for i, t in enumerate(["La fréquence du circuit LC", "varie en fonction de la tension", "d'alimentation de la diode",
                           "Varicap. La tension de", "commande est isolée par Ci. La", "diode est montée en inverse."]):
        f.text(802, 525 + i * 35.3, t, size=S, anchor="c")
    # --- zener
    f.text(1090, 165, "U", size=S)
    f.line((1090, 174.5), (1133, 174.5), w=W)
    f.rect(1133, 153, 65, 43, lw=2.4)
    f.text(1165, 186, "Rz", size=S, anchor="c")
    f.line((1198, 174.5), (1305.5, 174.5), (1305.5, 216), w=W)
    f.text(1223, 163, "U_{z}", size=S)
    f.line((1220, 174.5), (1220, 261), w=W)
    f.line((1198, 261), (1241, 261), (1220, 284), w=2.6)
    f.poly((1205, 312), (1235, 312), (1220, 283), stroke=None, fill=BLACK)
    f.line((1220, 312), (1220, 364), w=W)
    gnd(f, 1198, 363, 1241, 374)
    f.text(1127, 289, "Zener", size=S)
    charge_box(f, 1285, 216.5, 1345, 316.5, size=27)
    f.line((1305.5, 317), (1305.5, 364), w=W)
    gnd(f, 1285, 363, 1327, 374)
    for i, t in enumerate(["La diode Zener est une", "soupape qui stabilise la", "tension U_{z} aux bornes de la",
                           "charge. Rz, calculée selon", "l’intensité consommée par", "la charge, soulage la diode",
                           "Zener. La diode est montée", "en inverse."]):
        f.text(1187, 453 + i * 35.4, t, size=S, anchor="c")


PURPLE_D = "#7030a0"


@figure("c065_2#0")
def recombinaison(f):
    f.rect(330, 9, 188, 185, stroke=None, fill="#a6a6a6")
    f.rect(58.5, 6, 712, 190.5, lw=6)
    f.line((428, 6), (428, 196), w=6)
    f.line((7, 111.5), (58, 111.5), w=5)
    f.line((770, 111.5), (848, 111.5), w=5)
    f.text(423, 36, "Recombinaison", size=S, italic=True, color="#ffffff", anchor="c")
    f.arrow(353, 62, 497, 62, stroke=PURPLE_D, w=4, size=20, both=True)
    for x, y in ((100, 61), (269, 61), (327, 66), (186, 126), (290, 147)):
        f.circle(x, y, 10.5, stroke=BLUE, lw=2.6)
    for x, y in ((518, 66), (712, 60), (649, 82), (564, 147), (712, 147)):
        f.circle(x, y, 11.5, stroke=None, fill=RED)
    f.text(133, 57, "zone P", **IT)
    f.text(578, 57, "zone N", **IT)
    f.arrow(127, 212, 101, 76, stroke=BLUE, w=2.4, size=16)
    f.arrow(127, 212, 177, 136, stroke=BLUE, w=2.4, size=16)
    f.text(133, 232, "Trous", **IT)
    f.arrow(401, 212, 401, 128, stroke=BLUE, w=2.4, size=16)
    f.text(277, 232, "Barrière de Potentiel", **IT)
    f.arrow(662, 216, 650, 95, stroke=RED, w=2.4, size=16)
    f.arrow(662, 216, 702, 158, stroke=RED, w=2.4, size=16)
    f.text(584, 232, "Electrons libres", **IT)


@figure("c065_3#0")
def symboles_zener(f):
    f.line((24, 7), (24, 114), w=2.4)
    f.line((7, 74), (14, 60), (38, 60), (40, 47), w=2.4)
    f.poly((10, 91), (38, 91), (24, 60), stroke=None, fill=BLACK)
    f.line((104, 7), (104, 41), w=2.4)
    f.line((92, 40), (115, 42), (104, 62), w=2.4)
    f.poly((90, 91), (118, 91), (104, 61), stroke=None, fill=BLACK)
    f.line((104, 91), (104, 114), w=2.4)
    f.text(64, 152, "Zener", size=S, anchor="c")


def arches(f, xs, base, top, stroke=BLACK, w=2, dash=None):
    for a, b in zip(xs, xs[1:]):
        f.curve(lambda x, a=a, b=b: base - (base - top) * math.sin(math.pi * (x - a) / (b - a)), a, b, n=40,
                stroke=stroke, w=w, dash=dash)


@figure("c066_1#0")
def redressement_tableau(f):
    s = 31
    for y in (14.5, 50.5, 259):
        f.line((7.5, y), (1353.5, y), w=2.2)
    for x in (7.5, 174.5, 566.5, 958.5, 1353.5):
        f.line((x, 14.5), (x, 259), w=2.2)
    for x, t in ((91, "Eléments"), (370, "Redressement par un Pont"), (762, "Chute de tension des diodes"),
                 (1155, "Lissage du condensateur")):
        f.text(x, 41, t, size=s, anchor="c")
    f.text(91, 76, "Forme du", size=s, anchor="c")
    f.text(91, 112, "courant", size=s, anchor="c")
    f.text(91, 252, "Calcul", size=s, anchor="c")
    # bridge rectification
    xs = [219, 260, 301, 345, 386, 431]
    for i, (a, b) in enumerate(zip(xs, xs[1:])):
        red = i % 2 == 0
        arches(f, [a, b], 170.5, 63, stroke="#ff8080" if red else BLUE, w=2, dash=[3, 2] if red else None)
    f.arrow(196, 171, 490, 171, w=2.4, size=16)
    f.text(497, 160, "T", size=s)
    f.text(237, 114, "2", size=s, color=RED)
    f.text(279, 114, "1", size=s, color=BLUE)
    f.text(320, 114, "2", size=s, color=RED)
    f.text(370, 218, "Alternance 2 redressée", size=s, anchor="c")
    f.text(370, 252, "U_{s} ne change pas", size=s, anchor="c")
    # diode drop
    arches(f, [683, 724, 767, 809, 852], 151, 63, w=2)
    f.arrow(663, 173, 892, 173, w=2.4, size=16)
    f.text(613, 162, "1,4V", size=s)
    f.text(897, 160, "T", size=s)
    f.text(762, 218, "Passage dans 2 diodes", size=s, anchor="c")
    f.text(762, 252, "Chute de 2 x 0,7 V", size=s, anchor="c")
    # smoothing
    arches(f, [1001, 1043, 1085, 1127, 1170], 150, 65, stroke=GREY, w=1.6, dash=[2, 3])
    f.line((1004, 149), (1006, 110), (1015, 70), (1025, 65), (1169, 65), stroke=RED, w=6, cap=None)
    f.arrow(981, 170.5, 1253, 170.5, w=2.4, size=16)
    f.text(1263, 160, "T", size=s)
    f.text(1170, 91, "Umax - chute", size=s)
    f.text(1170, 124, "des diodes", size=s)
    f.text(1155, 218, "Filtrage", size=s, anchor="c")
    f.text(1155, 252, "U_{s} = (U x 1,414) - (2 x 0,7 V)", size=s, anchor="c")


def bridge(f, xl, xr, yt, yb, xd, xbars, xmid_top, label_x, label_y):
    f.line((xl, yt), (xr, yt), w=W)
    f.line((xl, yb), (xr, yb), w=W)
    f.line((xl, yt), (xl, yb), w=W)
    f.line((xr, yt), (xr, yb), w=W)
    for (x0, x1) in zip(xd, xbars):
        diode_r(f, x0, x1, yt, h=14)
        diode_r(f, x0, x1, yb, h=14)
    f.text(label_x, label_y, "Pont", size=S, italic=True, anchor="c")


def polar_cap(f, x, top_plate, plate_h, half, bx0, bx1, by0, by1):
    f.rect(x - half, top_plate, 2 * half, plate_h, stroke=None, fill=BLACK)
    f.line((bx0, by0), (bx0, by1), (bx1, by1), (bx1, by0), w=W)


@figure("c066_2#0")
def alimentations(f):
    it = dict(size=S, italic=True)
    # --- simple supply
    vcoil(f, 37, 42, 132, 3, 27, side=-1)
    gnd(f, 60, 46, 64, 127)
    vcoil(f, 112, 45, 130, 3, 27, side=-1)
    f.line((112, 45), (132, 37), (134, 7), (265, 7), (265, 51), w=W)
    f.line((112, 130), (134, 135), (135, 182), (265, 182), (265, 138.5), w=W)
    bridge(f, 200, 330.5, 51, 138.5, (214, 279), (244, 309), 265, 264, 105)
    gnd(f, 156, 73, 162, 116)
    f.line((159, 95), (200, 95), w=W)
    f.line((330.5, 94), (357.5, 94), (357.5, 7.5), (684, 7.5), w=W)
    f.line((439.5, 7.5), (439.5, 88), w=W)
    polar_cap(f, 444.5, 88, 12, 21.5, 407.5, 476.5, 88, 113)
    f.line((439.5, 113), (439.5, 155), w=W)
    gnd(f, 408, 154, 461, 164)
    f.text(344, 145, "filtrage", **it)
    f.rect(516.5, 22.5, 103, 108, lw=2.4)
    f.line((568, 7.5), (568, 22.5), w=W)
    f.line((571.5, 130.5), (571.5, 150), w=W)
    gnd(f, 540, 149, 594, 161)
    f.text(555, 77, "Stabili-", rot=-90, anchor="c", va="middle", **it)
    f.text(590, 77, "sateur", rot=-90, anchor="c", va="middle", **it)
    f.rect(653.5, 23.5, 54, 104, lw=2.4)
    f.line((683.5, 7.5), (683.5, 23.5), w=W)
    f.line((683.5, 127.5), (683.5, 154), w=W)
    gnd(f, 652, 153, 705, 165)
    f.text(680, 75, "Charge", rot=-90, anchor="c", va="middle", **it)
    # --- regulated supply
    vcoil(f, 783, 55, 140, 3, 27, side=-1)
    gnd(f, 789, 58, 794, 138)
    vcoil(f, 840, 57, 138, 3, 27, side=-1)
    f.line((840, 57), (866, 50), (867, 18), (998, 18), (998, 62), w=W)
    f.line((840, 138), (866, 155), (867, 193), (998, 193), (998, 149.5), w=W)
    bridge(f, 933, 1063, 62, 149.5, (947, 1012), (976, 1041), 998, 995, 116)
    gnd(f, 886, 84, 895, 128)
    f.line((890, 106), (933, 106), w=W)
    f.line((1063, 98), (1145, 98), w=W)
    f.line((1145, 49), (1145, 121), w=W)
    f.line((1145, 49), (1171, 49), w=W)
    polar_cap(f, 1144.5, 121, 13, 26.5, 1106.5, 1180.5, 112, 147)
    f.line((1145, 147), (1145, 176), w=W)
    gnd(f, 1123, 175, 1176, 186)
    f.rect(1171.5, 18.5, 190, 82, lw=2.4)
    f.text(1266, 58, "Régulateur", anchor="c", **it)
    f.line((1252.5, 101), (1252.5, 130), w=W)
    f.text(1283, 152, "Tension de", anchor="c", **it)
    f.text(1285, 188, "référence", anchor="c", **it)
    f.line((1362, 46), (1416, 46), (1416, 62), w=W)
    f.rect(1388.5, 62.5, 54, 118, lw=2.4)
    f.text(1414, 121, "Charge", rot=-90, anchor="c", va="middle", **it)
    f.line((1416, 181), (1416, 188), w=W)
    gnd(f, 1389, 187, 1442, 199)


@figure("c066_3#0")
def commutation_diode(f):
    w = W
    f.line((6, 27.5), (29.5, 27.5), w=w)
    gnd(f, 28, 4, 31, 51)
    gnd(f, 53, 4, 56, 51)
    f.line((55, 27.5), (125, 27.5), w=w)
    f.poly((125, 14), (125, 41), (150, 27.5), stroke=None, fill=BLACK)
    gnd(f, 150, 4, 153, 51)
    f.line((152, 27.5), (224, 27.5), w=w)
    gnd(f, 223, 4, 226, 51)
    gnd(f, 247, 4, 250, 51)
    f.line((249, 27.5), (273, 27.5), w=w)
    f.line((102.5, 27.5), (102.5, 76), w=w)
    f.rect(78.5, 76.5, 49, 49, lw=2.2)
    f.line((102.5, 126), (102.5, 149.5), (55, 149.5), w=w)
    f.line((32, 149.5), (52, 128), w=w)
    f.line((6, 149.5), (32, 149.5), w=w)
    f.text(2, 141, "+", size=26)
    f.line((200.5, 27.5), (200.5, 76), w=w)
    f.rect(175.5, 76.5, 49, 49, lw=2.2)
    f.line((200.5, 126), (200.5, 145), w=w)
    gnd(f, 176, 144, 224, 155)
    f.text(2, 53, "E", size=28, color=RED)
    f.text(267, 57, "S", size=28, color=RED)


@figure("c066_4#0")
def led(f):
    f.rect(29.5, 21.5, 132, 59, lw=2.2)
    f.text(95, 62, "500 Ω", size=29, italic=True, anchor="c")
    f.line((3, 53.5), (29.5, 53.5), w=W)
    f.line((161.5, 54), (247, 54), w=W)
    f.poly((187, 40), (187, 68), (212, 54), stroke=None, fill=BLACK)
    gnd(f, 212, 28, 216, 80)
    gnd(f, 235, 28, 247, 80)
    f.arrow(190, 27, 210, 5, stroke=RED, w=1.8, size=10, open_=True)
    f.arrow(207, 27, 227, 5, stroke=RED, w=1.8, size=10, open_=True)
    f.text(1, 105, "+ 12 V", size=29, italic=True)
    f.text(182, 108, "LED", size=29)
