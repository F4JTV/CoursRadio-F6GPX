#include "themecolors.h"

#include <QHash>
#include <QRegularExpression>

namespace ThemeColors {

QColor paper(bool dark)
{
    return dark ? QColor(0x1e, 0x1e, 0x1e) : QColor(0xff, 0xff, 0xff);
}

QColor ink(bool dark)
{
    return dark ? QColor(0xea, 0xea, 0xea) : QColor(0x00, 0x00, 0x00);
}

QColor map(const QColor &c, bool dark)
{
    if (!dark || !c.isValid())
        return c;
    const qreal lo = paper(true).lightnessF();
    const qreal hi = ink(true).lightnessF();
    float h, s, l, a;
    c.getHslF(&h, &s, &l, &a);
    const qreal nl = lo + (1.0 - l) * (hi - lo);
    QColor out;
    out.setHslF(h < 0 ? 0 : h, s, nl, a);
    return out;
}

QString mapHtml(const QString &html, bool dark)
{
    if (!dark)
        return html;
    static const QRegularExpression re(QStringLiteral("#([0-9a-fA-F]{6})\\b"));
    QString out;
    out.reserve(html.size());
    qsizetype last = 0;
    auto it = re.globalMatch(html);
    while (it.hasNext()) {
        const auto m = it.next();
        out += QStringView(html).mid(last, m.capturedStart() - last);
        out += map(QColor(m.captured(0)), true).name();
        last = m.capturedEnd();
    }
    out += QStringView(html).mid(last);
    return out;
}

} // namespace ThemeColors
