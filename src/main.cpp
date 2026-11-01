// Cours Radioamateur - course for the French amateur radio
// operator certificate, after the course written by F6GPX for the
// Radio-Club de la Haute Ile (F6KGL / F5KFF), CC BY-NC-SA 4.0.
#include "diagram.h"

#include <QGuiApplication>
#include <QIcon>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QQuickStyle>
#include <QQuickWindow>
#include <QUrl>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    QGuiApplication::setOrganizationName(QStringLiteral("CoursRadio"));
    QGuiApplication::setOrganizationDomain(QStringLiteral("coursradio.org"));
    QGuiApplication::setApplicationName(QStringLiteral("CoursRadio"));
    QGuiApplication::setApplicationDisplayName(QStringLiteral("Cours Radioamateur"));
    QGuiApplication::setApplicationVersion(QStringLiteral(COURSRADIO_VERSION));
    QGuiApplication::setWindowIcon(QIcon(QStringLiteral(":/icons/coursradio.png")));

    registerBundledFonts(QStringLiteral(":/fonts"));
    QQuickStyle::setStyle(QStringLiteral("Material"));

    QQmlApplicationEngine engine;
    engine.addImportPath(QStringLiteral("qrc:/"));
    engine.rootContext()->setContextProperty(QStringLiteral("appVersion"), QStringLiteral(COURSRADIO_VERSION));
    engine.rootContext()->setContextProperty(QStringLiteral("captureDir"), qEnvironmentVariable("COURSRADIO_CAPTURE_DIR"));
    engine.rootContext()->setContextProperty(QStringLiteral("capturePlan"), qEnvironmentVariable("COURSRADIO_CAPTURE_PLAN"));

    const QUrl url(QStringLiteral("qrc:/CoursRadio/Main.qml"));
    QObject::connect(
        &engine, &QQmlApplicationEngine::objectCreated, &app,
        [url](QObject *obj, const QUrl &objUrl) {
            if (!obj && url == objUrl)
                QCoreApplication::exit(-1);
        },
        Qt::QueuedConnection);
    engine.load(url);

    return app.exec();
}
