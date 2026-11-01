#include "diagramitem.h"
#include "diagram.h"

#include <QPainter>

// 1 PDF point is displayed as 4/3 device independent pixels (96 dpi).
static constexpr qreal kPointToPixel = 4.0 / 3.0;

DiagramItem::DiagramItem(QQuickItem *parent)
    : QQuickPaintedItem(parent)
{
    setAntialiasing(true);
    setOpaquePainting(false);
}

void DiagramItem::setSource(const QString &source)
{
    if (source == m_source)
        return;
    m_source = source;
    m_diagram = DiagramStore::get(source);
    if (m_diagram) {
        setImplicitWidth(m_diagram->size().width() * kPointToPixel);
        setImplicitHeight(m_diagram->size().height() * kPointToPixel);
    } else {
        setImplicitWidth(0);
        setImplicitHeight(0);
    }
    emit sourceChanged();
    update();
}

void DiagramItem::setDark(bool dark)
{
    if (dark == m_dark)
        return;
    m_dark = dark;
    emit darkChanged();
    update();
}

qreal DiagramItem::naturalWidth() const
{
    return m_diagram ? m_diagram->size().width() * kPointToPixel : 0.0;
}

qreal DiagramItem::naturalHeight() const
{
    return m_diagram ? m_diagram->size().height() * kPointToPixel : 0.0;
}

void DiagramItem::paint(QPainter *painter)
{
    if (!m_diagram)
        return;
    m_diagram->paint(painter, QRectF(0, 0, width(), height()), m_dark);
}
