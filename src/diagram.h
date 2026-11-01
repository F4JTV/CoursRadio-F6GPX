// Native vector diagrams.
//
// Every schematic of the course is stored as a small JSON document made of
// drawing operations (paths, text labels and, for the few photographs, an
// image).  Coordinates are expressed in PDF points (1/72 inch) so that the
// geometry matches the original course exactly.  The same painting code is
// used by the QML item (DiagramItem) and by the command-line preview tool.
//
// JSON format (version 1):
// {
//   "w": <width>, "h": <height>,
//   "ops": [
//     { "p": "M x y L x y C x1 y1 x2 y2 x y Q x1 y1 x y H x V y Z",
//       "s": "#rrggbb" (stroke, optional), "f": "#rrggbb" (fill, optional),
//       "w": <line width>, "d": [dash, gap, ...], "c": "b|r|s" (cap),
//       "j": "m|r|b" (join), "eo": 1 (even-odd fill) },
//     { "t": "text with _{sub} and ^{sup}", "x": .., "y": .. (baseline),
//       "R": [{"t": "..", "b": 1, "i": 1, "u": 1, "s": "#rrggbb"}, ...]
//            (optional styled runs replacing "t", laid out one after the other),
//       "z": <font size>, "F": "serif|sans|mono", "b": 1, "i": 1, "u": 1,
//       "s": "#rrggbb", "r": <rotation in degrees>,
//       "a": 0|1|2 (left|centre|right), "va": 0|1|2 (baseline|middle|top) },
//     { "img": "file.jpg", "x": .., "y": .., "w": .., "h": .. }
//   ]
// }
#pragma once

#include <QColor>
#include <QHash>
#include <QMutex>
#include <QPainterPath>
#include <QRectF>
#include <QSizeF>
#include <QString>
#include <QVector>
#include <memory>

class QPainter;

struct DiagramTextRun
{
    QString text;
    int level = 0; // 0 normal, -1 subscript, +1 superscript
    bool bold = false;
    bool italic = false;
    bool underline = false;
    QColor color;  // invalid: colour of the operation
};

struct DiagramOp
{
    enum Type { Path, Text, Image };
    Type type = Path;

    // Path
    QPainterPath path;
    QColor stroke;
    QColor fill;
    qreal lineWidth = 1.0;
    QVector<qreal> dash;
    Qt::PenCapStyle cap = Qt::FlatCap;
    Qt::PenJoinStyle join = Qt::MiterJoin;

    // Text
    QVector<DiagramTextRun> runs;
    QPointF pos;
    qreal size = 10.0;
    int family = 0; // 0 serif, 1 sans, 2 mono
    bool bold = false;
    bool italic = false;
    bool underline = false;
    qreal rotation = 0.0;
    int hAlign = 0;
    int vAlign = 0;
    QColor color;

    // Image
    QString image;
    QRectF rect;
};

class Diagram
{
public:
    static std::shared_ptr<Diagram> fromJson(const QByteArray &json, QString *error = nullptr);

    QSizeF size() const { return m_size; }
    const QVector<DiagramOp> &ops() const { return m_ops; }

    // Paints the diagram scaled to fit `target` (aspect ratio preserved,
    // centred).  `dark` selects the colour mapping of the dark theme.
    void paint(QPainter *painter, const QRectF &target, bool dark) const;

    static QString familyName(int family);
    static void setImageBasePath(const QString &path);

private:
    QSizeF m_size;
    QVector<DiagramOp> m_ops;
};

// Loads diagrams on demand and keeps them cached.
class DiagramStore
{
public:
    static void setBasePath(const QString &path);
    static QString basePath();
    static std::shared_ptr<const Diagram> get(const QString &id);

private:
    static QMutex s_mutex;
    static QHash<QString, std::shared_ptr<const Diagram>> s_cache;
    static QString s_basePath;
};

// Registers the bundled Liberation fonts (metric-compatible with the
// Times New Roman / Arial fonts of the original document) and the
// "CoursRadio Symbols" font as their fallback for the symbols they lack.
void registerBundledFonts(const QString &directory);
