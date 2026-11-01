import QtQuick
import CoursRadio

// Rich text (course HTML subset) whose colours follow the theme.
// Links of the form "anchor:T-1.7d" open the course at that paragraph.
Text {
    id: label

    property string html
    property bool serif: false

    textFormat: Text.RichText
    wrapMode: Text.Wrap
    color: Style.ink
    linkColor: Style.navy
    font.family: serif ? Style.serif : Style.sans
    font.pixelSize: Style.bodySize
    text: ContentStore.themed(html, Style.dark)

    onLinkActivated: function(link) {
        if (link.startsWith("anchor:"))
            window.openAnchor(link.substring(7))
        else
            Qt.openUrlExternally(link)
    }

    HoverHandler {
        enabled: label.hoveredLink !== ""
        cursorShape: Qt.PointingHandCursor
    }
}
