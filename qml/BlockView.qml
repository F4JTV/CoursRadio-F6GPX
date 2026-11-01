import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import CoursRadio

// One block of a chapter: title, paragraph, example, schematic, table...
Loader {
    id: root

    property var block: ({})
    readonly property string kind: block.t || "p"
    readonly property real indentPx: Math.min((block.indent || 0) * 1.25, width * 0.18)
    // Justify only when a line holds enough words (about 70 characters):
    // on a narrow column the slack of each line goes into a few spaces and
    // leaves wide, uneven gaps, so the text is left-aligned there.
    readonly property bool justify: width - indentPx >= 32 * Style.bodySize

    sourceComponent: {
        switch (kind) {
        case "part": return partComponent
        case "section": return sectionComponent
        case "chapter": return chapterComponent
        case "heading": return headingComponent
        case "fig": return figureComponent
        case "table": return tableComponent
        case "img": return imageComponent
        case "space": return spaceComponent
        default: return paragraphComponent
        }
    }

    Component {
        id: partComponent
        Label {
            topPadding: 24
            bottomPadding: 8
            text: root.block.text
            color: Style.purple
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.Wrap
            font.family: Style.sans
            font.bold: true
            font.italic: true
            font.pixelSize: 24 * Style.textScale
        }
    }

    Component {
        id: sectionComponent
        Label {
            topPadding: 18
            bottomPadding: 6
            text: root.block.text
            color: Style.purple
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.Wrap
            font.family: Style.sans
            font.bold: true
            font.italic: true
            font.pixelSize: 20 * Style.textScale
        }
    }

    Component {
        id: chapterComponent
        RichLabel {
            topPadding: 20
            bottomPadding: 10
            html: root.block.html
            serif: false
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.italic: true
            font.pixelSize: 25 * Style.textScale
            color: Style.purple
        }
    }

    Component {
        id: headingComponent
        RichLabel {
            topPadding: 18
            bottomPadding: 4
            leftPadding: root.indentPx
            html: root.block.html
            serif: true
            font.pixelSize: Style.bodySize
        }
    }

    Component {
        id: paragraphComponent
        RichLabel {
            topPadding: root.block.gap ? 8 : 3
            bottomPadding: 3
            leftPadding: root.indentPx
            html: root.block.html
            serif: root.kind !== "ex"
            horizontalAlignment: root.block.align === "center" ? Text.AlignHCenter
                               : root.block.align === "right" ? Text.AlignRight
                               : root.block.align === "left" || !root.justify ? Text.AlignLeft
                               : Text.AlignJustify
            font.pixelSize: root.kind === "ex" ? Style.bodySize * 0.94 : Style.bodySize
            lineHeight: 1.08
        }
    }

    Component {
        id: figureComponent
        Item {
            implicitHeight: fig.implicitHeight + 16
            FigureView {
                id: fig
                y: 8
                x: root.indentPx
                width: parent.width - root.indentPx
                figureId: root.block.id
                maxScale: root.block.maxScale || 1.35
                // keep the text of figures and tables legible (>= 10.5 px)
                minScale: root.block.min ? Math.min(1.35, 10.5 / (root.block.min * 4 / 3)) : 0
            }
        }
    }

    Component {
        id: tableComponent
        TableBlock {
            topPadding: root.block.plain ? 2 : 8
            bottomPadding: root.block.plain ? 4 : 8
            leftPadding: root.indentPx
            table: root.block
        }
    }

    Component {
        id: imageComponent
        Item {
            implicitHeight: photo.height + 16
            Image {
                id: photo
                y: 8
                anchors.horizontalCenter: parent.horizontalCenter
                source: "qrc:/content/images/" + root.block.src
                fillMode: Image.PreserveAspectFit
                width: Math.min(parent.width, (root.block.w || 300) * 1.4)
                height: width * (root.block.h || 200) / (root.block.w || 300)
                smooth: true
                mipmap: true
            }
        }
    }

    Component {
        id: spaceComponent
        Item { implicitHeight: (root.block.h || 8) }
    }
}
