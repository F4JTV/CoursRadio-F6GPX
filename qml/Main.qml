import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
import CoursRadio

ApplicationWindow {
    id: window

    width: 1040
    height: 780
    minimumWidth: 340
    minimumHeight: 480
    visible: true
    title: qsTr("Cours Radioamateur")
    color: Style.paper
    font.family: Style.sans

    Material.theme: Style.dark ? Material.Dark : Material.Light
    Material.primary: Style.purple
    Material.accent: Style.purple
    Material.background: Style.paper
    Material.foreground: Style.ink

    // --- Navigation API used by every page ---------------------------------
    function openHome() { stack.pop(null) }
    function openCourse() { stack.push(courseTocComponent) }
    function openChapter(id, block) {
        stack.push(chapterComponent, { chapterId: id, startBlock: block === undefined ? 0 : block })
    }
    function openAnchor(anchor) {
        const loc = ContentStore.locate(anchor)
        if (loc.found)
            openChapter(loc.chapter, loc.block)
    }
    function openFigure(id, caption) {
        stack.push(figureComponent, { figureId: id, caption: caption || "" })
    }
    function openAbout() { stack.push(aboutComponent) }

    function goBack() {
        const page = stack.currentItem
        if (page && page.requestLeave !== undefined) {
            page.requestLeave()
            return
        }
        if (stack.depth > 1)
            stack.pop()
    }

    onClosing: function(close) {
        if (Qt.platform.os === "android" && stack.depth > 1) {
            close.accepted = false
            goBack()
        }
    }

    Shortcut {
        sequences: [StandardKey.Back, "Esc"]
        enabled: stack.depth > 1
        onActivated: window.goBack()
    }

    header: ToolBar {
        Material.foreground: "#ffffff"
        background: Rectangle { color: Style.dark ? "#2b2330" : "#800080" }

        RowLayout {
            anchors.fill: parent
            spacing: 0

            ToolButton {
                visible: stack.depth > 1
                icon.source: "qrc:/icons/back.png"
                icon.color: "#ffffff"
                onClicked: window.goBack()
                Accessible.name: qsTr("Retour")
            }

            Label {
                Layout.fillWidth: true
                Layout.leftMargin: stack.depth > 1 ? 0 : 16
                text: stack.currentItem && stack.currentItem.title ? stack.currentItem.title : window.title
                elide: Label.ElideRight
                font.pixelSize: 18
                font.bold: true
                color: "#ffffff"
            }

            ToolButton {
                icon.source: Style.dark ? "qrc:/icons/sun.png" : "qrc:/icons/moon.png"
                icon.color: "#ffffff"
                onClicked: AppSettings.dark = !AppSettings.dark
                ToolTip.visible: hovered
                ToolTip.text: Style.dark ? qsTr("Thème clair") : qsTr("Thème sombre")
                Accessible.name: ToolTip.text
            }

            ToolButton {
                icon.source: "qrc:/icons/menu.png"
                icon.color: "#ffffff"
                onClicked: appMenu.open()
                Accessible.name: qsTr("Menu")

                Menu {
                    id: appMenu
                    y: parent.height
                    MenuItem {
                        text: qsTr("Agrandir le texte")
                        onTriggered: AppSettings.textScale = AppSettings.textScale + 0.1
                    }
                    MenuItem {
                        text: qsTr("Réduire le texte")
                        onTriggered: AppSettings.textScale = AppSettings.textScale - 0.1
                    }
                    MenuSeparator {}
                    MenuItem { text: qsTr("Accueil"); onTriggered: window.openHome() }
                    MenuItem { text: qsTr("À propos"); onTriggered: window.openAbout() }
                }
            }
        }
    }

    StackView {
        id: stack
        anchors.fill: parent
        initialItem: HomePage {}
    }

    Component { id: courseTocComponent; CourseTocPage {} }
    Component { id: chapterComponent; ChapterPage {} }
    Component { id: figureComponent; FigurePage {} }
    Component { id: aboutComponent; AboutPage {} }

    // Automated screenshots (development only): COURSRADIO_CAPTURE_DIR=<dir>
    Loader {
        active: captureDir !== ""
        source: "CaptureDriver.qml"
    }
}
