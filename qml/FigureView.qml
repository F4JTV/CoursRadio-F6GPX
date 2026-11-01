import QtQuick
import QtQuick.Controls
import CoursRadio

// A schematic fitted to the available width (never wider than `maxScale`
// times its natural size).  When `minScale` is set (figures containing
// text, tables), the figure is never shrunk below it: on narrow screens it
// scrolls horizontally instead.  Tapping it opens the zoomable viewer.
Item {
    id: root

    property string figureId
    property string caption
    property real maxScale: 1.5
    property real minScale: 0
    property bool zoomable: true

    readonly property real fitScale: diagram.naturalWidth > 0 ? Math.min(maxScale, width / diagram.naturalWidth) : 1
    readonly property real scale_: Math.max(fitScale, minScale)
    readonly property bool scrolls: diagram.naturalWidth * scale_ > width + 1

    implicitWidth: diagram.naturalWidth * maxScale
    implicitHeight: diagram.naturalHeight * scale_ + (scrolls ? 10 : 0)

    Flickable {
        id: flick
        anchors.fill: parent
        contentWidth: Math.max(width, diagram.width)
        contentHeight: diagram.height
        flickableDirection: Flickable.HorizontalFlick
        boundsBehavior: Flickable.StopAtBounds
        interactive: root.scrolls
        clip: root.scrolls
        ScrollBar.horizontal: ScrollBar { policy: root.scrolls ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff }

        Diagram {
            id: diagram
            source: root.figureId
            dark: Style.dark
            width: naturalWidth * root.scale_
            height: naturalHeight * root.scale_
            x: root.scrolls ? 0 : (flick.width - width) / 2
        }

        TapHandler {
            enabled: root.zoomable && diagram.valid
            onTapped: window.openFigure(root.figureId, root.caption)
        }
    }

    Rectangle {
        visible: root.zoomable && hover.hovered
        x: Math.min(root.width, diagram.x + diagram.width) - width - 2
        y: 2
        width: 28
        height: 28
        radius: 14
        color: Style.purple
        opacity: 0.85
        Image {
            anchors.centerIn: parent
            source: Style.dark ? "qrc:/icons/zoom-in-dark.png" : "qrc:/icons/zoom-in.png"
            sourceSize: Qt.size(18, 18)
        }
    }

    HoverHandler { id: hover; enabled: root.zoomable }
}
