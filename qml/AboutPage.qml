import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import CoursRadio

Page {
    id: page
    title: qsTr("À propos")
    background: Rectangle { color: Style.paper }

    Flickable {
        anchors.fill: parent
        contentHeight: column.implicitHeight + 48
        clip: true
        ScrollIndicator.vertical: ScrollIndicator {}

        ColumnLayout {
            id: column
            width: parent.width - 2 * Style.gutter
            x: (parent.width - width) / 2
            y: 24
            spacing: 14

            Image {
                Layout.alignment: Qt.AlignHCenter
                source: "qrc:/icons/coursradio.png"
                sourceSize: Qt.size(96, 96)
            }
            Label {
                Layout.fillWidth: true
                text: qsTr("Cours Radioamateur %1").arg(appVersion)
                horizontalAlignment: Text.AlignHCenter
                color: Style.purple
                font.bold: true
                font.pixelSize: 22
            }

            SectionTitle { text: qsTr("Affichage") }
            RowLayout {
                Layout.fillWidth: true
                Label { text: qsTr("Thème sombre"); color: Style.ink; Layout.fillWidth: true; font.pixelSize: Style.bodySize }
                Switch {
                    checked: AppSettings.dark
                    onToggled: AppSettings.dark = checked
                }
            }
            RowLayout {
                Layout.fillWidth: true
                Label { text: qsTr("Taille du texte"); color: Style.ink; font.pixelSize: Style.bodySize }
                Slider {
                    Layout.fillWidth: true
                    from: 0.8
                    to: 1.6
                    stepSize: 0.1
                    value: AppSettings.textScale
                    onMoved: AppSettings.textScale = value
                }
                Label { text: Math.round(AppSettings.textScale * 100) + " %"; color: Style.inkSoft }
            }

            SectionTitle { text: qsTr("Le cours") }
            RichLabel {
                Layout.fillWidth: true
                html: qsTr("Cette application reprend le cours de « <i>Préparation au certificat d’opérateur du service amateur</i> » "
                           + "(premier livre : cours de Réglementation et de Technique), "
                           + "édition de novembre 2025, rédigé par <b>F6GPX</b> pour le <b>Radio-Club de la Haute Île</b> "
                           + "(F6KGL / F5KFF, Neuilly-sur-Marne) : "
                           + "<a href=\"https://f6kgl-f5kff.fr\">https://f6kgl-f5kff.fr</a>.")
            }
            RichLabel {
                Layout.fillWidth: true
                html: qsTr("Le document original est mis à disposition selon les termes de la licence Creative Commons "
                           + "Attribution – Pas d’Utilisation Commerciale – Partage dans les Mêmes Conditions 4.0 International "
                           + "(<a href=\"https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr\">CC BY-NC-SA 4.0</a>). "
                           + "Le contenu de l’application est diffusé sous la même licence, sans usage commercial. "
                           + "Les schémas ont été redessinés en vectoriel natif à partir du document original ; "
                           + "les textes sont reproduits avec leur mise en forme.")
            }

            SectionTitle { text: qsTr("Conventions du cours") }
            RichLabel {
                Layout.fillWidth: true
                serif: true
                html: qsTr("Les <b><u>mots-clés</u></b> sont en gras souligné. Les <b>formules à connaître</b> sont en gras ; "
                           + "les <b><i>formules en gras italique</i></b> ne sont pas à connaître. "
                           + "Les paragraphes en <i>italique</i> sont hors programme. "
                           + "Les exemples d’application sont présentés en retrait dans une autre police.")
            }

            SectionTitle { text: qsTr("Logiciel") }
            RichLabel {
                Layout.fillWidth: true
                font.pixelSize: Style.smallSize
                color: Style.inkSoft
                html: qsTr("Réalisé en C++ avec Qt 6 et Qt Quick (LGPLv3). Polices Liberation (SIL Open Font License 1.1).")
            }
        }
    }

    component SectionTitle: Label {
        Layout.fillWidth: true
        Layout.topMargin: 10
        color: Style.purple
        font.bold: true
        font.italic: true
        font.pixelSize: 18 * Style.textScale
    }
}
