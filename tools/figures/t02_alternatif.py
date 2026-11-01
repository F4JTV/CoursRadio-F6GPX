"""Chapter 2 (alternating currents, coils and capacitors) figures."""
import math

from figdsl import BLACK, RED, figure

BLUE = "#0000ff"
LBLUE = "#4f4fff"
NAVY = "#000080"
GREEN = "#008000"
DGREEN = "#00a000"
GREY = "#808080"
S = 28


@figure("c045_1#0")
def formes_signaux(f):
    f.text(9, 46, "0 V", size=S)
    f.line((65, 33), (1306, 33), stroke=GREY, w=2.4, dash=[2, 4])
    f.line((1296, 27), (1306, 33), (1296, 39), stroke=GREY, w=2)
    f.text(1321, 36, "T", size=S)
    f.line((90, 7.5), (145, 7.5), (145, 59.5), (196.5, 59.5), (196.5, 7.5), (250.5, 7.5), (250.5, 59.5),
           (302.5, 59.5), (302.5, 7.5), (356.5, 7.5), (356.5, 59), stroke=RED, w=2.2, cap=None)
    f.line((356, 60), (408, 7), (462, 60), (514, 7), (567, 60), (620, 7), (673, 60), stroke=LBLUE, w=1.6)
    pts = []
    xs = [673 + 53 * k for k in range(6)]
    for a, b in zip(xs, xs[1:]):
        pts += [(a, 60), (a, 7), (b, 60)]
    f.line(pts, stroke=GREEN, w=1.6)
    f.line((938, 60), (938, 7.5), (965.5, 7.5), (965.5, 32.5), (1044.5, 32.5), (1044.5, 7.5), (1071.5, 7.5),
           (1071.5, 32.5), (1150.5, 32.5), (1150.5, 7.5), (1177.5, 7.5), (1177.5, 32.5), (1257, 32.5), w=2.2, cap=None)
    for x, s in ((156, "Signal carré"), (410, "Signal triangulaire"), (696, "Signal dents de scie"),
                 (985, "Signal impulsionnel")):
        f.text(x, 98, s, size=S)


@figure("c045_2#0")
def superposition(f):
    f.text(16, 80, "0 V", size=S)
    f.arrow(60, 76, 1282, 76, stroke=GREY, w=2.4, size=14, open_=True)
    f.text(1270, 55, "T", size=S)
    f.line((214, 41), (560, 41), stroke=GREY, w=1.4)
    f.line((214, 5.5), (268.5, 5.5), (268.5, 60), (320.5, 60), (320.5, 5.5), (374.5, 5.5), (374.5, 60),
           (426.5, 60), (426.5, 5.5), (480.5, 5.5), (480.5, 60), (533, 60), w=2.2, cap=None)
    f.arrow(180, 118, 213, 44, stroke=BLUE, w=2.4, size=16)
    f.arrow(401.5, 122, 401.5, 59, stroke=BLUE, w=2.4, size=16)
    pts = [(745, 131)]
    for x in (797, 903, 1009):
        pts += [(x, 77), (x, 23), (x + 52, 77), (x + 52, 131)]
    pts.append((1115, 77))
    f.line(pts, w=1.6)
    f.text(5, 154, "Composante continue", size=S)
    f.text(311, 154, "Composante carrée", size=S)
    f.text(624, 154, "Superposition de composantes Carré et Triangle", size=S)


@figure("c045_3#0")
def sinusoide(f):
    yc, amp = 175.5, 141.5
    top, bot = yc - amp, yc + amp
    period, x0 = 260.0, 420.0

    def sine(x):
        return yc - amp * math.sin(2 * math.pi * (x - x0) / period)

    # hatched area (S = 2πf) and grey area (s = 1)
    f.rect(945, top, 455, yc - top, stroke=None, fill="#f2f2f2")
    for k in range(-12, 40):
        xa = 945 + k * 13
        a = (max(945, xa), yc - (max(945, xa) - xa))
        b = (min(1400, xa + (yc - top)), yc - (min(1400, xa + (yc - top)) - xa))
        if a[0] < b[0]:
            f.line(a, b, stroke="#c8c8c8", w=3, cap=None)
    q = x0 + 2 * period
    pts = [(q, yc)] + [(q + i * 65 / 30, sine(q + i * 65 / 30)) for i in range(31)] + [(q + 65, yc)]
    f.poly(pts, stroke=None, fill=GREY)
    # amplitude lines
    f.line((45, top), (1400, top), stroke=BLUE, w=1.4)
    f.line((216, bot), (1400, bot), stroke=BLUE, w=1.4)
    f.arrow(47.5, 174, 47.5, 37, stroke=BLUE, w=2, size=12, open_=True, both=True)
    f.text(52, 104, "1", size=S)
    # trigonometric circle
    f.circle(216.5, yc, 149, lw=2)
    f.line((216.5, 26), (216.5, 325), w=2)
    f.arrow(67, yc, 1228, yc, w=2.2, size=16, open_=True)
    f.text(1236, 172, "T", size=S)
    f.arrow(216.5, yc, 316, 82, stroke=DGREEN, w=2.4, size=14, dash=[6, 3])
    f.circle(321, 78, 9, stroke=None, fill=GREY)
    f.line((330, 78), (712, 78), stroke=DGREEN, w=1.6, dash=[8, 4, 2, 4])
    f.line((713, 78), (713, yc), stroke=DGREEN, w=1.6, dash=[8, 4, 2, 4])
    f.circle(713, 78, 9, stroke=None, fill=GREEN)
    f.arc(300, 115, 70, 70, 50, -60, stroke=DGREEN, w=6)
    f.head(306, 44, 200, size=26, stroke=DGREEN)
    # sine and its marks
    f.curve(sine, x0, 1200, n=400, stroke=RED, w=2)
    f.line((487, 37), (487, 70), stroke=BLUE, w=1.4)
    f.line((543.5, 34), (543.5, 410), stroke=BLUE, w=1.6)
    for x in (681, 811, 942):
        f.line((x, 30), (x, 410), stroke=BLUE, w=1.6, dash=[2, 3])
    f.arrow(812, 53, 941, 53, stroke=BLUE, w=2, size=14, both=True)
    f.arrow(682, 270.5, 942, 270.5, stroke=BLUE, w=2, size=14, both=True)
    f.arrow(945, 17.5, 1202, 17.5, stroke=BLUE, w=2, size=14, both=True)
    f.arrow(945, 190, 1398, 190, stroke=BLUE, w=2, size=14, both=True, dash=[8, 5])
    f.arrow(1095, 85, 1015, 140, w=2, size=16)
    # labels
    f.text(216, 22, "π/2 ou + 90°", size=S, anchor="c")
    f.text(10, 160, "π", size=S)
    f.text(10, 195, "ou", size=S)
    f.text(11, 229, "180°", size=S)
    f.text(196, 205, "O", size=S)
    f.text(232, 207, "Cosinus", size=S, italic=True)
    f.text(207, 82, "Sinus", size=S, italic=True, rot=-90, anchor="c")
    f.text(224, 136, "Vecteur", size=S, bold=True, color=GREEN)
    f.text(274, 85, "M", size=S)
    f.text(344, 167, "0 ou", size=S)
    f.text(370, 201, "2π", size=S)
    f.text(216, 357, "3π/2", size=S, anchor="c")
    f.text(216, 392, "ou +270° ou – 90°", size=S, anchor="c")
    f.text(482, 22, "π/2", size=S, anchor="c")
    f.text(688, 22, "0 ou 2π", size=S, anchor="c")
    f.text(435, 357, "0 ou 2π", size=S, anchor="c")
    f.text(536, 357, "π", size=S, anchor="c")
    f.text(616, 357, "3π/2", size=S, anchor="c")
    f.text(1073, 8, "2π", size=S, anchor="c")
    f.text(810, 104, "Alternance", size=S)
    f.text(701, 255, "Période", size=S)
    f.text(1079, 90, "surface grisée (s) = 1", size=S, italic=True)
    f.text(1064, 135, "surface hachurée (S) = 2πf", size=S, italic=True)
    f.text(1203, 218, "t = 1 seconde", size=S, italic=True)
    f.text(805, 368, "t(s) = 1 / f(Hz)", size=S, bold=True, color=NAVY, anchor="c")
    f.text(805, 402, "ou f(Hz) = 1 / t(s)", size=S, bold=True, color=NAVY, anchor="c")
    f.text(1137, 368, "ω (rad/s) = 2π . f(Hz)", size=S, bold=True, color=NAVY, anchor="c")
    f.text(1137, 402, "= 6,28 x f(Hz)", size=S, bold=True, color=NAVY, anchor="c")


TEAL = "#008080"
MAROON = "#800000"
PALEBLUE = "#5a5aff"


def vhead(f, x, y, up, color=BLUE, size=12, w=2.4):
    d = -1 if up else 1
    f.line((x - size * 0.6, y - d * size), (x, y), (x + size * 0.6, y - d * size), stroke=color, w=w)


def vline_arrow(f, x, y0, y1, both=False, color=BLUE, w=2.4):
    """Vertical arrow from y0 to y1 with an open head at y1."""
    f.line((x, y0), (x, y1), stroke=color, w=w)
    vhead(f, x, y1, y1 < y0, color, w=w)
    if both:
        vhead(f, x, y0, y0 < y1, color, w=w)


@figure("c046_1#0")
def valeurs_efficaces(f):
    f.text(730, 33, "Ucàc = 2.Umax = 2√2.Ueff", size=30, bold=True, color=NAVY, anchor="c")
    f.circle(143, 211, 136, lw=2.6)
    f.line((8, 212), (1215, 212), w=3)
    f.line((143, 212), (249, 126), w=1.4)
    f.text(190, 197, "45°", size=S)
    f.line((278, 75), (1215, 75), stroke=BLUE, w=2, dash=[2, 3])
    f.line((278, 349), (1240, 349), stroke=BLUE, w=2, dash=[2, 3])
    f.line((249, 126), (990, 126), stroke=TEAL, w=3)
    f.curve(lambda x: 212 - 137 * math.sin(2 * math.pi * (x - 371) / 128.5), 363, 887, n=300, stroke=RED, w=2)
    vline_arrow(f, 858, 126, 210, both=True)
    vline_arrow(f, 902.5, 126, 76)
    vline_arrow(f, 986.5, 76, 125)
    vline_arrow(f, 1148.5, 75, 343, both=True)
    vline_arrow(f, 1193, 77, 209, both=True)
    f.text(867, 172, "Ueff", size=S)
    f.text(813, 70, "x 1,414", size=S)
    f.text(982, 152, "x 0,707", size=S)
    f.text(1219, 150, "Umax", size=S)
    f.text(1246, 218, "Umoy (= 0)", size=S)
    f.text(1175, 305, "Ucàc = 2 x Umax", size=S)


def _chev(f, x, y, color=PALEBLUE):
    f.line((x - 18, y - 10), (x, y), (x - 18, y + 10), stroke=color, w=2.4)


@figure("c046_1#1")
def exemples_efficaces(f):
    k = dict(size=25, family="sans")
    f.text(7, 25, "Exemples :", size=25, family="sans", bold=True, underline=True, color=MAROON)
    for y, s in ((56, "Ieff = Imax x 0,707"), (87, "Ieff = 1A max x 0,707"), (122, "Ieff = 0,707 Aeff"),
                 (151, "U = R . I")):
        f.text(94, y, s, **k)
    f.text(94, 186, "U = 50 x 0,707 = ", **k)
    f.text(301, 186, "35,35 V", color=MAROON, **k)
    f.text(394, 26, "Ueff = ?", bold=True, **k)
    f.arrow(493, 41, 365, 41, stroke=PALEBLUE, w=3, size=12)
    f.text(545, 29, "1)", bold=True, **k)
    f.rect(391, 67, 87, 44, lw=4)
    f.text(435, 100, "50 Ω", anchor="c", **k)
    f.line((369, 95.5), (391, 95.5), w=2)
    f.line((478, 95.5), (636, 95.5), w=2)
    _chev(f, 549, 95.5)
    f.text(505, 131, "I = 1 Amax", **k)
    f.line((691, 1), (691, 186), stroke=GREY, w=1.4)
    for y, s in ((56, "P = Ueff . Ieff"), (87, "Ueff = Umax x 0,707"), (122, "Ueff = 14 x 0,707 ≈ 10 Veff"),
                 (151, "P = 10 V x 2 A")):
        f.text(738, y, s, **k)
    f.text(738, 184, "P = ", **k)
    f.text(785, 184, "20 W", color=MAROON, **k)
    f.text(1081, 29, "2)", bold=True, **k)
    f.text(1216, 41, "P = ?", bold=True, **k)
    f.rect(1211, 67, 86, 44, lw=4)
    f.text(1254, 100, "R", anchor="c", **k)
    f.line((1168, 95.5), (1211, 95.5), w=2)
    f.line((1297, 95.5), (1433, 95.5), w=2)
    _chev(f, 1342, 95.5)
    f.text(1324, 70, "2 Aeff", **k)
    f.arrow(1318, 141.5, 1185, 141.5, stroke=BLUE, w=2.4, size=12)
    f.text(1209, 170, "14 Vmax", **k)


@figure("c046_2#0")
def tension_continue_superposee(f):
    f.line((55.5, 179), (55.5, 22), w=2)
    f.poly((50, 24), (61, 24), (55.5, 8), stroke=None, fill=BLACK)
    f.arrow(54, 125, 270, 125, w=2, size=14)
    f.line((56, 36), (275, 36), stroke=BLUE, w=2, dash=[2, 2])
    f.line((55, 161), (280, 161), stroke=BLUE, w=2, dash=[2, 2])
    f.curve(lambda x: 100 - 59 * math.sin(2 * math.pi * (x - 72.75) / 85), 67, 243, n=160, stroke=RED, w=2)
    f.text(3, 48, "4 V", size=S, italic=True)
    f.text(0, 156, "-1 V", size=S, italic=True)
    f.text(287, 137, "T", size=S, italic=True)
    f.text(215, 70, "Ueff = ?", size=25, family="sans", bold=True, italic=True)


@figure("c047_2#0")
def oscilloscope(f):
    for x in (71, 99, 127, 155):
        f.line((x, 5), (x, 143), w=1.4, dash=[2, 3])
    for y in (32, 60, 88, 116):
        f.line((44, y), (183, y), w=1.4, dash=[2, 3])
    f.curve(lambda x: 60 - 28 * math.cos(2 * math.pi * (x - 43) / 57), 44, 183, n=140, stroke=GREEN, w=2.6)
    f.rect(43.5, 4.5, 140, 139, stroke=BLUE, lw=2.6)
    f.text(30, 74, "5 V/div", size=S, rot=-90, anchor="c")
    f.text(113, 171, "2 ms/div", size=S, anchor="c")


B = {"b": 1}
BU = {"b": 1, "u": 1}
I_ = {"i": 1}
NB = {"b": 1, "color": NAVY}
NBU = {"b": 1, "u": 1, "color": NAVY}
NBI = {"b": 1, "i": 1, "color": NAVY}


def _humps(f, x0, x1, y, n, h, down=False, w=2):
    pts = []
    step = (x1 - x0) / n
    for k in range(n):
        for i in range(17):
            a = math.pi * i / 16
            pts.append((x0 + k * step + step / 2 - math.cos(a) * step / 2 * 1.08,
                        y + (1 if down else -1) * math.sin(a) * h))
    f.line(pts, w=w)


def _phase(f, x_axis0, x_axis1, red, blue):
    yc, amp, per = 1462, 76, 128.0
    f.arrow(x_axis0, 1463.5, x_axis1, 1463.5, stroke="#404040", w=3, size=16)
    f.curve(lambda x: yc - amp * math.sin(2 * math.pi * (x - red[2]) / per), red[0], red[1], n=200,
            stroke=RED, w=2.2)
    f.curve(lambda x: yc - amp * math.sin(2 * math.pi * (x - blue[2]) / per), blue[0], blue[1], n=200,
            stroke=PALEBLUE, w=2.2, dash=[1.5, 2.5])


@figure("c047_1#0")
def condensateur_bobine(f):
    s = 31
    W, H = 1365, 1560
    # grid
    f.rect(3, 3, W - 3, H - 3, lw=2.4)
    for y in (40, 905):
        f.line((3, y), (W, y), w=2.4)
    for x in (260, 812):
        f.line((x, 3), (x, H), w=2.4)
    f.text(36, 469, "Différenciation condensateurs / bobines", size=29, rot=-90, anchor="c", va="middle")
    f.text(36, 1229, "Complémentarité condensateurs / bobines", size=29, rot=-90, anchor="c", va="middle")
    c1, c2, c3 = 162, 536, 1090
    f.text(132, 30, "Caractéristiques", size=s, anchor="c")
    f.text(c2, 30, "Condensateur", size=s, anchor="c")
    f.text(c3, 30, "Bobine", size=s, anchor="c")
    # column 1
    col1 = [(66, "Origines du", {}), (99, "phénomène", {}), (205, "Schémas", BU), (324, "Unités", BU),
            (442, "Dimensions", BU), (596, "Calcul des", I_), (630, "valeurs avec", I_), (665, "les formules", I_),
            (700, "simplifiées", I_), (826, "Définitions", BU), (860, "physiques", BU), (937, "Fonctions", BU),
            (1007, "Impédance", BU), (1076, "formule", {}), (1111, "simplifiée", {}), (1167, "Groupement", BU),
            (1198, "Parallèle", {}), (1253, "Série", {}), (1340, "la tension aux", {}), (1375, "bornes par", {}),
            (1409, "rapport à", {}), (1444, "l’intensité", {}), (1478, "parcourue", {})]
    for y, t, st in col1:
        f.rich(c1, y, [(t, st)], size=s, anchor="c")
    f.rich(c1, 1305, [("Déphasage", BU), (" de", {})], size=s, anchor="c")
    f.text(100, 1513, "U =", size=s)
    f.line((165, 1503), (237, 1503), stroke=PALEBLUE, w=2.2)
    f.text(107, 1550, "I =", size=s)
    f.line((165, 1530), (245, 1530), stroke=RED, w=2.2)
    # column 2: capacitor
    f.text(c2, 84, "Effet électrostatique", size=s, anchor="c")
    f.line((313, 215), (368, 215), w=2)
    f.line((393, 215), (447, 215), w=2)
    f.line((368, 190), (368, 240), w=3)
    f.line((393, 190), (393, 240), w=3)
    f.arrow(342, 240, 418, 192, w=1.8, size=14, open_=True)
    f.line((473, 161), (528, 161), w=2)
    f.line((555, 161), (609, 161), w=2)
    f.line((528, 137), (528, 188), w=3)
    f.line((555, 137), (555, 188), w=3)
    f.line((635, 189), (679, 189), w=2)
    f.rect(679, 162, 19, 53, stroke=None, fill=BLACK)
    f.line((690, 133.5), (716, 133.5), (716, 240), (690, 240), w=3)
    f.line((716, 189), (769, 189), w=2)
    f.text(638, 222, "+", size=24, anchor="c", color=NAVY)
    f.text(743, 222, "–", size=24, anchor="c")
    f.text(262, 276, "condensateur variable", size=s)
    f.text(547, 276, "condensateur polarisé", size=s)
    f.rich(c2, 324, [("farad", BU), (" (F) µF, nF, pF", {})], size=s, anchor="c")
    f.rich(c2, 371, [("C = ε . S / E", NB)], size=s, anchor="c")
    f.rich(c2, 407, [("C = valeur du condensateur = ", {}), ("capacité", BU)], size=s, anchor="c")
    for y, t in ((444, "ε = constante diélectrique de l’isolant"), (478, "S = surfaces en vis à vis"),
                 (515, "E = épaisseur du diélectrique (isolant)")):
        f.text(c2, y, t, size=s, anchor="c")
    for y, t in ((582, "Formule avec diélectrique à air"), (616, "C(pF) = 8,85 . S (cm²) / E (¹/₁₀ mm)"),
                 (650, "Si le diélectrique n’est pas de l’air, il faut"),
                 (686, "multiplier le résultat par le coefficient du"), (721, "diélectrique (voir ci-après)")):
        f.text(c2, y, t, size=s, italic=True, anchor="c")
    f.rich(c2, 790, [("C(F) = Q(C) / U(V)", NB), (" ou ", {"color": NAVY}), ("Q = C . U", NB)], size=s, anchor="c")
    f.rich(c2, 827, [("E(J) =½ . Q(C) . U(V) = ½ . C(F) . U²(V)", NB)], size=s, anchor="c")
    f.text(c2, 860, "Q = électricité emmagasinée en Coulomb", size=s, anchor="c")
    f.text(c2, 896, "U= tension aux bornes de C ; E= énergie en J", size=s, anchor="c")
    f.rich(c2, 937, [("laisse passer les tensions alternatives", NBU)], size=s, anchor="c")
    f.rich(c2, 969, [("Capacitance", NBU), (" : Z_{C} = 1 / ωC", NB)], size=s, anchor="c")
    f.rich(362, 1005, [("Z(Ω) =", NB)], size=s)
    f.text(574, 1004, "1", size=s, bold=True, color=NAVY, anchor="c")
    f.line((455, 1010), (711, 1010), stroke=NAVY, w=2)
    f.text(586, 1042, "2 . π . f(Hz) . C(F)", size=s, bold=True, color=NAVY, anchor="c")
    f.text(c2, 1104, "Z(Ω) = 159 / f(MHz) / C(nF)", size=s, bold=True, color=NAVY, anchor="c")
    f.text(c2, 1165, "Inverse des résistances", size=s, anchor="c")
    f.text(c2, 1202, "C_{t} = C1 + C2", size=s, bold=True, color=NAVY, anchor="c")
    f.text(450, 1237, "C_{t} = ", size=s, bold=True, color=NAVY)
    f.text(567, 1237, "C1 . C2", size=s, bold=True, color=NAVY, anchor="c")
    f.line((513, 1243), (621, 1243), stroke=NAVY, w=2)
    f.text(567, 1272, "C1 + C2", size=s, bold=True, color=NAVY, anchor="c")
    f.rich(c2, 1340, [("U en retard", BU), (" de 90°", {})], size=s, anchor="c")
    _phase(f, 308, 715, (342, 620, 348), (385, 660, 391))
    f.text(725, 1472, "T", size=s)
    # column 3: coil
    f.text(c3, 84, "Effet électromagnétique", size=s, anchor="c")
    f.line((879, 135), (1029, 135), w=2)
    _humps(f, 1029, 1158, 135, 5, 20)
    f.line((1158, 135), (1309, 135), w=2)
    f.line((890, 189), (1040, 189), w=2)
    _humps(f, 1040, 1170, 189, 5, 23, down=True)
    f.line((1170, 189), (1320, 189), w=2)
    f.line((1027, 221), (1187, 221), w=5, dash=[15, 8])
    f.text(c3, 276, "Bobine à noyau", size=s, anchor="c")
    f.rich(c3, 324, [("henry", BU), (" (H) mH, µH, nH", {})], size=s, anchor="c")
    f.rich(c3, 373, [("L = F . N² . D²", NB)], size=s, anchor="c")
    f.rich(c3, 407, [("L = valeur de la bobine = ", {}), ("inductance", BU)], size=s, anchor="c")
    f.rich(c3, 441, [("F = Facteur de forme ", {}), ("(ou constante", I_)], size=s, anchor="c")
    f.rich(c3, 477, [("magnétique)", I_), (" ; N = nombre de spires ;", {})], size=s, anchor="c")
    f.text(c3, 511, "D = diamètre de la bobine", size=s, anchor="c")
    f.text(c3, 562, "Formule de Nagaoka simplifiée", size=s, italic=True, anchor="c")
    f.text(950, 597, "L =", size=s, italic=True)
    f.text(1063, 596, "N²", size=s, italic=True, anchor="c")
    f.text(1133, 596, "x", size=s, italic=True, anchor="c")
    f.text(1207, 596, "D²", size=s, italic=True, anchor="c")
    f.line((1012, 604), (1228, 604), w=2)
    f.text(1120, 631, "45 D + 100 long", size=s, italic=True, anchor="c")
    for y, t in ((668, "avec L en µH, N = nombre de spires, D ="), (702, "diamètre intérieur de la bobine (en cm),"),
                 (737, "long = longueur de la bobine (en cm)")):
        f.text(c3, y, t, size=s, italic=True, anchor="c")
    f.text(c3, 790, "L(H) = Φ(Wb) / I(A)", size=s, bold=True, italic=True, color=NAVY, anchor="c")
    f.text(c3, 827, "E(J) = ½ Φ(Wb) . I(A) = ½ L(H) . I²(A)", size=s, bold=True, italic=True, color=NAVY, anchor="c")
    f.text(c3, 860, "I = intensité parcourue ; E= énergie en J", size=s, italic=True, anchor="c")
    f.text(c3, 896, "Φ = flux généré par la bobine (en Weber)", size=s, italic=True, anchor="c")
    f.rich(c3, 937, [("s’oppose aux variations d’intensité", NBU)], size=s, anchor="c")
    f.rich(c3, 987, [("Réactance", NBU), (" : Z_{L} = ωL", NB)], size=s, anchor="c")
    f.text(c3, 1023, "Z(Ω) = 2 . π . f(Hz) . L(H)", size=s, bold=True, color=NAVY, anchor="c")
    f.text(c3, 1104, "Z(Ω) = 6,28 x f(MHz) x L(µH)", size=s, bold=True, color=NAVY, anchor="c")
    f.text(c3, 1165, "Comme pour les résistances", size=s, anchor="c")
    f.text(c3, 1201, "montage rarement utilisé", size=s, italic=True, anchor="c")
    f.text(c3, 1237, "L_{t} = L1 + L2 ± M", size=s, bold=True, color=NAVY, anchor="c")
    f.text(c3, 1271, "M est la mutuelle induction entre L1 et L2", size=s, anchor="c")
    f.rich(c3, 1340, [("U en avance", BU), (" de 90°", {})], size=s, anchor="c")
    _phase(f, 885, 1270, (952, 1228, 955), (910, 1185, 913))
    f.text(1285, 1472, "T", size=s)


@figure("c050_1#0")
def charge_condensateur(f):
    k = dict(size=28, family="sans")
    f.line((29, 4), (29, 59.5), w=2)
    f.line((2, 59.5), (56, 59.5), w=3.5)
    f.line((2, 87.5), (56, 87.5), w=3.5)
    f.line((29, 87.5), (29, 143), w=2)
    f.text(52, 42, "Q = 0,8 mC", **k)
    f.text(104, 82, "20 V", **k)
    f.arrow(84.5, 115, 84.5, 61, stroke=BLUE, w=3, size=16)
    f.circle(282, 114, 29, stroke=None, fill="#c8c8c8")
    f.poly((307, 4), (363, 143.5), (251, 143.5), stroke=BLUE, w=3)
    f.text(308, 58, "Q", size=26, family="sans", anchor="c")
    f.text(285, 108, "C", size=26, family="sans", anchor="c")
    f.text(329, 108, "U", size=26, family="sans", anchor="c")


@figure("c050_2#0")
def reactance_c(f):
    k = dict(size=28, family="sans")
    f.line((52, 56.5), (158, 56.5), w=2)
    f.line((185, 56.5), (250, 56.5), stroke=GREY, w=3)
    f.line((158, 36), (158, 87), w=4)
    f.line((185, 36), (185, 87), w=4)
    f.line((118, 50), (106, 56.5), (118, 63), stroke=BLUE, w=2.4)
    f.text(52, 41, "Ieff = ?", bold=True, **k)
    f.text(196, 43, "10 µF", **k)
    f.text(2, 99, "f = 15 kHz", **k)
    f.arrow(106, 122, 252, 122, stroke=BLUE, w=3, size=16)
    f.text(111, 153, "14 Vmax", **k)


@figure("c050_3#0")
def reactance_l(f):
    k = dict(size=28, family="sans")
    f.line((61, 44), (169, 44), w=2.4)
    _humps(f, 169, 274, 44, 4, 22, w=2.4)
    f.line((274, 44), (354, 44), w=2.4)
    f.text(296, 27, "Z = ?", bold=True, **k)
    f.text(5, 81, "f = 8 MHz", **k)
    f.text(174, 81, "12,5 µH", **k)


@figure("c051_3#0")
def condensateurs_parallele(f):
    k = dict(size=28, family="sans")
    f.line((32, 9), (254, 9), w=2.4)
    f.line((15, 66), (254, 66), w=2.4)
    for x in (120, 253.5):
        f.line((x, 9), (x, 28), w=2.4)
        f.line((x - 22, 28), (x + 22, 28), w=3.5)
        f.line((x - 22, 46.5), (x + 22, 46.5), w=3.5)
        f.line((x, 46.5), (x, 66), w=2.4)
    f.text(8, 41, "100 pF", **k)
    f.text(282, 49, "0,4 nF", **k)


@figure("c051_1#0")
def charge_decharge(f):
    s = 29
    # circuit
    f.text(49, 45, "Charge", size=s)
    f.text(176, 45, "Décharge", size=s)
    f.line((61, 70.5), (150, 70.5), stroke=RED, w=2.2)
    f.circle(150, 70.5, 8, stroke=None, fill=RED)
    f.line((191, 70.5), (280, 70.5), stroke=BLUE, w=2.2)
    f.circle(191, 70.5, 8, stroke=None, fill=BLUE)
    f.line((61, 70.5), (61, 166), w=2.2)
    f.line((61, 190), (61, 274.5), (279.5, 274.5), (279.5, 70.5), w=2.2)
    f.rect(35, 160, 52, 13, stroke=None, fill=BLACK)
    f.line((7, 190), (115, 190), w=3.6)
    f.text(10, 140, "E", size=s)
    f.text(99, 222, "+", size=s, anchor="c")
    f.text(66, 124, "U_{C}", size=s)
    f.arrow(117, 97, 117, 161, stroke=BLUE, w=3, size=16)
    f.line((170.5, 51), (170.5, 123.5), w=2.2)
    f.line((147, 123.5), (199, 123.5), w=4)
    f.line((147, 150), (199, 150), w=4)
    f.line((170.5, 150), (170.5, 165), w=2.2)
    f.rect(143.5, 166.5, 42, 89, lw=3)
    f.rect(149, 172, 31, 78, lw=1.4)
    f.line((164.5, 257), (164.5, 274.5), w=2.2)
    f.text(204, 155, "C", size=s)
    f.text(164, 229, "R", size=s, anchor="c")
    # curves
    f.arrow(361.5, 236, 361.5, 19, w=2, size=14)
    f.arrow(361.5, 236, 798, 236, w=2, size=14)
    f.text(383, 48, "U_{C}", size=s)
    f.text(780, 268, "T (s)", size=s)
    for y, lab, x1 in ((70, "E", 775), (124, "²/₃ E", 499), (177, "¹/₃ E", 499)):
        f.line((363, y), (x1, y), stroke="#505050", w=1.4)
        f.text(356, y + 7, lab, size=s, anchor="r")
    for x, lab in ((445, "1"), (581, "3"), (716, "5")):
        f.line((x, 206), (x, 238), w=2)
        f.rich(x, 270, [(lab + " ", {}), ("T", {"i": 1})], size=s, anchor="c")
    tau = 82.0
    f.curve(lambda x: 236 - 166 * (1 - math.exp(-(x - 363) / tau)), 363, 775, n=120, stroke=RED, w=2.2, dash=[7, 5])
    f.curve(lambda x: 70 + 166 * (1 - math.exp(-(x - 363) / tau)), 363, 775, n=120, stroke=BLUE, w=2.2, dash=[7, 5])
    f.line((363, 236), (445, 70), stroke=RED, w=1.6, dash=[2, 3])
    f.line((363, 70), (445, 236), stroke=BLUE, w=1.6, dash=[2, 3])
    f.text(640, 99, "Charge", size=s)
    f.text(640, 205, "Décharge", size=s)
    # time constant and table
    f.rich(1053, 37, [("T", {"b": 1, "i": 1}), ("(s) = R(Ω) . C(F)", {"b": 1}), (" ou ", {}), ("T", {"b": 1, "i": 1}),
                      ("(ms) = R(kΩ) . C(µF)", {"b": 1})], size=31, anchor="c", color=NAVY)
    f.text(860, 74, "Temps", size=s)
    f.text(1045, 74, "Charge", size=s, anchor="c")
    f.text(1261, 74, "Décharge", size=s, anchor="c")
    xs = [851, 916, 1045, 1153, 1259, 1346]
    ys = [83, 123.5, 163, 200.5, 239.5, 282.5]
    for x in xs[1:-1]:
        f.line((x, ys[0]), (x, ys[-1]), w=2.2)
    for y in ys[1:-1]:
        f.line((xs[0], y), (xs[-1], y), w=2.2)
    f.rect(xs[0], ys[0], xs[-1] - xs[0], ys[-1] - ys[0], lw=4)
    rows = [("1", "63,2%", "2/3", "36,8%", "1/3"), ("2", "86,5%", "8/9", "12,5%", "1/9"),
            ("3", "95,0%", "26/27", "5,0%", "1/27"), ("4", "98,2%", "80/81", "1,8%", "1/81"),
            ("5", "99,3%", "1", "0,7%", "0")]
    cx = [(a + b) / 2 for a, b in zip(xs, xs[1:])]
    for r, (n, *cells) in enumerate(rows):
        y = (ys[r] + ys[r + 1]) / 2 + 10
        f.rich(cx[0], y, [(n + " ", {}), ("T", {"i": 1})], size=s, anchor="c")
        for c, t in enumerate(cells):
            f.text(cx[c + 1], y, t, size=s, anchor="c")


def _dotted_box(f, x0, y0, x1, y1, label):
    f.rect(x0, y0, x1 - x0, y1 - y0, lw=2.4, dash=[2, 2.5])
    f.text((x0 + x1) / 2, (y0 + y1) / 2 + 10, label, size=29, italic=True, anchor="c")


@figure("c051_2#0")
def impedances_rl_rc(f):
    s = 29
    f.line((4, 45), (49, 45), w=2.4)
    _dotted_box(f, 49, 28, 113, 62, "R")
    f.line((113, 45), (202, 45), w=2.4)
    _humps(f, 202, 314, 45, 4, 22, w=2.4)
    f.line((314, 45), (424, 45), w=2.4)
    f.text(258, 76, "L", size=s, italic=True, anchor="c")
    f.text(133, 124, "Z =  √(R² + X_{L}²)", size=s, bold=True, italic=True, color=NAVY)
    f.line((530, 47), (692, 47), (692, 129), w=1.8, dash=[2, 3])
    f.arrow(530, 129.5, 692, 129.5, w=2.4, size=16)
    f.arrow(530, 129.5, 530, 46, w=2.4, size=16)
    f.arrow(530, 129.5, 692, 47, stroke=BLUE, w=2.4, size=16)
    f.text(466, 57, "X_{L}", size=s, italic=True)
    f.text(701, 52, "Z", size=s, italic=True)
    f.text(692, 118, "R", size=s, italic=True)
    f.text(507, 141, "O", size=s, italic=True)
    f.line((835, 39), (924, 39), w=2.4)
    _dotted_box(f, 924, 22, 989, 56, "R")
    f.line((989, 39), (1078.5, 39), w=2.4)
    f.line((1078.5, 17), (1078.5, 61), stroke="#003300", w=4)
    f.line((1100.5, 17), (1100.5, 61), stroke="#003300", w=4)
    f.line((1100.5, 39), (1167, 39), w=2.4)
    f.text(1052, 82, "C", size=s, italic=True, anchor="c")
    f.text(1162, 104, "X_{c}", size=s, italic=True)
    f.text(896, 124, "Z =  √(R² + X_{C}²)", size=s, bold=True, italic=True, color=NAVY)
    f.line((1222.5, 101), (1391, 101), (1391, 17.5), w=1.8, dash=[2, 3])
    f.arrow(1222.5, 17.5, 1391, 17.5, w=2.4, size=16)
    f.arrow(1222.5, 17.5, 1222.5, 101, w=2.4, size=16)
    f.arrow(1223, 17.5, 1386, 100, stroke=BLUE, w=2.4, size=16)
    f.text(1196, 32, "O", size=s, italic=True)
    f.text(1386, 31, "R", size=s, italic=True)
    f.text(1400, 112, "Z", size=s, italic=True)


@figure("c052_1#0")
def bobine_non_parfaite(f):
    s = 31
    it = dict(size=s, italic=True)
    f.line((0, 130), (66, 130), w=2.4)
    for x in (67, 86):
        f.line((x, 108), (x, 152), w=2.4, dash=[2, 2.5])
    f.line((86, 129.5), (109, 129.5), w=2.4)
    _dotted_box(f, 109, 108, 174, 152, "R")
    f.line((174, 129.5), (198, 129.5), w=2.4)
    _humps(f, 198, 306, 130, 4, 22, w=2.4)
    f.line((306, 130), (395, 130), w=2.4)
    f.text(80, 91, "C", **it)
    f.text(236, 84, "L", **it)
    f.text(76, 203, "Bobine non parfaite", size=s)
    # axes
    f.arrow(500, 158, 500, 10, stroke=GREEN, w=2.4, size=16)
    f.arrow(500, 158, 637, 158, stroke=BLUE, w=2.4, size=16)
    f.arrow(500, 160, 500, 239, stroke=RED, w=2.4, size=16)
    f.text(513, 24, "+X_{L}", **it)
    f.text(470, 102, "L", **it)
    f.text(474, 163, "O", **it)
    f.text(614, 134, "R", **it)
    f.text(470, 209, "C", **it)
    f.text(510, 244, "-X_{C}", **it)
    f.text(603, 203, "Représentation vectorielle", size=s)
    # impedance triangle
    f.arrow(971, 12.5, 1107, 12.5, w=2.4, size=16)
    f.text(911, 46, "résistance (R)", **it)
    f.text(1111, 35, "L", **it)
    f.line((970, 133), (1270, 133), w=2.6, dash=[2, 4])
    f.line((1260, 125), (1272, 133), (1260, 141), w=2.2)
    f.arrow(1191, 133, 1191, 51, w=2.4, size=16)
    f.text(1213, 85, "X_{L} réactance", **it)
    f.arrow(970, 133, 1105, 53, w=2.4, size=18)
    f.text(1014, 126, "φ", **it)
    f.text(744, 108, "Z(Ω) = longueur 0L", **it)
    f.text(936, 139, "O", **it)
    f.arrow(1106, 216, 1106, 53, stroke=GREEN, w=2.4, size=16)
    f.arrow(970, 135, 970, 214, stroke=RED, w=2.4, size=16)
    f.arrow(971, 216.5, 1106, 216.5, stroke=BLUE, w=2.4, size=16)
    f.text(948, 221, "C", **it)
    f.text(1111, 223, "R", **it)


@figure("c052_2#0")
def dephasage(f):
    s = 31
    it = dict(size=s, italic=True)
    # vector triangle
    f.line((41, 43), (195, 43), (195, 142), w=1.4)
    f.arrow(41, 142, 41, 36, w=2.4, size=16)
    f.arrow(41, 142, 200, 142, w=2.4, size=16)
    f.arrow(41, 142, 195, 43, stroke=BLUE, w=2.4, size=16)
    f.text(44, 24, "X_{L}", **it)
    f.text(117, 56, "80 Ω", **it)
    f.text(206, 50, "Z", **it)
    f.text(20, 91, "+ j 40 Ω", rot=-90, anchor="c", va="middle", **it)
    f.text(62, 131, "+30°", **it)
    f.text(174, 126, "R", **it)
    f.text(144, 175, "69 Ω", **it)
    # rotating vector
    f.circle(344, 129, 119, lw=2.2)
    f.line((344, 10), (344, 249), w=2.2)
    f.line((225, 129.5), (1333, 129.5), w=2.4)
    f.line((494, 129.5), (1084, 129.5), stroke="#a6a6a6", w=4)
    f.line((1322, 122), (1336, 129.5), (1322, 137), w=2.2)
    f.text(1338, 140, "T", size=s)
    f.arrow(344, 129, 444, 71, stroke=BLUE, w=2.4, size=16)
    f.line((427, 72), (575, 72), stroke=BLUE, w=1.2)
    f.text(382, 125, "+30°", **it)
    # sines
    yc, amp, per, ref = 131, 107, 352.0, 504.0

    def sig(shift):
        return lambda x: yc - amp * math.sin(2 * math.pi * (x - ref - shift) / per)
    f.curve(sig(0), 491, 1204, n=400, stroke=RED, w=2)
    f.curve(sig(-per / 12), 489, 842, n=200, stroke=BLUE, w=2.4, dash=[10, 4, 2, 4])
    f.curve(sig(per / 4), 782, 1279, n=200, stroke=GREEN, w=2.4, dash=[7, 5])
    f.line((515, 94), (515, 249), stroke=RED, w=1.2)
    f.line((859, 106), (859, 268), stroke=GREEN, w=1.6)
    f.line((757, 236), (757, 266), stroke=BLUE, w=1.6)
    f.arrow(782, 266.5, 757, 266.5, stroke=BLUE, w=2, size=10)
    f.line((1144, 212), (1144, 268), stroke=RED, w=1.4)
    f.line((1217, 236), (1217, 268), stroke=GREEN, w=1.6)
    f.arrow(1144, 268, 1217, 268, stroke=GREEN, w=2, size=10)
    f.text(641, 279, "Avance", **it)
    f.text(1231, 265, "Retard", **it)
    f.text(713, 50, "Signal de", **it)
    f.text(713, 84, "référence", **it)
    f.text(574, 177, "Signal", **it)
    f.text(555, 211, "déphasé", **it)
    f.text(555, 245, "de +30°", **it)
    f.text(959, 168, "Signal", **it)
    f.text(959, 202, "déphasé", **it)
    f.text(959, 236, "de −90°", **it)
    f.arrow(694, 38, 654, 63, w=2, size=14)
    f.arrow(834, 38, 884, 61, w=2, size=14)
    f.arrow(674, 208, 702, 193, w=2, size=14)
    f.arrow(957, 177, 932, 165, w=2, size=14)
