import QtQuick
import QtQuick.Controls
import CoursRadio

// Push button with a flat, theme-aware look (identical on every platform).
AbstractButton {
    id: button

    property bool primary: false
    property bool quiet: false

    hoverEnabled: true
    focusPolicy: Qt.StrongFocus
    implicitHeight: 42
    implicitWidth: Math.max(96, label.implicitWidth + 32)
    opacity: enabled ? 1 : 0.4
    Accessible.role: Accessible.Button
    Accessible.name: text

    background: Rectangle {
        radius: 21
        color: button.primary ? (button.down ? Qt.darker(Style.purple, 1.2) : button.hovered ? Qt.lighter(Style.purple, 1.1) : Style.purple)
                              : button.quiet ? (button.down ? Style.surfaceStrong : "transparent")
                              : (button.down ? Style.surfaceStrong : Style.surface)
        border.width: button.primary || button.quiet ? (button.visualFocus ? 2 : 0) : 1
        border.color: button.visualFocus ? Style.navy : Style.divider
    }

    contentItem: Label {
        id: label
        text: button.text
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
        color: button.primary ? Style.onPurple : Style.purple
        font.bold: true
        font.pixelSize: 15
    }
}
