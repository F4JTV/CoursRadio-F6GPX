#include "diagram.h"
#include "themecolors.h"

#include <QDir>
#include <QFile>
#include <QFont>
#include <QFontDatabase>
#include <QFontMetricsF>
#include <QImage>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QPaintDevice>
#include <QPainter>
#include <QtMath>

namespace {

QString g_imageBasePath = QStringLiteral(":/content/images/");

// ---------------------------------------------------------------------------
// Minimal SVG-like path parser (absolute commands M L H V C Q Z).
// ---------------------------------------------------------------------------
class PathParser
{
public:
    explicit PathParser(const QString &d) : m_d(d) {}

    QPainterPath parse()
    {
        QPainterPath path;
        QChar cmd;
        QPointF cur;
        while (true) {
            skipSeparators();
            if (m_pos >= m_d.size())
                break;
            const QChar c = m_d.at(m_pos);
            if (c.isLetter()) {
                cmd = c;
                ++m_pos;
                if (cmd == QLatin1Char('Z') || cmd == QLatin1Char('z')) {
                    path.closeSubpath();
                    cur = path.currentPosition();
                    continue;
                }
            }
            bool ok = true;
            switch (cmd.toLatin1()) {
            case 'M': {
                const QPointF p = point(&ok);
                if (!ok) return path;
                path.moveTo(p);
                cur = p;
                cmd = QLatin1Char('L'); // implicit lineto after moveto
                break;
            }
            case 'L': {
                const QPointF p = point(&ok);
                if (!ok) return path;
                path.lineTo(p);
                cur = p;
                break;
            }
            case 'H': {
                const qreal x = number(&ok);
                if (!ok) return path;
                cur.setX(x);
                path.lineTo(cur);
                break;
            }
            case 'V': {
                const qreal y = number(&ok);
                if (!ok) return path;
                cur.setY(y);
                path.lineTo(cur);
                break;
            }
            case 'C': {
                const QPointF c1 = point(&ok);
                const QPointF c2 = point(&ok);
                const QPointF p = point(&ok);
                if (!ok) return path;
                path.cubicTo(c1, c2, p);
                cur = p;
                break;
            }
            case 'Q': {
                const QPointF c1 = point(&ok);
                const QPointF p = point(&ok);
                if (!ok) return path;
                path.quadTo(c1, p);
                cur = p;
                break;
            }
            default:
                return path; // unknown command: stop parsing
            }
        }
        return path;
    }

private:
    void skipSeparators()
    {
        while (m_pos < m_d.size()) {
            const QChar c = m_d.at(m_pos);
            if (c.isSpace() || c == QLatin1Char(','))
                ++m_pos;
            else
                break;
        }
    }

    qreal number(bool *ok)
    {
        skipSeparators();
        const qsizetype start = m_pos;
        if (m_pos < m_d.size() && (m_d.at(m_pos) == QLatin1Char('-') || m_d.at(m_pos) == QLatin1Char('+')))
            ++m_pos;
        while (m_pos < m_d.size()) {
            const QChar c = m_d.at(m_pos);
            if (c.isDigit() || c == QLatin1Char('.'))
                ++m_pos;
            else if ((c == QLatin1Char('e') || c == QLatin1Char('E')) && m_pos + 1 < m_d.size()) {
                ++m_pos;
                if (m_d.at(m_pos) == QLatin1Char('-') || m_d.at(m_pos) == QLatin1Char('+'))
                    ++m_pos;
            } else
                break;
        }
        bool good = false;
        const qreal v = QStringView(m_d).mid(start, m_pos - start).toDouble(&good);
        if (!good)
            *ok = false;
        return v;
    }

    QPointF point(bool *ok)
    {
        const qreal x = number(ok);
        const qreal y = number(ok);
        return QPointF(x, y);
    }

    QString m_d;
    qsizetype m_pos = 0;
};

// Splits "U_{R1} = 10^{3}" into runs of normal / subscript / superscript text.
QVector<DiagramTextRun> parseRuns(const QString &text)
{
    QVector<DiagramTextRun> runs;
    QString buf;
    int i = 0;
    const int n = text.size();
    auto flush = [&](int level) {
        if (!buf.isEmpty()) {
            runs.append({buf, level});
            buf.clear();
        }
    };
    while (i < n) {
        const QChar c = text.at(i);
        if ((c == QLatin1Char('_') || c == QLatin1Char('^')) && i + 1 < n && text.at(i + 1) == QLatin1Char('{')) {
            const int close = text.indexOf(QLatin1Char('}'), i + 2);
            if (close > 0) {
                flush(0);
                buf = text.mid(i + 2, close - i - 2);
                flush(c == QLatin1Char('_') ? -1 : 1);
                i = close + 1;
                continue;
            }
        }
        buf.append(c);
        ++i;
    }
    flush(0);
    return runs;
}

QColor parseColor(const QJsonValue &v)
{
    if (!v.isString())
        return QColor();
    const QString s = v.toString();
    if (s.isEmpty() || s == QLatin1String("none"))
        return QColor();
    return QColor(s);
}

QFont makeFont(const DiagramOp &op, const DiagramTextRun *run, qreal size, QPaintDevice *device)
{
    QFont f(Diagram::familyName(op.family));
    const qreal dpi = device ? device->logicalDpiY() : 96.0;
    f.setPointSizeF(qMax<qreal>(0.5, size * 72.0 / dpi));
    f.setBold(run ? run->bold : op.bold);
    f.setItalic(run ? run->italic : op.italic);
    f.setUnderline(run ? run->underline : op.underline);
    f.setHintingPreference(QFont::PreferNoHinting);
    f.setStyleStrategy(QFont::PreferAntialias);
    return f;
}

QImage loadImage(const QString &name)
{
    static QHash<QString, QImage> cache;
    static QMutex mutex;
    QMutexLocker lock(&mutex);
    auto it = cache.find(name);
    if (it != cache.end())
        return it.value();
    QImage img(g_imageBasePath + name);
    cache.insert(name, img);
    return img;
}

} // namespace

// ---------------------------------------------------------------------------
// Diagram
// ---------------------------------------------------------------------------

QString Diagram::familyName(int family)
{
    switch (family) {
    case 1: return QStringLiteral("Liberation Sans");
    case 2: return QStringLiteral("Liberation Mono");
    default: return QStringLiteral("Liberation Serif");
    }
}

void Diagram::setImageBasePath(const QString &path)
{
    g_imageBasePath = path.endsWith(QLatin1Char('/')) ? path : path + QLatin1Char('/');
}

std::shared_ptr<Diagram> Diagram::fromJson(const QByteArray &json, QString *error)
{
    QJsonParseError perr;
    const QJsonDocument doc = QJsonDocument::fromJson(json, &perr);
    if (perr.error != QJsonParseError::NoError || !doc.isObject()) {
        if (error)
            *error = perr.errorString();
        return nullptr;
    }
    const QJsonObject root = doc.object();
    auto d = std::make_shared<Diagram>();
    d->m_size = QSizeF(root.value(QLatin1String("w")).toDouble(100), root.value(QLatin1String("h")).toDouble(100));
    const QJsonArray ops = root.value(QLatin1String("ops")).toArray();
    d->m_ops.reserve(ops.size());
    for (const QJsonValue &v : ops) {
        const QJsonObject o = v.toObject();
        DiagramOp op;
        if (o.contains(QLatin1String("p"))) {
            op.type = DiagramOp::Path;
            op.path = PathParser(o.value(QLatin1String("p")).toString()).parse();
            if (o.value(QLatin1String("eo")).toInt() == 1)
                op.path.setFillRule(Qt::OddEvenFill);
            else
                op.path.setFillRule(Qt::WindingFill);
            op.stroke = parseColor(o.value(QLatin1String("s")));
            op.fill = parseColor(o.value(QLatin1String("f")));
            op.lineWidth = o.value(QLatin1String("w")).toDouble(1.0);
            for (const QJsonValue &dv : o.value(QLatin1String("d")).toArray())
                op.dash.append(dv.toDouble());
            const QString cap = o.value(QLatin1String("c")).toString();
            op.cap = cap == QLatin1String("r") ? Qt::RoundCap : cap == QLatin1String("s") ? Qt::SquareCap : Qt::FlatCap;
            const QString join = o.value(QLatin1String("j")).toString();
            op.join = join == QLatin1String("r") ? Qt::RoundJoin : join == QLatin1String("b") ? Qt::BevelJoin : Qt::MiterJoin;
        } else if (o.contains(QLatin1String("t")) || o.contains(QLatin1String("R"))) {
            op.type = DiagramOp::Text;
            op.bold = o.value(QLatin1String("b")).toInt() == 1;
            op.italic = o.value(QLatin1String("i")).toInt() == 1;
            op.underline = o.value(QLatin1String("u")).toInt() == 1;
            if (o.contains(QLatin1String("R"))) {
                for (const QJsonValue &rv : o.value(QLatin1String("R")).toArray()) {
                    const QJsonObject ro = rv.toObject();
                    QVector<DiagramTextRun> parts = parseRuns(ro.value(QLatin1String("t")).toString());
                    for (DiagramTextRun &r : parts) {
                        r.bold = ro.contains(QLatin1String("b")) ? ro.value(QLatin1String("b")).toInt() == 1 : op.bold;
                        r.italic = ro.contains(QLatin1String("i")) ? ro.value(QLatin1String("i")).toInt() == 1 : op.italic;
                        r.underline = ro.contains(QLatin1String("u")) ? ro.value(QLatin1String("u")).toInt() == 1 : op.underline;
                        r.color = parseColor(ro.value(QLatin1String("s")));
                        op.runs.append(r);
                    }
                }
            } else {
                op.runs = parseRuns(o.value(QLatin1String("t")).toString());
                for (DiagramTextRun &r : op.runs) {
                    r.bold = op.bold;
                    r.italic = op.italic;
                    r.underline = op.underline;
                }
            }
            op.pos = QPointF(o.value(QLatin1String("x")).toDouble(), o.value(QLatin1String("y")).toDouble());
            op.size = o.value(QLatin1String("z")).toDouble(10.0);
            const QString fam = o.value(QLatin1String("F")).toString();
            op.family = fam == QLatin1String("sans") ? 1 : fam == QLatin1String("mono") ? 2 : 0;
            op.color = parseColor(o.value(QLatin1String("s")));
            if (!op.color.isValid())
                op.color = Qt::black;
            op.rotation = o.value(QLatin1String("r")).toDouble(0.0);
            op.hAlign = o.value(QLatin1String("a")).toInt(0);
            op.vAlign = o.value(QLatin1String("va")).toInt(0);
        } else if (o.contains(QLatin1String("img"))) {
            op.type = DiagramOp::Image;
            op.image = o.value(QLatin1String("img")).toString();
            op.rect = QRectF(o.value(QLatin1String("x")).toDouble(), o.value(QLatin1String("y")).toDouble(),
                             o.value(QLatin1String("w")).toDouble(), o.value(QLatin1String("h")).toDouble());
        } else {
            continue;
        }
        d->m_ops.append(op);
    }
    return d;
}

void Diagram::paint(QPainter *p, const QRectF &target, bool dark) const
{
    if (m_size.isEmpty() || target.isEmpty())
        return;
    const qreal s = qMin(target.width() / m_size.width(), target.height() / m_size.height());
    const QPointF origin(target.x() + (target.width() - m_size.width() * s) / 2.0,
                         target.y() + (target.height() - m_size.height() * s) / 2.0);

    p->save();
    p->setRenderHint(QPainter::Antialiasing, true);
    p->setRenderHint(QPainter::TextAntialiasing, true);
    p->setRenderHint(QPainter::SmoothPixmapTransform, true);
    p->translate(origin);
    p->scale(s, s);

    QPaintDevice *device = p->device();

    for (const DiagramOp &op : m_ops) {
        switch (op.type) {
        case DiagramOp::Path: {
            if (op.fill.isValid())
                p->fillPath(op.path, ThemeColors::map(op.fill, dark));
            if (op.stroke.isValid()) {
                QPen pen(ThemeColors::map(op.stroke, dark));
                pen.setWidthF(op.lineWidth);
                pen.setCapStyle(op.cap);
                pen.setJoinStyle(op.join);
                if (!op.dash.isEmpty() && op.lineWidth > 0) {
                    QVector<qreal> pattern;
                    pattern.reserve(op.dash.size());
                    for (qreal v : op.dash)
                        pattern.append(qMax<qreal>(0.01, v / op.lineWidth));
                    if (pattern.size() % 2)
                        pattern.append(pattern.last());
                    pen.setDashPattern(pattern);
                }
                p->strokePath(op.path, pen);
            }
            break;
        }
        case DiagramOp::Text: {
            const QColor color = ThemeColors::map(op.color, dark);
            // Measure runs.
            struct Placed { QFont font; QString text; qreal dy; qreal width; QColor color; };
            QVector<Placed> placed;
            qreal total = 0;
            qreal ascent = 0, descent = 0;
            for (const DiagramTextRun &run : op.runs) {
                const qreal sz = run.level == 0 ? op.size : op.size * 0.7;
                const QFont f = makeFont(op, &run, sz, device);
                const QFontMetricsF fm(f, device);
                const qreal w = fm.horizontalAdvance(run.text);
                const qreal dy = run.level < 0 ? op.size * 0.22 : run.level > 0 ? -op.size * 0.38 : 0.0;
                placed.append({f, run.text, dy, w, run.color.isValid() ? ThemeColors::map(run.color, dark) : color});
                total += w;
                if (run.level == 0) {
                    ascent = qMax(ascent, fm.ascent());
                    descent = qMax(descent, fm.descent());
                }
            }
            if (ascent == 0) {
                const QFontMetricsF fm(makeFont(op, nullptr, op.size, device), device);
                ascent = fm.ascent();
                descent = fm.descent();
            }
            qreal x0 = 0;
            if (op.hAlign == 1)
                x0 = -total / 2.0;
            else if (op.hAlign == 2)
                x0 = -total;
            qreal y0 = 0;
            if (op.vAlign == 1)
                y0 = (ascent - descent) / 2.0 * 0.85;
            else if (op.vAlign == 2)
                y0 = ascent * 0.8;

            p->save();
            p->translate(op.pos);
            if (!qFuzzyIsNull(op.rotation))
                p->rotate(op.rotation);
            qreal x = x0;
            for (const Placed &pl : placed) {
                p->setPen(pl.color);
                p->setFont(pl.font);
                p->drawText(QPointF(x, y0 + pl.dy), pl.text);
                x += pl.width;
            }
            p->restore();
            break;
        }
        case DiagramOp::Image: {
            const QImage img = loadImage(op.image);
            if (!img.isNull())
                p->drawImage(op.rect, img);
            break;
        }
        }
    }
    p->restore();
}

// ---------------------------------------------------------------------------
// DiagramStore
// ---------------------------------------------------------------------------

QMutex DiagramStore::s_mutex;
QHash<QString, std::shared_ptr<const Diagram>> DiagramStore::s_cache;
QString DiagramStore::s_basePath = QStringLiteral(":/content/figures/");

void DiagramStore::setBasePath(const QString &path)
{
    QMutexLocker lock(&s_mutex);
    s_basePath = path.endsWith(QLatin1Char('/')) ? path : path + QLatin1Char('/');
    s_cache.clear();
}

QString DiagramStore::basePath()
{
    QMutexLocker lock(&s_mutex);
    return s_basePath;
}

std::shared_ptr<const Diagram> DiagramStore::get(const QString &id)
{
    if (id.isEmpty())
        return nullptr;
    QMutexLocker lock(&s_mutex);
    auto it = s_cache.find(id);
    if (it != s_cache.end())
        return it.value();
    QFile f(s_basePath + id + QStringLiteral(".json"));
    std::shared_ptr<const Diagram> d;
    if (f.open(QIODevice::ReadOnly))
        d = Diagram::fromJson(f.readAll());
    s_cache.insert(id, d);
    return d;
}

void registerBundledFonts(const QString &directory)
{
    static const char *files[] = {
        "LiberationSerif-Regular.ttf", "LiberationSerif-Bold.ttf",
        "LiberationSerif-Italic.ttf", "LiberationSerif-BoldItalic.ttf",
        "LiberationSans-Regular.ttf", "LiberationSans-Bold.ttf",
        "LiberationSans-Italic.ttf", "LiberationSans-BoldItalic.ttf",
        "CoursRadioSymbols.ttf",
    };
    const QString dir = directory.endsWith(QLatin1Char('/')) ? directory : directory + QLatin1Char('/');
    for (const char *f : files)
        QFontDatabase::addApplicationFont(dir + QLatin1String(f));

    // Characters missing from the Liberation fonts (arrows, mathematical
    // operators, geometric shapes) come from the bundled symbol font before
    // the system fallbacks, which do not always have them (Android shows a
    // box for "▸" or "⇒").
    const QString symbols = QStringLiteral("CoursRadio Symbols");
    for (const char *family : {"Liberation Serif", "Liberation Sans", "Liberation Mono"})
        QFont::insertSubstitution(QLatin1String(family), symbols);
}
