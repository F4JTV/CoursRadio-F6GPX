import QtQuick
import CoursRadio

// Development helper: replays a navigation plan and saves screenshots.
// COURSRADIO_CAPTURE_DIR=<dir> COURSRADIO_CAPTURE_PLAN="size:400x800;home;shot:home;toc;shot:toc;..."
Item {
    id: driver

    property var steps: capturePlan.split(";").filter(s => s.trim() !== "")
    property int position: 0

    function page() { return stack.currentItem }

    function findChild(item, predicate) {
        if (!item)
            return null
        if (predicate(item))
            return item
        const kids = item.children || []
        for (let i = 0; i < kids.length; ++i) {
            const found = findChild(kids[i], predicate)
            if (found)
                return found
        }
        if (item.contentItem && item.contentItem !== item) {
            const found = findChild(item.contentItem, predicate)
            if (found)
                return found
        }
        return null
    }

    function run(step) {
        const parts = step.split(":")
        const cmd = parts[0].trim()
        const arg = parts.slice(1).join(":")
        switch (cmd) {
        case "size": {
            const wh = arg.split("x")
            window.width = parseInt(wh[0]); window.height = parseInt(wh[1]); break
        }
        case "dark": AppSettings.dark = true; break
        case "light": AppSettings.dark = false; break
        case "scale": AppSettings.textScale = parseFloat(arg); break
        case "home": window.openHome(); break
        case "toc": window.openCourse(); break
        case "about": window.openAbout(); break
        case "chapter": {
            const a = arg.split(",")
            window.openChapter(a[0], a.length > 1 ? parseInt(a[1]) : 0); break
        }
        case "anchor": window.openAnchor(arg); break
        case "figure": window.openFigure(arg, ""); break
        case "zoom": page().zoom = parseFloat(arg); break
        case "back": stack.pop(); break
        case "scroll": {
            const flick = findChild(page(), it => it.contentY !== undefined && it.contentHeight !== undefined && it.flickableDirection !== undefined)
            if (flick)
                flick.contentY = parseInt(arg)
            break
        }
        case "shot": {
            const path = captureDir + "/" + arg + ".png"
            window.contentItem.parent.grabToImage(function(result) { result.saveToFile(path) })
            break
        }
        case "quit": Qt.quit(); break
        }
    }

    Timer {
        interval: 700
        running: driver.steps.length > 0
        repeat: true
        onTriggered: {
            if (driver.position >= driver.steps.length) {
                Qt.quit()
                return
            }
            driver.run(driver.steps[driver.position++])
        }
    }
}
