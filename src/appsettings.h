// Persistent user preferences exposed to QML as the AppSettings singleton.
#pragma once

#include <QObject>
#include <QSettings>
#include <QtQml/qqmlregistration.h>

class AppSettings : public QObject
{
    Q_OBJECT
    QML_ELEMENT
    QML_SINGLETON
    Q_PROPERTY(bool dark READ dark WRITE setDark NOTIFY darkChanged)
    Q_PROPERTY(qreal textScale READ textScale WRITE setTextScale NOTIFY textScaleChanged)
    Q_PROPERTY(QString lastChapter READ lastChapter WRITE setLastChapter NOTIFY lastChapterChanged)
    Q_PROPERTY(int lastBlock READ lastBlock WRITE setLastBlock NOTIFY lastBlockChanged)

public:
    explicit AppSettings(QObject *parent = nullptr);

    bool dark() const { return m_dark; }
    void setDark(bool dark);

    qreal textScale() const { return m_textScale; }
    void setTextScale(qreal scale);

    QString lastChapter() const { return m_lastChapter; }
    void setLastChapter(const QString &id);

    int lastBlock() const { return m_lastBlock; }
    void setLastBlock(int index);

signals:
    void darkChanged();
    void textScaleChanged();
    void lastChapterChanged();
    void lastBlockChanged();

private:
    QSettings m_settings;
    bool m_dark = false;
    qreal m_textScale = 1.0;
    QString m_lastChapter;
    int m_lastBlock = 0;
};
