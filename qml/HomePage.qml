import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import CoursRadio

Page {
    id: page
    title: qsTr("Cours Radioamateur")
    background: Rectangle { color: Style.paper }

    readonly property var lastChapter: AppSettings.lastChapter !== "" ? findChapter(AppSettings.lastChapter) : null

    function findChapter(id) {
        const order = ContentStore.chapterOrder()
        for (let i = 0; i < order.length; ++i)
            if (order[i].id === id)
                return order[i]
        return null
    }

    Flickable {
        anchors.fill: parent
        contentHeight: column.implicitHeight + 48
        clip: true
        ScrollIndicator.vertical: ScrollIndicator {}

        ColumnLayout {
            id: column
            width: Math.min(parent.width - 2 * Style.gutter, 880)
            x: (parent.width - width) / 2
            y: 24
            spacing: 18

            // Title block, after the cover of the course
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4
                Label {
                    Layout.fillWidth: true
                    text: qsTr("Préparation au")
                    color: Style.inkSoft
                    font.pixelSize: 15 * Style.textScale
                    horizontalAlignment: Text.AlignHCenter
                }
                Label {
                    Layout.fillWidth: true
                    text: qsTr("CERTIFICAT D’OPÉRATEUR\ndu SERVICE AMATEUR")
                    color: Style.purple
                    font.family: Style.serif
                    font.bold: true
                    font.pixelSize: 26 * Style.textScale
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.Wrap
                }
                Label {
                    Layout.fillWidth: true
                    text: qsTr("Réglementation et Technique — cours de F6GPX")
                    color: Style.inkSoft
                    font.pixelSize: 14 * Style.textScale
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.Wrap
                }
            }

            HomeTile {
                Layout.fillWidth: true
                heading: qsTr("Cours")
                detail: qsTr("Réglementation (R-1 à R-5), Technique (chapitres 0 à 12) et annexes.")
                accent: Style.purple
                glyph: "§"
                onActivated: window.openCourse()
            }

            ItemDelegate {
                Layout.fillWidth: true
                visible: page.lastChapter !== null
                contentItem: ColumnLayout {
                    spacing: 2
                    Label {
                        text: qsTr("Reprendre la lecture")
                        color: Style.purple
                        font.bold: true
                        font.pixelSize: 14 * Style.textScale
                    }
                    Label {
                        Layout.fillWidth: true
                        text: page.lastChapter ? page.lastChapter.title : ""
                        color: Style.ink
                        elide: Text.ElideRight
                        font.pixelSize: 15 * Style.textScale
                    }
                }
                background: Rectangle {
                    color: parent.down ? Style.surfaceStrong : Style.surface
                    radius: 10
                    border.color: Style.divider
                }
                onClicked: window.openChapter(AppSettings.lastChapter, AppSettings.lastBlock)
            }

            Label {
                Layout.fillWidth: true
                Layout.topMargin: 8
                text: qsTr("D’après « Préparation au certificat d’opérateur du service amateur » (édition de novembre 2025) "
                           + "de F6GPX, Radio-Club de la Haute Île F6KGL / F5KFF — licence CC BY-NC-SA 4.0.")
                color: Style.inkSoft
                font.pixelSize: 12 * Style.textScale
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.Wrap
            }
        }
    }
}
