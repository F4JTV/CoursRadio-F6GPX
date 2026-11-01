import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import CoursRadio

// Table of contents: parts, chapters and their paragraphs.
Page {
    id: page
    title: qsTr("Cours")
    background: Rectangle { color: Style.paper }

    readonly property var parts: ContentStore.courseParts()
    property string expanded: ""

    Flickable {
        anchors.fill: parent
        contentHeight: column.implicitHeight + 40
        clip: true
        ScrollIndicator.vertical: ScrollIndicator {}

        ColumnLayout {
            id: column
            width: parent.width - 2 * Style.gutter
            x: (parent.width - width) / 2
            y: 12
            spacing: 6

            Repeater {
                model: page.parts

                ColumnLayout {
                    id: partColumn
                    required property var modelData
                    Layout.fillWidth: true
                    spacing: 6

                    Label {
                        Layout.fillWidth: true
                        Layout.topMargin: 16
                        text: partColumn.modelData.title
                        color: Style.purple
                        font.bold: true
                        font.italic: true
                        font.pixelSize: 20 * Style.textScale
                        wrapMode: Text.Wrap
                    }

                    Repeater {
                        model: partColumn.modelData.chapters

                        ColumnLayout {
                            id: chapterColumn
                            required property var modelData
                            readonly property bool open: page.expanded === modelData.id
                            Layout.fillWidth: true
                            spacing: 0

                            Label {
                                Layout.fillWidth: true
                                Layout.topMargin: 6
                                visible: (chapterColumn.modelData.group || "") !== ""
                                text: chapterColumn.modelData.group || ""
                                color: Style.inkSoft
                                font.bold: true
                                font.pixelSize: 14 * Style.textScale
                                wrapMode: Text.Wrap
                            }

                            ItemDelegate {
                                Layout.fillWidth: true
                                hoverEnabled: true
                                onClicked: window.openChapter(chapterColumn.modelData.id, 0)
                                background: Rectangle {
                                    radius: 8
                                    color: parent.down ? Style.surfaceStrong : (parent.hovered ? Style.surface : "transparent")
                                }
                                contentItem: RowLayout {
                                    spacing: 8
                                    Label {
                                        Layout.fillWidth: true
                                        text: chapterColumn.modelData.title
                                        color: Style.ink
                                        font.family: Style.serif
                                        font.bold: true
                                        font.pixelSize: 17 * Style.textScale
                                        wrapMode: Text.Wrap
                                    }
                                    ToolButton {
                                        visible: (chapterColumn.modelData.sections || []).length > 0
                                        text: chapterColumn.open ? "▾" : "▸"
                                        // a Liberation family, so that the bundled symbol font
                                        // provides these arrows (they are not in Liberation itself)
                                        font.family: Style.sans
                                        font.pixelSize: 18
                                        onClicked: page.expanded = chapterColumn.open ? "" : chapterColumn.modelData.id
                                        Accessible.name: chapterColumn.open ? qsTr("Replier") : qsTr("Déplier")
                                    }
                                }
                            }

                            Repeater {
                                model: chapterColumn.open ? chapterColumn.modelData.sections : []
                                ItemDelegate {
                                    required property var modelData
                                    Layout.fillWidth: true
                                    leftPadding: 28
                                    onClicked: window.openAnchor(modelData.anchor)
                                    contentItem: Label {
                                        text: modelData.title
                                        color: Style.purple
                                        font.family: Style.serif
                                        font.pixelSize: 15 * Style.textScale
                                        wrapMode: Text.Wrap
                                    }
                                }
                            }

                            Rectangle {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 1
                                color: Style.divider
                            }
                        }
                    }
                }
            }
        }
    }
}
