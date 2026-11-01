"""Chapter 0 (maths) figures: formula tables (measured with tools/measure.py)."""
from figdsl import RED, figure

BLUE = "#0000ff"
S = 27


@figure("c034_1#0")
def thales(f):
    for cx, num, den in ((26, "A", "B"), (95, "C", "D")):
        f.text(cx, 30, num, size=S, anchor="c")
        f.line((cx - 15, 37), (cx + 15, 37), w=2)
        f.text(cx, 64, den, size=S, anchor="c")
    f.text(60, 47, "=", size=S, anchor="c")


@figure("c034_2#0")
def transformations(f):
    for y in (2, 39, 78, 186, 297):
        f.line((2, y), (1367, y), w=2)
    for x in (2, 255.5, 659, 1060.5, 1367):
        f.line((x, 2), (x, 297), w=2)
    for x in (509.5, 848.5, 1230.5):
        f.line((x, 186), (x, 297), w=2)

    def t(x, y, s, anchor="c", **k):
        f.text(x, y, s, size=S, anchor=anchor, **k)
    cx = (128, 457, 860, 1213)
    for x, s in zip(cx, ("Opération", "Addition et Soustraction", "Multiplication et Division", "Puissance et Racine")):
        t(x, 32, s)
    for x, s in zip(cx, ("Equation", "A + B = C – D", "A x B = C / D", "A² = B ou C = √D")):
        t(x, 70, s)
    t(128, 108, "Transformation")
    rows = [("Changement de signe quand le", "terme passe de l'autre côté", "(opposé) : + ⇒ - et - ⇒ +"),
            ("Changement d’opérateur quand", "le terme passe de l'autre côté", "(inverse) : x ⇒ / et / ⇒x"),
            ("Changement de", "puissance des 2 côtés à la", "fois : ² ⇒√ et √ ⇒²")]
    for x, lines in zip(cx[1:], rows):
        for i, s in enumerate(lines):
            t(x, 108 + i * 36, s)
    for i, s in enumerate(["Exemples avec", "X = inconnue", "A,B,C,D = données"]):
        t(128, 216 + i * 36, s)

    def red_a(x, y):
        f.text(x, y, "A", size=S, color=RED)

    def blue_a(x, y):
        f.text(x, y, "A", size=S, color=BLUE, bold=True)

    def route(pts, angle):
        f.line(pts, stroke=BLUE, w=2)
        f.head(pts[-1][0], pts[-1][1], angle, size=13, stroke=BLUE, open_=True, w=2)

    # addition / subtraction
    t(267, 216, "X + ", "l"); red_a(325, 216); t(348, 216, " = C – D", "l")
    t(267, 252, "X", "l"); t(356, 252, "= C – D – ", "l"); blue_a(487, 252)
    route([(326, 221), (326, 281), (492, 281), (492, 258)], -90)
    t(520, 216, "X – ", "l"); red_a(577, 216); t(600, 216, " = 0", "l")
    t(520, 252, "X", "l"); t(602, 252, "=", "l"); blue_a(631, 252)
    route([(582, 220), (582, 281), (633.5, 281), (633.5, 252)], -90)
    # multiplication / division
    t(668, 216, "X x ", "l"); red_a(726, 216); t(748, 216, " = C x D", "l")
    t(668, 252, "X", "l"); t(744, 252, "= C x D", "l")
    f.line((770, 255.5), (840, 255.5), w=2)
    route([(728, 222), (728, 280), (797, 280)], 0)
    blue_a(803, 287)
    t(919, 216, "X = B", "l")
    f.line((919, 220), (937, 220), w=2)
    red_a(917, 252)
    route([(940, 242), (1006, 242), (1006, 258)], 90)
    t(900, 287, "X = B x ", "l"); blue_a(1000, 287)
    # powers / roots
    t(1080, 216, "X²", "l"); t(1135, 216, "=", "l"); t(1185, 216, "B", "l")
    for x, y0, y1 in ((1097.5, 217, 260), (1195.5, 221, 263), (1267.5, 217, 263), (1338.5, 221, 263)):
        f.arrow(x, y0, x, y1, stroke=BLUE, w=2, size=12, open_=True)
    f.text(1124, 252, "⇒√", size=S, color=BLUE)
    t(1084, 287, "X", "l"); t(1135, 287, "=", "l"); t(1180, 287, "√B", "l")
    f.text(1243, 216, "√", size=S, color=RED); t(1260, 216, "X", "l"); t(1295, 216, "=", "l"); t(1332, 216, "D", "l")
    f.text(1282, 254, "⇒²", size=S, color=BLUE)
    t(1258, 287, "X", "l"); t(1287, 287, "=", "l"); t(1322, 287, "D²", "l")


@figure("c034_3#0")
def fractions(f):
    f.text(472, 26, "1 / (1 / A) = 1 x (A / 1) = A", size=S, anchor="r")
    f.text(2, 61, "et", size=S, family="sans")
    f.text(808, 61, "(A / B) / (C / D) = (A / B) x (D / C) = (A x D) / (B x C)", size=S, anchor="r")
    f.text(2, 96, "et encore", size=S, family="sans")
    f.text(505, 96, "A / B / C = (A / B) / (C / 1) =", size=S, anchor="r")
    for x0, x1, num, den in ((513, 533, "A", "B"), (564, 594, "1", "C"), (628, 701, "A x 1", "B x C"),
                             (742, 815, "A", "B x C")):
        c = (x0 + x1) / 2
        f.text(c, 96, num, size=S, anchor="c")
        f.line((x0, 97.5), (x1, 97.5), w=2)
        f.text(c, 129, den, size=S, anchor="c")
    f.text(548, 96, "x", size=S, anchor="c")
    f.text(611, 96, "=", size=S, anchor="c")
    f.text(721, 96, "=", size=S, anchor="c")


@figure("c034_4#0")
def thomson(f):
    k = dict(family="sans", italic=True, size=25)
    for x, s in ((270, "si Z_{L} = Z_{C}, alors 2πFL ="), (546, ", donc (2πF)² ="), (756, ", donc F² ="),
                 (1100, ", d'où la formule : F =")):
        f.text(x, 25, s, anchor="r", **k)
    for x0, x1, den in ((274, 349, "2πFC"), (550, 611, "LC"), (759, 835, "4π²LC"), (1102, 1206, "2π√(LC)")):
        c = (x0 + x1) / 2
        f.text(c, 25, "1", anchor="c", **k)
        f.line((x0, 28.5), (x1, 28.5), w=1.8)
        f.text(c, 58, den, anchor="c", **k)


@figure("c035_1#0")
def puissances_de_10(f):
    for y in (2, 110, 359, 573):
        f.line((2, y), (1379, y), w=2)
    for x in (2, 256, 1379):
        f.line((x, 2), (x, 573), w=2)
    f.line((198, 110), (198, 359), w=2)
    cols = [406, 547, 681, 807, 957, 1085, 1212, 1338]
    for i, s in enumerate(["Symbole", "Préfixe", "Puissances de 10"]):
        f.text(130, 32 + i * 34, s, size=S, anchor="c")
    sym = ["G", "M", "k", "", "m", "µ", "n", "p"]
    pre = ["giga", "méga", "kilo", "UNITE", "milli", "micro", "nano", "pico"]
    pw = ["9", "6", "3", "0", "-3", "-6", "-9", "-12"]
    for x, a, b, c in zip(cols, sym, pre, pw):
        f.text(x, 32, a, size=S, anchor="c")
        f.text(x, 67, b, size=S, anchor="c")
        f.text(x - 3, 101, "10^{" + c + "}", size=S, anchor="c")
    units = [("R (ohm)", "Ω", {547: "MΩ", 681: "kΩ", 807: "Ω"}),
             ("I (ampère)", "A", {807: "A", 957: "mA", 1085: "µA"}),
             ("U (volt)", "V", {681: "kV", 807: "V", 957: "mV", 1085: "µV"}),
             ("P (watt)", "W", {681: "kW", 807: "W", 957: "mW"}),
             ("F (hertz)", "Hz", {406: "GHz", 547: "MHz", 681: "kHz", 807: "Hz"}),
             ("L (henry)", "H", {957: "mH", 1085: "µH", 1212: "nH"}),
             ("C (farad)", "F", {1085: "µF", 1212: "nF", 1352: "pF"})]
    for i, (name, u, cells) in enumerate(units):
        y = 142 + i * 35.2
        f.text(100, y, name, size=S, anchor="c")
        f.text(227, y, u, size=S, anchor="c")
        for x, s in cells.items():
            f.text(x, y, s, size=S, anchor="c")
    f.text(130, 386, "Table de conversion", size=S, anchor="c")
    f.line((272, 368), (272, 420), (1349, 420), (1349, 368), w=2)
    for x in (407, 542, 677, 945, 1080, 1215):
        f.line((x, 368), (x, 420), w=2)
    f.line((809.5, 368), (809.5, 421), w=6, cap=None)
    for x in (318, 367, 455, 500, 590, 635, 723, 770, 858, 905, 990, 1040, 1124, 1169, 1254, 1302):
        f.line((x, 394), (x, 420), w=2)
    for x, s, b in ((521, "0", False), (566, "0", False), (612, "2", True), (656, "5", True)):
        f.text(x, 386, s, size=S, bold=b, anchor="c")
    f.text(684, 386, "(exemple", size=S)
    f.text(822, 386, "n°1)", size=S)
    ex = [("Exemple n°2", [(925, "1", 1), (967, "5", 1), (1015, "0", 1), (1060, "0", 1)]),
          ("Exemple n°3", [(788, "0", 1), (835, "4", 1), (881, "5", 1), (925, "0", 0)]),
          ("Exemple n°4", [(1110, "0", 1), (1135, ",", 1), (1160, "8", 1), (1200, "0", 0)]),
          ("Exemple n°5", [(656, "5", 1), (700, "0", 0), (745, "0", 0), (788, "0", 0)])]
    for i, (label, digits) in enumerate(ex):
        y = 460 + i * 35.3
        f.text(129, y, label, size=S, anchor="c")
        for x, s, b in digits:
            f.text(x, y, s, size=S, bold=bool(b), anchor="c")
