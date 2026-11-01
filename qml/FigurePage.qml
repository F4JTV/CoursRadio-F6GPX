import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import CoursRadio

// Full-screen, zoomable view of one schematic (pinch, wheel or buttons).
Page {
    id: page

    property string figureId
    property string caption
    property real zoom: 1.0

    title: caption !== "" ? caption : qsTr("Schéma")
    background: Rectangle { color: Style.paper }

    readonly property real fitScale: diagram.naturalWidth > 0
        ? Math.min((flick.width - 24) / diagram.naturalWidth, (flick.height - 24) / diagram.naturalHeight)
        : 1
    readonly property real scaleFactor: fitScale * zoom

    function setZoom(z, cx, cy) {
        const old = scaleFactor
        z = Math.max(0.5, Math.min(z, 8 / Math.max(fitScale, 0.01)))
        // keep the point under (cx, cy) in place
        const px = (flick.contentX + cx) / old
        const py = (flick.contentY + cy) / old
        zoom = z
        flick.contentX = Math.max(0, px * scaleFactor - cx)
        flick.contentY = Math.max(0, py * scaleFactor - cy)
    }

    Flickable {
        id: flick
        anchors.fill: parent
        anchors.bottomMargin: bar.height
        contentWidth: Math.max(width, diagram.width + 24)
        contentHeight: Math.max(height, diagram.height + 24)
        clip: true
        boundsBehavior: Flickable.StopAtBounds
        ScrollBar.vertical: ScrollBar {}
        ScrollBar.horizontal: ScrollBar {}

        PinchArea {
            width: flick.contentWidth
            height: flick.contentHeight
            property real startZoom: 1
            onPinchStarted: startZoom = page.zoom
            onPinchUpdated: function(pinch) {
                page.setZoom(startZoom * pinch.scale, pinch.center.x - flick.contentX, pinch.center.y - flick.contentY)
            }

            Diagram {
                id: diagram
                source: page.figureId
                dark: Style.dark
                width: naturalWidth * page.scaleFactor
                height: naturalHeight * page.scaleFactor
                x: (flick.contentWidth - width) / 2
                y: (flick.contentHeight - height) / 2
            }

            WheelHandler {
                acceptedModifiers: Qt.ControlModifier
                onWheel: function(event) {
                    page.setZoom(page.zoom * (event.angleDelta.y > 0 ? 1.15 : 1 / 1.15),
                                 event.x - flick.contentX, event.y - flick.contentY)
                }
            }

            TapHandler {
                onDoubleTapped: function(eventPoint) {
                    page.setZoom(page.zoom > 1.5 ? 1 : 2.5,
                                 eventPoint.position.x - flick.contentX, eventPoint.position.y - flick.contentY)
                }
            }
        }
    }

    ToolBar {
        id: bar
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        background: Rectangle { color: Style.surface; border.color: Style.divider }

        RowLayout {
            anchors.centerIn: parent
            spacing: 8
            ToolButton {
                icon.source: "qrc:/icons/zoom-out.png"
                icon.color: Style.ink
                onClicked: page.setZoom(page.zoom / 1.4, flick.width / 2, flick.height / 2)
                Accessible.name: qsTr("Réduire")
            }
            Label {
                text: Math.round(page.zoom * 100) + " %"
                color: Style.ink
                Layout.preferredWidth: 60
                horizontalAlignment: Text.AlignHCenter
            }
            ToolButton {
                icon.source: "qrc:/icons/zoom-in.png"
                icon.color: Style.ink
                onClicked: page.setZoom(page.zoom * 1.4, flick.width / 2, flick.height / 2)
                Accessible.name: qsTr("Agrandir")
            }
            ToolButton {
                icon.source: "qrc:/icons/fit.png"
                icon.color: Style.ink
                onClicked: { page.zoom = 1; flick.contentX = 0; flick.contentY = 0 }
                Accessible.name: qsTr("Ajuster à l’écran")
            }
        }
    }
}
