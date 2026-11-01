pragma Singleton
import QtQuick
import CoursRadio

// Colours, fonts and sizes shared by every page.  The palette follows the
// original course (purple titles, dark red labels, navy answers) and has a
// dark variant computed like the diagrams' colour mapping.
QtObject {
    readonly property bool dark: AppSettings.dark

    readonly property color paper: dark ? "#1e1e1e" : "#ffffff"
    readonly property color surface: dark ? "#262329" : "#f7f3f8"
    readonly property color surfaceStrong: dark ? "#332d38" : "#efe6f1"
    readonly property color ink: dark ? "#eaeaea" : "#000000"
    readonly property color inkSoft: dark ? "#b3b0b6" : "#5b5560"
    readonly property color divider: dark ? "#3d3842" : "#ddd3e0"

    readonly property color purple: dark ? "#d793d7" : "#800080"
    readonly property color maroon: dark ? "#e99a9a" : "#800000"
    readonly property color navy: dark ? "#a3a3ff" : "#000080"
    readonly property color good: dark ? "#7ccf8a" : "#1b7a2e"
    readonly property color bad: dark ? "#ff8c80" : "#b3261e"
    readonly property color warn: dark ? "#ffb74d" : "#b26a00"
    readonly property color onPurple: dark ? "#1e1e1e" : "#ffffff"

    readonly property string serif: "Liberation Serif"
    readonly property string sans: "Liberation Sans"

    readonly property real textScale: AppSettings.textScale
    readonly property real bodySize: 16 * textScale
    readonly property real smallSize: 13 * textScale
    readonly property real titleSize: 22 * textScale

    // Responsive layout helpers
    readonly property real gutter: 16
}
