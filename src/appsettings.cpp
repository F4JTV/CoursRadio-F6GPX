#include "appsettings.h"

#include <QtMath>

AppSettings::AppSettings(QObject *parent)
    : QObject(parent)
{
    m_dark = m_settings.value(QStringLiteral("ui/dark"), false).toBool();
    m_textScale = m_settings.value(QStringLiteral("ui/textScale"), 1.0).toReal();
    m_lastChapter = m_settings.value(QStringLiteral("reading/chapter")).toString();
    m_lastBlock = m_settings.value(QStringLiteral("reading/block"), 0).toInt();
}

void AppSettings::setDark(bool dark)
{
    if (dark == m_dark)
        return;
    m_dark = dark;
    m_settings.setValue(QStringLiteral("ui/dark"), dark);
    emit darkChanged();
}

void AppSettings::setTextScale(qreal scale)
{
    scale = qBound<qreal>(0.8, scale, 1.6);
    if (qFuzzyCompare(scale, m_textScale))
        return;
    m_textScale = scale;
    m_settings.setValue(QStringLiteral("ui/textScale"), scale);
    emit textScaleChanged();
}

void AppSettings::setLastChapter(const QString &id)
{
    if (id == m_lastChapter)
        return;
    m_lastChapter = id;
    m_settings.setValue(QStringLiteral("reading/chapter"), id);
    emit lastChapterChanged();
}

void AppSettings::setLastBlock(int index)
{
    if (index == m_lastBlock)
        return;
    m_lastBlock = index;
    m_settings.setValue(QStringLiteral("reading/block"), index);
    emit lastBlockChanged();
}
