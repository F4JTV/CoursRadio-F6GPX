import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import CoursRadio

// A table of the course (merged cells, rich text and schematics in cells).
// Tables wider than the screen scroll horizontally.
Control {
    id: root

    property var table: ({})
    readonly property bool plain: table.plain === true
    readonly property var widths: table.widths || []
    readonly property real naturalWidth: widths.reduce((a, b) => a + b, 0) * 1.3
    readonly property real tableWidth: plain ? (widths.length <= 2 ? availableWidth : Math.max(availableWidth, Math.min(naturalWidth * 1.15, 640)))
                                             : Math.max(availableWidth, Math.min(naturalWidth, availableWidth * 2.2))
    readonly property real unit: widths.length ? tableWidth / widths.reduce((a, b) => a + b, 0) : 1

    function span(col, count) {
        let w = 0
        for (let i = col; i < col + count && i < widths.length; ++i)
            w += widths[i]
        return w * unit
    }

    contentItem: Flickable {
        implicitHeight: grid.implicitHeight
        contentWidth: grid.width
        contentHeight: grid.implicitHeight
        flickableDirection: Flickable.HorizontalFlick
        boundsBehavior: Flickable.StopAtBounds
        clip: contentWidth > width
        interactive: contentWidth > width
        ScrollBar.horizontal: ScrollBar { policy: root.tableWidth > root.availableWidth ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff }

        GridLayout {
            id: grid
            width: root.tableWidth
            columns: Math.max(1, root.widths.length)
            rowSpacing: 0
            columnSpacing: 0

            Repeater {
                model: root.table.cells || []

                Rectangle {
                    id: cell
                    required property var modelData
                    Layout.row: modelData.r
                    Layout.column: modelData.c
                    Layout.rowSpan: modelData.rs || 1
                    Layout.columnSpan: modelData.cs || 1
                    Layout.fillHeight: true
                    Layout.preferredWidth: root.span(modelData.c, modelData.cs || 1)
                    Layout.minimumWidth: Layout.preferredWidth
                    Layout.maximumWidth: Layout.preferredWidth
                    implicitHeight: cellColumn.implicitHeight + (root.plain ? 2 : 10)
                    color: modelData.bg ? ContentStore.themed(modelData.bg, Style.dark) : "transparent"
                    border.color: Style.dark ? "#77707c" : "#000000"
                    border.width: root.plain ? 0 : 0.6

                    ColumnLayout {
                        id: cellColumn
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.margins: root.plain ? 1 : 5
                        anchors.rightMargin: root.plain ? 8 : 5
                        anchors.leftMargin: (root.plain ? 1 : 5) + Math.min((cell.modelData.pad || 0) * root.unit, cell.width * 0.25)
                        spacing: 4

                        Repeater {
                            model: cell.modelData.items || []
                            Loader {
                                id: itemLoader
                                required property var modelData
                                Layout.fillWidth: true
                                sourceComponent: modelData.f !== undefined ? cellFigure : cellText
                                Component {
                                    id: cellText
                                    RichLabel {
                                        html: itemLoader.modelData.h
                                        serif: itemLoader.modelData.sans !== true
                                        horizontalAlignment: itemLoader.modelData.align === "center" ? Text.AlignHCenter
                                                           : itemLoader.modelData.align === "right" ? Text.AlignRight
                                                           : Text.AlignLeft
                                        font.pixelSize: Style.bodySize * (root.plain ? 0.94 : 0.9)
                                    }
                                }
                                Component {
                                    id: cellFigure
                                    FigureView { figureId: itemLoader.modelData.f; maxScale: 1.3 }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
