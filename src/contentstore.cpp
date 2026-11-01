#include "contentstore.h"
#include "themecolors.h"

#include <QFile>
#include <QJsonDocument>
#include <QRegularExpression>

static const QString kContentRoot = QStringLiteral(":/content/");

ContentStore::ContentStore(QObject *parent)
    : QObject(parent)
{
    m_courseIndex = loadJson(kContentRoot + QStringLiteral("course/index.json"));

    const QJsonObject anchors = m_courseIndex.value(QLatin1String("anchors")).toObject();
    for (auto it = anchors.begin(); it != anchors.end(); ++it) {
        const QJsonArray a = it.value().toArray();
        m_anchors.insert(it.key(), qMakePair(a.at(0).toString(), a.at(1).toInt()));
    }
}

QJsonObject ContentStore::loadJson(const QString &path) const
{
    QFile f(path);
    if (!f.open(QIODevice::ReadOnly)) {
        qWarning("ContentStore: cannot open %s", qPrintable(path));
        return {};
    }
    QJsonParseError err;
    const QJsonDocument doc = QJsonDocument::fromJson(f.readAll(), &err);
    if (err.error != QJsonParseError::NoError)
        qWarning("ContentStore: %s: %s", qPrintable(path), qPrintable(err.errorString()));
    return doc.object();
}

// ---------------------------------------------------------------------------
// Course
// ---------------------------------------------------------------------------

QVariantList ContentStore::courseParts() const
{
    return m_courseIndex.value(QLatin1String("parts")).toArray().toVariantList();
}

QVariantList ContentStore::chapterOrder() const
{
    QVariantList out;
    const QJsonArray parts = m_courseIndex.value(QLatin1String("parts")).toArray();
    for (const QJsonValue &pv : parts) {
        const QJsonObject p = pv.toObject();
        for (const QJsonValue &cv : p.value(QLatin1String("chapters")).toArray()) {
            const QJsonObject c = cv.toObject();
            out.append(QVariantMap{
                {QStringLiteral("id"), c.value(QLatin1String("id")).toString()},
                {QStringLiteral("title"), c.value(QLatin1String("title")).toString()},
                {QStringLiteral("part"), p.value(QLatin1String("title")).toString()},
            });
        }
    }
    return out;
}

QVariantMap ContentStore::chapter(const QString &id) const
{
    auto it = m_chapterCache.constFind(id);
    if (it != m_chapterCache.constEnd())
        return it.value();
    const QVariantMap map = loadJson(kContentRoot + QStringLiteral("course/") + id + QStringLiteral(".json")).toVariantMap();
    m_chapterCache.insert(id, map);
    return map;
}

QVariantMap ContentStore::locate(const QString &anchor) const
{
    // Exact anchor, then progressively less precise: "T-2.3g1" -> "T-2.3g"
    // -> "T-2.3" -> "T-2".
    QString key = anchor.trimmed();
    static const QRegularExpression trailingDigits(QStringLiteral("(?<=[a-z])\\d+$"));
    static const QRegularExpression trailingLetter(QStringLiteral("(?<=\\d)[a-z]$"));
    static const QRegularExpression trailingSection(QStringLiteral("\\.\\d+$"));
    for (int guard = 0; guard < 4 && !key.isEmpty(); ++guard) {
        auto it = m_anchors.constFind(key);
        if (it != m_anchors.constEnd()) {
            return {
                {QStringLiteral("chapter"), it.value().first},
                {QStringLiteral("block"), it.value().second},
                {QStringLiteral("found"), true},
                {QStringLiteral("exact"), key == anchor.trimmed()},
            };
        }
        QString next = key;
        if (next.contains(trailingDigits))
            next.remove(trailingDigits);
        else if (next.contains(trailingLetter))
            next.remove(trailingLetter);
        else if (next.contains(trailingSection))
            next.remove(trailingSection);
        if (next == key)
            break;
        key = next;
    }
    return {{QStringLiteral("found"), false}};
}

// ---------------------------------------------------------------------------

QString ContentStore::themed(const QString &html, bool dark) const
{
    return ThemeColors::mapHtml(html, dark);
}
