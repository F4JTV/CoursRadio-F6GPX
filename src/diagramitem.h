// QML element drawing a native vector diagram (see diagram.h).
#pragma once

#include <QQuickPaintedItem>
#include <QtQml/qqmlregistration.h>
#include <memory>

class Diagram;

class DiagramItem : public QQuickPaintedItem
{
    Q_OBJECT
    QML_NAMED_ELEMENT(Diagram)
    Q_PROPERTY(QString source READ source WRITE setSource NOTIFY sourceChanged)
    Q_PROPERTY(bool dark READ dark WRITE setDark NOTIFY darkChanged)
    Q_PROPERTY(qreal naturalWidth READ naturalWidth NOTIFY sourceChanged)
    Q_PROPERTY(qreal naturalHeight READ naturalHeight NOTIFY sourceChanged)
    Q_PROPERTY(bool valid READ valid NOTIFY sourceChanged)

public:
    explicit DiagramItem(QQuickItem *parent = nullptr);

    QString source() const { return m_source; }
    void setSource(const QString &source);

    bool dark() const { return m_dark; }
    void setDark(bool dark);

    // Size of the diagram in PDF points.
    qreal naturalWidth() const;
    qreal naturalHeight() const;
    bool valid() const { return bool(m_diagram); }

    void paint(QPainter *painter) override;

signals:
    void sourceChanged();
    void darkChanged();

private:
    QString m_source;
    bool m_dark = false;
    std::shared_ptr<const Diagram> m_diagram;
};
