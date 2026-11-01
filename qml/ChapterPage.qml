import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import CoursRadio

// Reader of one chapter of the course.
Page {
    id: page

    property string chapterId
    property int startBlock: 0

    readonly property var chapter: ContentStore.chapter(chapterId)
    readonly property var order: ContentStore.chapterOrder()
    readonly property int orderIndex: order.findIndex(c => c.id === chapterId)
    readonly property var previous: orderIndex > 0 ? order[orderIndex - 1] : null
    readonly property var next: orderIndex >= 0 && orderIndex < order.length - 1 ? order[orderIndex + 1] : null

    title: chapter.short || chapter.title || ""
    background: Rectangle { color: Style.paper }

    function rememberPosition() {
        const index = list.indexAt(20, list.contentY + 20)
        AppSettings.lastChapter = chapterId
        AppSettings.lastBlock = Math.max(0, index)
    }

    ListView {
        id: list
        anchors.fill: parent
        clip: true
        model: page.chapter.blocks || []
        cacheBuffer: 2400
        ScrollBar.vertical: ScrollBar {}
        onMovementEnded: page.rememberPosition()

        header: Item { width: list.width; height: 12 }

        // The delegate spans the whole view and centres the column inside it:
        // ListView may reset the x of its delegates (Qt 6.11 does on Android),
        // which would drop a binding on the delegate's own x.
        delegate: Item {
            id: row
            required property var modelData
            required property int index
            width: list.width
            height: blockView.height

            BlockView {
                id: blockView
                width: row.width - 2 * Style.gutter
                x: Style.gutter
                block: row.modelData
            }
        }

        footer: Item {
            width: list.width
            height: navRow.implicitHeight + 48

            RowLayout {
                id: navRow
                width: list.width - 2 * Style.gutter
                x: Style.gutter
                y: 24
                spacing: 12

                Button {
                    Layout.fillWidth: true
                    Layout.preferredWidth: 1
                    visible: page.previous !== null
                    text: page.previous ? "‹ " + page.previous.title : ""
                    flat: true
                    onClicked: stack.replace(stack.currentItem, "ChapterPage.qml", { chapterId: page.previous.id })
                    contentItem: Label {
                        text: parent.text
                        color: Style.purple
                        elide: Text.ElideRight
                        horizontalAlignment: Text.AlignLeft
                        font.pixelSize: 14 * Style.textScale
                    }
                }
                Button {
                    Layout.fillWidth: true
                    Layout.preferredWidth: 1
                    visible: page.next !== null
                    text: page.next ? page.next.title + " ›" : ""
                    flat: true
                    onClicked: stack.replace(stack.currentItem, "ChapterPage.qml", { chapterId: page.next.id })
                    contentItem: Label {
                        text: parent.text
                        color: Style.purple
                        elide: Text.ElideRight
                        horizontalAlignment: Text.AlignRight
                        font.pixelSize: 14 * Style.textScale
                    }
                }
            }
        }

        Component.onCompleted: {
            if (page.startBlock > 0)
                Qt.callLater(function() { list.positionViewAtIndex(page.startBlock, ListView.Beginning) })
            AppSettings.lastChapter = page.chapterId
        }
    }
}
