// figrender - renders native diagram JSON files to PNG with the exact same
// painting code as the application.  Used to check every redrawn schematic
// against the original course.
//
// Usage:
//   figrender [--scale S] [--dark] [--fonts DIR] [--images DIR] <in.json|dir> <out.png|dir>
#include "../../src/diagram.h"
#include "../../src/themecolors.h"

#include <QCommandLineParser>
#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QGuiApplication>
#include <QImage>
#include <QPainter>
#include <cstdio>

static bool renderOne(const QString &in, const QString &out, qreal scale, bool dark)
{
    QFile f(in);
    if (!f.open(QIODevice::ReadOnly)) {
        std::fprintf(stderr, "cannot open %s\n", qPrintable(in));
        return false;
    }
    QString err;
    auto d = Diagram::fromJson(f.readAll(), &err);
    if (!d) {
        std::fprintf(stderr, "%s: %s\n", qPrintable(in), qPrintable(err));
        return false;
    }
    const QSize px(qMax(1, qRound(d->size().width() * scale)), qMax(1, qRound(d->size().height() * scale)));
    QImage img(px, QImage::Format_ARGB32_Premultiplied);
    img.setDotsPerMeterX(3780);
    img.setDotsPerMeterY(3780);
    img.fill(ThemeColors::paper(dark));
    QPainter p(&img);
    d->paint(&p, QRectF(QPointF(0, 0), QSizeF(px)), dark);
    p.end();
    return img.save(out);
}

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);
    QCommandLineParser parser;
    parser.addHelpOption();
    QCommandLineOption scaleOpt(QStringList{"s", "scale"}, "Pixels per point.", "scale", "3");
    QCommandLineOption darkOpt(QStringList{"dark"}, "Use the dark theme colours.");
    QCommandLineOption fontsOpt(QStringList{"fonts"}, "Font directory.", "dir");
    QCommandLineOption imagesOpt(QStringList{"images"}, "Image directory.", "dir");
    parser.addOption(scaleOpt);
    parser.addOption(darkOpt);
    parser.addOption(fontsOpt);
    parser.addOption(imagesOpt);
    parser.addPositionalArgument("input", "JSON file or directory");
    parser.addPositionalArgument("output", "PNG file or directory");
    parser.process(app);

    const QStringList pos = parser.positionalArguments();
    if (pos.size() < 2)
        parser.showHelp(1);
    if (parser.isSet(fontsOpt))
        registerBundledFonts(parser.value(fontsOpt));
    if (parser.isSet(imagesOpt))
        Diagram::setImageBasePath(parser.value(imagesOpt));
    const qreal scale = parser.value(scaleOpt).toDouble();
    const bool dark = parser.isSet(darkOpt);

    const QFileInfo in(pos.at(0));
    if (in.isDir()) {
        QDir().mkpath(pos.at(1));
        int failures = 0;
        const QStringList files = QDir(in.absoluteFilePath()).entryList({"*.json"}, QDir::Files, QDir::Name);
        for (const QString &name : files) {
            const QString out = QDir(pos.at(1)).filePath(QFileInfo(name).completeBaseName() + ".png");
            if (!renderOne(QDir(in.absoluteFilePath()).filePath(name), out, scale, dark))
                ++failures;
        }
        std::printf("rendered %d file(s), %d failure(s)\n", int(files.size()) - failures, failures);
        return failures ? 2 : 0;
    }
    return renderOne(pos.at(0), pos.at(1), scale, dark) ? 0 : 2;
}
