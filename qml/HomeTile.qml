import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import CoursRadio

// Large navigation tile of the home page.
AbstractButton {
    id: tile

    property string heading
    property string detail
    property string glyph
    property color accent: Style.purple
    signal activated()

    implicitHeight: Math.max(150, content.implicitHeight + 40)
    hoverEnabled: true
    onClicked: activated()
    Accessible.name: heading

    background: Rectangle {
        radius: 14
        color: tile.down ? Style.surfaceStrong : Style.surface
        border.width: tile.hovered || tile.activeFocus ? 2 : 1
        border.color: tile.hovered || tile.activeFocus ? tile.accent : Style.divider
    }

    contentItem: RowLayout {
        id: content
        spacing: 18

        Rectangle {
            Layout.alignment: Qt.AlignVCenter
            Layout.leftMargin: 4
            width: 64
            height: 64
            radius: 32
            color: tile.accent
            Label {
                anchors.centerIn: parent
                text: tile.glyph
                color: Style.onPurple
                font.family: Style.serif
                font.bold: true
                font.pixelSize: 34
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignVCenter
            spacing: 6
            Label {
                Layout.fillWidth: true
                text: tile.heading
                color: tile.accent
                font.family: Style.serif
                font.bold: true
                font.italic: true
                font.pixelSize: 26 * Style.textScale
            }
            Label {
                Layout.fillWidth: true
                text: tile.detail
                color: Style.ink
                wrapMode: Text.Wrap
                font.pixelSize: 15 * Style.textScale
            }
        }
    }
}
