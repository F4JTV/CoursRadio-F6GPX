// Read-only access to the bundled course (JSON resources),
// exposed to QML as the ContentStore singleton.
#pragma once

#include <QHash>
#include <QJsonArray>
#include <QJsonObject>
#include <QObject>
#include <QVariant>
#include <QtQml/qqmlregistration.h>

class ContentStore : public QObject
{
    Q_OBJECT
    QML_ELEMENT
    QML_SINGLETON

public:
    explicit ContentStore(QObject *parent = nullptr);

    // Course ---------------------------------------------------------------
    // [{id, title, chapters: [{id, title, subtitle, sections: [{anchor, title}]}]}]
    Q_INVOKABLE QVariantList courseParts() const;
    // Chapters in reading order: [{id, title, part}]
    Q_INVOKABLE QVariantList chapterOrder() const;
    // {id, title, part, blocks: [...]}
    Q_INVOKABLE QVariantMap chapter(const QString &id) const;
    // {chapter, block, found} for an anchor such as "T-1.7d"
    Q_INVOKABLE QVariantMap locate(const QString &anchor) const;

    // Rich text ------------------------------------------------------------
    // Maps the colours of an HTML fragment onto the requested theme.
    Q_INVOKABLE QString themed(const QString &html, bool dark) const;

private:
    QJsonObject loadJson(const QString &path) const;

    QJsonObject m_courseIndex;
    mutable QHash<QString, QVariantMap> m_chapterCache;
    QHash<QString, QPair<QString, int>> m_anchors;
};
