"""Chapter 4 (decibel, RC/LC circuits, Thomson) figures."""
import math

from figdsl import BLACK, RED, figure

from .t02_alternatif import BLUE, NAVY, GREY, NB, BU, I_, _humps
from .t03_transfo import vcoil

SANS = dict(family="sans")


@figure("c057_2#0")
def chaine_reception(f):
    k = dict(size=28, family="sans")
    for x0, x1 in ((11, 58), (56, 102), (100, 147), (145, 191)):
        f.line((x0, 113), (x1, 23), stroke=RED, w=5, cap=None)
    f.line((38, 68), (165, 68), w=2.6)
    f.path("M104 68Q116 93 178 94L524 94", w=5)
    f.text(185, 63, "Antenne : gain = 19 dB", **k)
    f.rect(523, 56, 198, 94, lw=4)
    f.text(622, 86, "Préampli", anchor="c", **k)
    f.text(622, 118, "Gain = 20 dB", anchor="c", **k)
    f.line((723, 96.5), (1097, 96.5), w=5)
    f.line((1123, 96.5), (1232, 96.5), w=5)
    f.rect(1099, 80, 22, 44, stroke=RED, fill="#c0c0c0", lw=4)
    f.text(897, 55, "33 m de câble coaxial", anchor="c", **k)
    f.text(897, 86, "Perte = 3 dB / 100 m", anchor="c", **k)
    f.text(1083, 30, "PL (Connecteur HF)", **k)
    f.text(1081, 59, "Perte d’insertion = 2 dB", **k)


@figure("c057_3#0")
def conversion_db(f):
    s = 28.5
    f.rect(3, 5, 612, 153, stroke="#404040", lw=2)
    f.rich(14, 40, [("Table de conversion simplifiée", BU), (" :", {})], size=s)
    f.text(14, 70, "unités de dB :", size=s)
    f.text(14, 104, "Rapport arithmétique :", size=s)
    for x, a, b in ((328, "0", "1"), (389, "3", "2"), (449, "6", "4"), (517, "7", "5"), (570, "9", "8")):
        f.text(x, 70, a, size=s, anchor="c")
        f.text(x, 104, b, size=s, anchor="c")
    f.text(310, 138, "Dizaine de dB = nombre de 0 du rapport", size=s, anchor="c")
    k = dict(size=26, family="sans")
    f.text(16, 183, "Exemples convertis avec la table simplifiée :", **k)
    f.text(14, 211, "dB", **k)
    f.text(16, 245, "Ex n°", **k)
    f.text(16, 277, "Rapport", **k)
    cols = [("9", "1", "8", 155, None), ("2 6", "2", "4 00", 244, "up"), ("1 6", "3", "4 0", 343, "down"),
            ("2 0", "4", "1 00", 441, "down"), ("3 3", "5", "2 000", 554, "down")]
    for db, n, rap, cx, mode in cols:
        f.text(cx, 211, db.replace(" ", "   "), anchor="c", **k)
        f.text(cx - 18, 245, n, anchor="r", **k)
        f.text(cx, 277, rap.replace(" ", "  "), anchor="c", **k)
        if mode is None:
            f.arrow(cx, 249, cx, 218, stroke=BLUE, w=2.4, size=10)
        elif mode == "up":
            f.arrow(cx - 13, 251, cx + 13, 218, stroke=BLUE, w=2.4, size=10)
            f.arrow(cx + 13, 251, cx - 13, 218, stroke=BLUE, w=2.4, size=10)
        else:
            f.arrow(cx - 13, 219, cx + 13, 253, stroke=BLUE, w=2.4, size=10)
            f.arrow(cx + 13, 219, cx - 13, 253, stroke=BLUE, w=2.4, size=10)


@figure("c058_1#0")
def ampli_gain(f):
    f.poly((114.5, 7), (198, 65), (114.5, 123), w=4)
    f.line((60, 65.5), (114.5, 65.5), w=2.4)
    f.line((198, 65.5), (252, 65.5), w=2.4)
    k = dict(size=28, family="sans", italic=True)
    f.text(4, 50, "U_{e} = 4 V", **k)
    f.text(195, 50, "U_{s} = 8 V", **k)


@figure("c058_3#0")
def filtre_rc(f):
    f.rect(67, 8, 166, 60, lw=4)
    f.text(150, 47, "21,22 Ω", size=28, family="sans", italic=True, anchor="c")
    f.line((39, 34.5), (67, 34.5), w=2.4)
    f.line((233, 34.5), (316, 34.5), w=2.4)
    f.line((288.5, 34.5), (288.5, 62), w=2.4)
    f.line((261, 62.5), (316, 62.5), w=4)
    f.line((261, 90), (316, 90), w=4)
    f.line((288.5, 90), (288.5, 115), w=2.4)
    f.rect(261, 114, 55, 8, stroke=None, fill=BLACK)
    f.text(183, 101, "5 µF", size=28, family="sans", italic=True)
    f.arrow(11.5, 116, 11.5, 40, stroke=BLUE, w=2.4, size=16, open_=True)
    f.arrow(344, 116, 344, 39, stroke=BLUE, w=2.4, size=16, open_=True)
    f.text(14, 108, "V_{e} = 4 V", size=30, italic=True)
    f.text(355, 100, "V_{s}", size=30, italic=True)


def frac(f, cx, y, num, den, x0, x1, size=30, gap=35, **k):
    f.text(cx, y, num, size=size, anchor="c", **k)
    f.line((x0, y + 5.5), (x1, y + 5.5), stroke=k.get("color", BLACK), w=2)
    f.text(cx, y + gap, den, size=size, anchor="c", **k)


def _up_tick(f, x, y):
    f.poly((x - 5, y + 12), (x + 5, y + 12), (x, y), stroke=None, fill=BLACK)
    f.line((x, y + 12), (x, y + 18), w=2)


@figure("c058_2#0")
def filtres_rc(f):
    s = 30
    nb = dict(bold=True, color=NAVY)
    f.text(123, 30, "R =", size=s)
    frac(f, 207, 30, "1", "ωC", 185, 228)
    f.text(257, 30, "⇔", size=s, anchor="c")
    f.text(287, 30, "R =", size=s)
    frac(f, 370, 30, "1", "2πFC", 343, 411)
    f.text(456, 30, "⇔", size=s, anchor="c")
    f.text(522, 30, "f(Hz) =", size=s, **nb)
    frac(f, 680, 30, "1", "2πR(Ω).C(F)", 606, 769, **nb)
    f.rich(787, 30, ["; formule simplifiée : ", ("f(Hz) = 159 / R(kΩ) / C(µF)", NB)], size=s)
    # low-pass schematic
    red = dict(size=s, color=RED)
    f.text(11, 108, "Entrée", **red)
    f.text(234, 108, "Sortie", **red)
    f.line((28, 122), (90, 122), w=2.4)
    f.rect(90, 101, 60, 41, lw=4)
    f.text(120, 131, "R", size=s, anchor="c")
    f.line((150, 122), (274, 122), w=2.4)
    f.line((211.5, 122), (211.5, 182), w=2.4)
    f.line((192, 183), (232, 183), w=4)
    f.line((192, 203.5), (232, 203.5), w=4)
    f.line((211.5, 204), (211.5, 229), w=2.4)
    f.rect(172, 229, 81, 10, stroke=None, fill=BLACK)
    f.text(234, 184, "C", size=s)
    f.text(58, 264, "Filtre RC  passe-bas", size=s, bold=True, underline=True)
    # low-pass Bode plot
    f.line((382.5, 275), (382.5, 95), w=2)
    f.poly((377, 97), (388, 97), (382.5, 84), stroke=None, fill=BLACK)
    f.arrow(382, 257.5, 711, 257.5, w=2, size=14)
    for x in (382.5, 502, 584):
        _up_tick(f, x, 258)
    f.line((382, 206), (502, 206), stroke=RED, w=1.6, dash=[2, 2])
    f.line((382, 243), (584, 243), stroke=RED, w=1.6, dash=[2, 2])
    f.spline([(384, 124), (443, 165), (502, 206), (545, 231), (584, 244), (630, 250), (679, 250)], stroke=BLUE, w=2)
    f.text(323, 131, "0 dB", size=s)
    f.text(315, 210, "-3 dB", size=s)
    f.text(315, 252, "-6 dB", size=s)
    f.text(386, 298, "0 Hz", size=s)
    f.text(486, 300, "fc", size=s)
    f.text(567, 298, "2 fc", size=s)
    f.text(712, 285, "f", size=s)
    f.line((660, 104), (789, 284), w=1.4, dash=[2, 2])
    # high-pass schematic
    f.text(714, 108, "Entrée", **red)
    f.text(870, 108, "Sortie", **red)
    f.line((720, 119.5), (821, 119.5), w=2.4)
    f.line((821, 99), (821, 137), w=4)
    f.line((842.5, 99), (842.5, 137), w=4)
    f.line((842.5, 117.5), (922, 117.5), w=2.4)
    f.text(792, 140, "C", size=s)
    f.line((882.5, 117.5), (882.5, 183), w=2.4)
    f.rect(862, 183, 40, 60, lw=4)
    f.text(880, 214, "R", size=s, anchor="c")
    f.line((882.5, 245), (882.5, 262), w=2.4)
    f.rect(843, 262, 79, 9, stroke=None, fill=BLACK)
    # high-pass Bode plot
    f.text(994, 82, "Filtre RC  passe-haut", size=s, bold=True, underline=True)
    f.line((964.5, 284), (964.5, 77), w=2)
    f.poly((959, 79), (970, 79), (964.5, 65), stroke=None, fill=BLACK)
    f.arrow(966, 287.5, 1244, 287.5, w=2, size=14)
    f.line((966, 140), (1230, 140), stroke=RED, w=2, dash=[5, 4])
    f.line((966, 181), (1052, 181), (1052, 285), stroke=RED, w=1.4)
    _up_tick(f, 1052, 270)
    f.spline([(966, 284), (1000, 240), (1030, 200), (1052, 181), (1100, 166), (1160, 156), (1225, 148)], stroke=BLUE, w=2)
    f.text(977, 115, "V", size=s)
    f.text(1219, 276, "f", size=s)
    f.text(1179, 125, "Ve", size=s)
    f.text(1168, 177, "Vs", size=s)
    # vertical high-pass schematic
    f.text(1272, 83, "Entrée", **red)
    f.text(1332, 166, "Sortie", **red)
    f.line((1309.5, 97), (1309.5, 138.5), w=2.4)
    f.line((1289, 138.5), (1329, 138.5), w=3.4)
    f.line((1289, 159.5), (1329, 159.5), w=3.4)
    f.line((1309.5, 159.5), (1309.5, 202), w=2.4)
    f.line((1309.5, 179.5), (1349, 179.5), w=2.4)
    f.rect(1289, 203, 40, 59, lw=4)
    f.line((1309.5, 264), (1309.5, 282), w=2.4)
    f.rect(1289, 281, 40, 9, stroke=None, fill=BLACK)
    f.arrow(1279, 277, 1279, 119, stroke=BLUE, w=2.6, size=16, open_=True)
    f.text(1237, 194, "Ve", size=s)
    f.arrow(1350.5, 288, 1350.5, 209, stroke=BLUE, w=2.6, size=16, open_=True)
    f.text(1360, 233, "Vs", size=s)


@figure("c058_2#1")
def filtre_exemple(f):
    k = dict(size=28, family="sans")
    f.rect(35, 6, 127, 51, lw=4)
    f.text(98, 41, "200 Ω", anchor="c", **k)
    f.line((9, 22.5), (35, 22.5), w=2.4)
    f.line((162, 21.5), (239, 21.5), w=2.4)
    f.line((188.5, 21.5), (188.5, 73.5), w=2.4)
    f.line((163, 73.5), (213, 73.5), w=4)
    f.line((163, 100), (213, 100), w=4)
    f.line((188.5, 100), (188.5, 122), w=2.4)
    f.rect(163, 122, 50, 5, stroke=None, fill=BLACK)
    f.text(217, 95, "5 µF", **k)


@figure("c059_1#0")
def thomson_formules(f):
    s = 31
    f.rich(14, 38, [("ωL = 1 / (ωC)", NB), (" ⇔ L . C . ω² = 1 ⇔ ω² = 1 / (L . C) ⇔ ω = 1 / (√(L . C)) ⇔ 2 . π . f = 1 / (√[L . C]), donc :", {})], size=s)
    nb = dict(bold=True, color=NAVY)
    f.text(14, 82, "fc = fo =", size=s, **nb)
    frac(f, 207, 82, "1", "2 π √(LC)", 122, 292, size=s, gap=40, **nb)
    f.text(315, 82, "=", size=s, **nb)
    frac(f, 418, 82, "1", "6,28 √(L . C)", 340, 497, size=s, gap=40, **nb)
    f.rich(683, 82, ["formule simplifiée : ", ("f(MHz) =", NB)], size=s)
    frac(f, 1198, 82, "159", "√[L(µH) . C(pF)]", 1084, 1311, size=s, gap=40, **nb)


@figure("c059_3#0")
def filtre_rl(f):
    it = dict(size=31, italic=True)
    f.line((5, 48.5), (94, 48.5), w=2.4)
    _humps(f, 94, 204, 48.5, 4, 24, w=2.4)
    f.line((204, 48.5), (292, 48.5), w=2.4)
    f.line((236.5, 48.5), (236.5, 82), w=2.4)
    f.rect(210, 82, 66, 55, lw=4)
    f.text(243, 117, "R", anchor="c", **it)
    f.line((237.5, 139), (237.5, 162), w=2.4)
    f.rect(210, 161, 54, 8, stroke=None, fill=BLACK)
    f.text(66, 30, "L", **it)
    f.text(41, 108, "Filtre RL", **it)
    f.text(35, 146, "passe-bas", **it)


MBLUE = "#0070c0"


def _graph(f, x_axis, y_axis, y_top, x_end, tick_x, tick_label, label_x, blue_y, blue_x0, blue_x1,
           db0, db60, curve, f_label):
    s = 30
    f.line((x_axis, y_axis), (x_axis, y_top + 12), w=2.4)
    f.poly((x_axis - 5, y_top + 14), (x_axis + 5, y_top + 14), (x_axis, y_top), stroke=None, fill=BLACK)
    f.arrow(x_axis, y_axis, x_end, y_axis, stroke="#595959", w=3, size=16)
    f.poly((tick_x - 4, y_axis - 1), (tick_x + 4, y_axis - 1), (tick_x, y_axis - 14), stroke=None, fill=BLACK)
    f.text(label_x, y_axis + 36, tick_label, size=s, anchor="c")
    f.line((blue_x0, blue_y), (blue_x1, blue_y), stroke=MBLUE, w=2.4)
    f.text(db0[0], db0[1], "0 dB", size=s)
    f.text(db60[0], db60[1], "-60 dB", size=s)
    f.spline(curve, stroke=RED, w=2)
    f.text(f_label[0], f_label[1], "f", size=s)


@figure("c059_2#0")
def filtres_lc(f):
    s = 30
    f.rect(5, 14, 1370, 631, lw=2.4)
    f.line((168, 14), (168, 645), w=2.4)
    f.line((771.5, 14), (771.5, 645), w=2.4)
    f.line((5, 330.5), (1375, 330.5), w=2.4)
    c1 = 87
    for y, t, st in ((76, "Schéma", BU), (145, "Impédance", BU), (214, "Réponse en", {}), (250, "Fréquence", {}),
                     (319, "Résonance", BU), (392, "Schéma", BU), (530, "Réponse en", {}), (566, "Fréquence", {}),
                     (638, "Coupure", BU)):
        f.rich(c1, y, [(t, st)], size=s, anchor="c")
    # series
    f.rich(470, 43, ["Filtre ", ("Série", BU), " (Passe bande)"], size=s, anchor="c")
    f.line((248, 101.5), (334, 101.5), w=2.4)
    _humps(f, 334, 440, 101.5, 5, 20, w=2.4)
    f.line((440, 101.5), (527, 101.5), w=2.4)
    f.line((527, 80), (527, 123), w=4)
    f.line((550, 80), (550, 123), w=4)
    f.line((550, 101.5), (593, 101.5), w=2.4)
    f.text(318, 85, "L", size=s)
    f.text(560, 85, "C", size=s)
    f.rich(760, 147, [("Nulle", BU), " pour Fo"], size=s, anchor="r")
    _graph(f, 280.5, 275.5, 168, 656, 466, "fo", 463, 193, 280, 634, (190, 202), (186, 272),
           [(295, 265), (380, 260), (425, 248), (447, 225), (466, 196), (485, 225), (510, 252), (575, 268)],
           (686, 286))
    # parallel
    f.rich(1073, 43, ["Filtre ", ("Parallèle", BU), " (ou ", ("Bouchon", BU), " ou coupe bande)"], size=s, anchor="c")
    f.line((901, 129), (943.5, 129), w=2.4)
    f.line((1117.5, 129), (1159, 129), w=2.4)
    f.line((943.5, 171), (943.5, 85.5), (1008.5, 85.5), w=2.4)
    f.line((1030.5, 85.5), (1117.5, 85.5), (1117.5, 171), w=2.4)
    f.line((1008.5, 64), (1008.5, 107), w=4)
    f.line((1030.5, 64), (1030.5, 107), w=4)
    f.line((943.5, 171), (990, 171), w=2.4)
    _humps(f, 990, 1075, 171, 4, 22, w=2.4)
    f.line((1075, 171), (1117.5, 171), w=2.4)
    f.text(983, 136, "L", size=s)
    f.text(1035, 111, "C", size=s)
    f.rich(1362, 147, [("Infinie", BU), " pour Fo"], size=s, anchor="r")
    _graph(f, 892.5, 287, 179, 1214, 1053.5, "fo", 1043, 213.5, 890, 1242, (787, 219), (783, 285),
           [(899, 216), (980, 225), (1015, 240), (1048, 275), (1080, 245), (1110, 225), (1185, 215)],
           (1218, 290))
    # high pass
    f.rich(470, 359, ["Filtre ", ("Passe Haut", BU)], size=s, anchor="c")
    f.line((344, 413), (409, 413), w=2.4)
    f.line((409, 392), (409, 434), w=4)
    f.line((430.5, 392), (430.5, 434), w=4)
    f.line((430.5, 413), (646, 413), w=2.4)
    f.line((473, 413), (473, 478), (516, 478), stroke="#595959", w=3)
    _humps(f, 516, 626, 478, 5, 20, w=2.4)
    f.line((626, 478), (684, 478), stroke="#595959", w=3)
    f.rect(683, 458, 11, 40, stroke=None, fill=BLACK)
    f.text(398, 465, "C", size=s)
    f.text(524, 500, "L", size=s)
    _graph(f, 269.5, 603, 472, 636, 440.5, "fc", 434, 511.5, 275, 627, (174, 523), (170, 594),
           [(277, 596), (330, 565), (380, 535), (440, 520), (520, 514), (600, 512)], (638, 612))
    # low pass
    f.rich(1073, 359, ["Filtre ", ("Passe Bas", BU)], size=s, anchor="c")
    f.line((933, 408.5), (1020, 408.5), w=2.4)
    _humps(f, 1020, 1135, 408.5, 5, 20, w=2.4)
    f.line((1135, 408.5), (1279, 408.5), w=2.4)
    f.line((1191, 408.5), (1191, 472), (1235.5, 472), stroke="#595959", w=3)
    f.line((1235.5, 451), (1235.5, 494), w=4)
    f.line((1256, 451), (1256, 494), w=4)
    f.line((1256, 472), (1293, 472), w=2.4)
    f.rect(1293, 451, 13, 43, stroke=None, fill=BLACK)
    f.text(1062, 434, "L", size=s)
    f.text(1225, 433, "C", size=s)
    _graph(f, 892.5, 607.5, 458, 1202, 1064, "fc", 1058, 516, 892, 1247, (796, 517), (796, 584),
           [(899, 523), (1000, 528), (1080, 542), (1150, 582), (1200, 606)], (1218, 612))


def _dotted_r(f, x0, y0, x1, y1, label, size=30):
    f.rect(x0, y0, x1 - x0, y1 - y0, lw=2.4, dash=[2, 2.5])
    f.text((x0 + x1) / 2, (y0 + y1) / 2 + 11, label, size=size, anchor="c")


@figure("c060_1#0")
def circuits_resonants(f):
    s = 30
    w = 2.4
    # series
    f.line((4, 74), (21, 74), w=w)
    _humps(f, 21, 127, 74, 4, 25, w=w)
    f.line((127, 73.5), (202.5, 73.5), w=w)
    f.line((202.5, 48), (202.5, 89), w=4)
    f.line((229, 48), (229, 89), w=4)
    f.line((229, 76), (256, 76), w=w)
    _dotted_r(f, 256, 59, 353, 105, "20 Ω")
    f.line((353, 74), (370, 74), w=w)
    f.text(59, 37, "25 µH", size=s)
    f.text(162, 37, "100 pF", size=s)
    f.text(65, 120, "Circuit série", size=s)
    # tank
    f.line((434, 85), (469, 85), w=w)
    f.line((469, 111), (469, 32), (521, 32), w=w)
    _humps(f, 521, 629, 32, 4, 24, w=w)
    f.line((629, 33), (656, 33), w=w)
    _dotted_r(f, 656, 7, 753, 61, "20 Ω")
    f.line((753, 32.5), (779.5, 32.5), (779.5, 111), (575.5, 111), w=w)
    f.line((469, 110), (548.5, 110), w=w)
    f.line((548.5, 85), (548.5, 135), w=4)
    f.line((575.5, 85), (575.5, 135), w=4)
    f.line((779.5, 85), (805, 85), w=w)
    f.text(501, 66, "25 µH", size=s)
    f.text(599, 89, "100 pF", size=s)
    f.text(602, 147, "Circuit bouchon", size=s)
    # parallel
    f.text(995, 70, "Circuit", size=s, anchor="c")
    f.text(995, 104, "parallèle", size=s, anchor="c")
    f.line((1054.5, 201), (1054.5, 45), (1109, 45), w=w)
    _humps(f, 1109, 1214, 45, 4, 24, w=w)
    f.line((1214, 45), (1321, 45), (1321, 201), (1266, 201), w=w)
    f.line((1002, 123), (1134.5, 123), w=w)
    f.line((1134.5, 97), (1134.5, 148), w=4)
    f.line((1161.5, 97), (1161.5, 148), w=4)
    f.line((1161.5, 123), (1374, 123), w=w)
    f.line((1054.5, 201), (1107, 201), w=w)
    _dotted_r(f, 1107, 169, 1266, 226, "12,5 kΩ")
    f.text(1098, 77, "25 µH", size=s)
    f.text(1168, 152, "100 pF", size=s)
    f.text(16, 194, "L et C ayant les mêmes valeurs, les circuits ont la même fréquence de résonance.", size=s)
    f.text(16, 227, "Les résistances n’ont pas d’incidence sur la fréquence de résonance des circuits.", size=s)


@figure("c060_2#0")
def pente_filtre(f):
    s = 30
    f.text(23, 30, "Atténuation", size=s)
    f.line((21, 279), (21, 64), w=2.4)
    f.poly((15, 66), (27, 66), (21, 50), stroke=None, fill=BLACK)
    f.line((20, 278.5), (466, 278.5), w=2.4)
    f.poly((464, 272), (464, 285), (480, 278.5), stroke=None, fill=BLACK)
    for y, t in ((62, "0 dB"), (114, "- 3 dB"), (177, "- 30 dB"), (230, "- 60 dB")):
        f.text(45 if t == "0 dB" else 29, y, t, size=s)
    for y, x0, x1 in ((71, 41, 440), (90, 62, 374), (154, 41, 440), (238, 41, 440)):
        f.line((x0, y), (x1, y), stroke=RED, w=1.6)
    f.line((251, 48), (251, 278), stroke=RED, w=1.6, dash=[4, 3])
    f.line((84, 280), (272, 48), w=1.4)
    f.spline([(88, 270), (170, 170), (250, 88), (300, 77), (370, 73), (440, 72)], w=4.5, dash=[12, 6])
    for x in (84, 115, 167.5, 250.5, 333.5, 417):
        f.line((x, 302), (x, 292), w=2.2)
        f.poly((x - 5, 293), (x + 5, 293), (x, 280), stroke=None, fill=BLACK)
    for x, t in ((82, "¹/₄f"), (128, "¹/₃f"), (180, "¹/₂f"), (247, "fc"), (333, "2 f"), (417, "4 f")):
        f.text(x, 341, t, size=s, anchor="c")
    f.arrow(290, 212, 169, 177, stroke=BLUE, w=2, size=16)
    f.text(288, 196, "Pente du filtre", size=s)
    f.text(288, 229, "en dB/octave", size=s)


@figure("c061_1#0")
def coefficients_q(f):
    for y in (7.5, 43.5, 80, 154.5):
        f.line((5, y), (752, y), w=2.4)
    for x in (5.5, 142.5, 345.5, 548, 751):
        f.line((x, 7), (x, 155), w=2.4)
    nb = dict(size=30, bold=True, color=NAVY, anchor="c")
    nbi = dict(size=30, bold=True, italic=True, color=NAVY, anchor="c")
    for x, t in ((74, "Circuit"), (244, "Bouchon"), (447, "Série"), (649, "Parallèle")):
        f.text(x, 37, t, **nb)
    for x, t in ((74, "Z"), (244, "L / (C . R)"), (447, "R"), (649, "R")):
        f.text(x, 73, t, **nb)
    f.text(74, 128, "Q", **nb)
    f.text(244, 108, "Q = Z / X_{L}", **nbi)
    f.text(244, 146, "√(L / C) / R", **nb)
    f.text(447, 108, "Q = X_{L} / Z", **nbi)
    f.text(447, 146, "√(L / C) / R", **nb)
    f.text(649, 108, "Q = Z / X_{L}", **nbi)
    f.text(649, 146, "R / [ √(L / C)]", **nbi)


@figure("c061_2#0")
def z_bouchon(f):
    f.text(7, 25, "Z_{bouchon} =", size=28)
    f.text(259, 25, "√((ωL)²+R²) x 1/(ωC))", size=28, anchor="c")
    f.line((124, 30), (394, 30), w=2)
    f.text(259, 62, "√(R² + (ωL – 1/ωC)²)", size=28, anchor="c")


DGREEN = "#008000"


def _cv(f, x, y0, y1, horizontal=False, w=2.4):
    """Variable capacitor between (x, y0) and (x, y1) (vertical) - plates at mid."""
    m = (y0 + y1) / 2
    f.line((x, y0), (x, m - 9), w=w)
    f.line((x, m + 9), (x, y1), w=w)
    f.line((x - 17, m - 7), (x + 17, m - 7), w=4)
    f.line((x - 17, m + 7), (x + 17, m + 7), w=4)
    f.arrow(x - 20, m + 19, x + 20, m - 24, w=2, size=12, open_=True)


def _cvh(f, x0, x1, y, w=2.4):
    m = (x0 + x1) / 2
    f.line((x0, y), (m - 13, y), w=w)
    f.line((m + 13, y), (x1, y), w=w)
    f.line((m - 13, y - 25), (m - 13, y + 25), w=4)
    f.line((m + 13, y - 25), (m + 13, y + 25), w=4)
    f.arrow(m - 38, y + 26, m + 38, y - 26, w=2, size=12, open_=True)


@figure("c062_1#0")
def filtres_pi_t(f):
    s = 30
    w = 2.4
    f.text(16, 52, "TX", size=s)
    f.line((36, 63.5), (99, 63.5), w=w)
    f.line((98, 108), (98, 43), (160, 43), w=w)
    _humps(f, 160, 265, 43, 4, 22, w=w)
    f.line((265, 43), (327, 43), (327, 108), w=w)
    f.line((327, 63.5), (368, 63.5), w=w)
    f.text(328, 52, "ANT", size=s)
    for x in (98, 327):
        _cv(f, x, 108, 160)
        f.rect(x - 21, 162, 42, 10, stroke=None, fill=BLACK)
    f.text(145, 74, "Filtre en Π", size=s)
    f.text(2, 137, "CV1", size=s)
    f.text(237, 137, "CV2", size=s)
    f.text(379, 145, "Équi-", size=s)
    f.text(366, 179, "valent à", size=s)
    # equivalent
    f.text(408, 52, "TX", size=s)
    f.line((451, 62), (471, 62), w=w)
    f.line((471, 103), (471, 41), (493, 41), w=w)
    _humps(f, 493, 615, 41, 5, 22, w=w)
    f.line((615, 41), (637.5, 41), (637.5, 103), (471, 103), w=w)
    f.line((637.5, 61), (679, 61), w=w)
    f.text(640, 52, "ANT", size=s)
    for x in (502.5, 606.5):
        f.line((x - 11, 82), (x - 11, 126), w=4)
        f.line((x + 11, 82), (x + 11, 126), w=4)
        f.arrow(x - 33, 128, x + 33, 80, w=2, size=12, open_=True)
    f.line((554.5, 103), (554.5, 160), w=w)
    f.rect(534, 160, 41, 10, stroke=None, fill=BLACK)
    f.text(484, 145, "CV1", size=s)
    f.text(588, 145, "CV2", size=s)
    f.text(719, 117, "C_{T} =", size=s)
    f.text(848, 117, "CV1 x CV2", size=s, anchor="c")
    f.line((780, 122), (916, 122), w=2)
    f.text(848, 152, "CV1 + CV2", size=s, anchor="c")
    # T filter
    f.text(979, 64, "TX", size=s)
    f.line((1009, 26.5), (1035, 26.5), w=w)
    _cvh(f, 1035, 1112, 26.5)
    f.line((1112, 26.5), (1165, 26.5), w=w)
    _cvh(f, 1165, 1242, 26.5)
    f.line((1242, 26.5), (1268, 26.5), w=w)
    f.text(1240, 49, "ANT", size=s)
    f.line((1138.5, 26.5), (1138.5, 52), w=w)
    vcoil(f, 1138.5, 52, 131, 3, 13, side=1)
    f.line((1138.5, 131), (1138.5, 160), w=w)
    f.rect(1113, 161, 51, 12, stroke=None, fill=BLACK)
    f.text(1056, 74, "CV1", size=s)
    f.text(1186, 74, "CV2", size=s)
    f.text(1075, 127, "Filtre", size=s)
    f.text(1173, 127, "en T", size=s)


@figure("c062_2#0")
def courbe_analyseur(f):
    f.rect(3.5, 5, 523.5, 209, lw=2)
    f.line((108.5, 5), (108.5, 214), w=2)
    f.line((108, 152.5), (527, 152.5), w=2)
    for x in (161, 213, 265, 317, 370, 422, 474):
        f.line((x, 5), (x, 152), stroke=RED, w=1.4, dash=[2, 3])
    for y in (30, 81, 133):
        f.line((108, y), (527, y), stroke=RED, w=1.4, dash=[2, 3])
    k = dict(size=24, family="sans")
    for x, t in ((39, "V"), (66, "dBm")):
        f.text(x, 200, t, rot=-90, anchor="l", va="middle", **k)
    for x, a, b, c in ((39, "1,2", "5,4", "24"), (66, "13", "26", "39")):
        f.text(x, 133, a, rot=-90, anchor="c", va="middle", **k)
        f.text(x, 81, b, rot=-90, anchor="c", va="middle", **k)
        f.text(x, 30, c, rot=-90, anchor="c", va="middle", **k)
    for i, t in enumerate(("500", "520", "540", "560", "580", "600", "620")):
        f.text(145 + i * 52, 192, t, size=26, family="sans", anchor="c")
    f.spline([(132, 145), (200, 135), (250, 95), (282, 33), (302, 33), (340, 43), (368, 42), (390, 30),
              (408, 50), (440, 102), (474, 135), (510, 143)], stroke=DGREEN, w=5)


@figure("c062_3#0")
def deux_cellules(f):
    s = 30
    f.line((84.5, 312), (84.5, 64), w=2.4)
    f.poly((79, 66), (90, 66), (84.5, 50), stroke=None, fill=BLACK)
    f.line((83, 313), (460, 313), w=2.4)
    f.poly((458, 307), (458, 319), (472, 313), stroke=None, fill=BLACK)
    f.text(52, 42, "dB", size=s)
    f.text(468, 340, "f", size=s, italic=True)
    for y, x1 in ((107, 386), (132, 430), (258, 452)):
        f.line((84, y), (x1, y), stroke=RED, w=1.6)
    f.text(82, 115, "0 dB", size=s, anchor="r")
    f.text(82, 141, "-3 dB", size=s, anchor="r")
    f.text(82, 255, "-60 dB", size=s, anchor="r")
    for x in (138, 218, 350, 430):
        f.line((x, 170 if x in (138, 430) else 95), (x, 395 if x in (138, 430) else 340), stroke=RED, w=1.4, dash=[2, 3])
    f.spline([(110, 237), (160, 200), (215, 130), (245, 100), (280, 108), (320, 185), (360, 222), (390, 242),
              (480, 242)], stroke="#88c088", w=1.4, dash=[2, 2])
    f.spline([(130, 245), (190, 200), (250, 130), (300, 105), (325, 100), (355, 125), (420, 215), (480, 243)],
             stroke="#88c088", w=1.4, dash=[2, 2])
    f.spline([(100, 278), (150, 240), (200, 165), (238, 112), (258, 105), (283, 118), (308, 105), (328, 102),
              (352, 122), (400, 200), (440, 255), (482, 272)], stroke=DGREEN, w=4.5)
    f.text(158, 46, "Courbe de réponse du filtre", size=s)
    f.text(208, 80, "constitué des 2 cellules", size=s)
    f.arrow(430, 103, 373, 165, w=2, size=20)
    f.text(245, 230, "Courbes", size=s)
    f.text(240, 264, "de réponse", size=s)
    f.text(216, 298, "des 2 cellules", size=s)
    f.line((228, 280), (228, 228), stroke=BLUE, w=2.4)
    f.head(228, 225, -90, size=16, stroke=BLUE)
    f.arrow(228, 280, 122, 240, stroke=BLUE, w=2.2, size=16)
    f.arrow(218, 336.5, 348, 336.5, stroke=BLUE, w=2.4, size=12, both=True)
    f.text(285, 368, "B (= δf à -3 dB)", size=s, anchor="c")
    f.arrow(140, 388.5, 427, 388.5, stroke=BLUE, w=2.4, size=12, both=True)
    f.text(283, 416, "réjection ultime", size=s, anchor="c")
    f.text(283, 451, "δf à -60 dB", size=s, anchor="c")
