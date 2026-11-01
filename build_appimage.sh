#!/usr/bin/env bash
# Builds a portable AppImage of Cours Radioamateur (Linux x86_64): the Qt
# libraries, QML modules and plugins are bundled by linuxdeploy and its Qt
# plugin, so the AppImage runs on distributions without Qt 6.
#
#   ./build_appimage.sh
#
# Requirements: CMake, Ninja (optional), a C++17 compiler, Qt 6.4 or later
# (desktop kit), curl, and the X11/XCB libraries the Qt xcb plugin needs.
#
# Environment (all optional):
#   QT_DIR     Qt kit to bundle, e.g. ~/Qt/6.8.3/gcc_64 (default: the Qt of
#              the system, found through qmake6 / qmake)
#   BUILD_DIR  build folder (default: build-appimage)
#   TOOLS_DIR  where linuxdeploy is downloaded (default: $BUILD_DIR/tools)
#
# Output: dist/CoursRadio-<version>-x86_64.AppImage
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${BUILD_DIR:-$SRC_DIR/build-appimage}"
TOOLS_DIR="${TOOLS_DIR:-$BUILD_DIR/tools}"
APPDIR="$BUILD_DIR/AppDir"
DIST_DIR="$SRC_DIR/dist"
ARCH="x86_64"

die() { echo "[ERROR] $*" >&2; exit 1; }

VERSION="$(sed -n 's/^project(CoursRadio VERSION \([0-9.]*\).*/\1/p' "$SRC_DIR/CMakeLists.txt")"
[[ -n "$VERSION" ]] || die "Cannot read the version from CMakeLists.txt"

# qmake of the Qt to bundle (linuxdeploy-plugin-qt reads QMAKE)
if [[ -n "${QT_DIR:-}" ]]; then
    QMAKE="$QT_DIR/bin/qmake"
    cmake_prefix=(-DCMAKE_PREFIX_PATH="$QT_DIR")
else
    QMAKE="$(command -v qmake6 || command -v qmake || true)"
    cmake_prefix=()
fi
[[ -x "$QMAKE" ]] || die "qmake not found: set QT_DIR to your Qt kit (e.g. ~/Qt/6.8.3/gcc_64)"
export QMAKE
QT_PLUGINS="$("$QMAKE" -query QT_INSTALL_PLUGINS)"
echo "==> Qt $("$QMAKE" -query QT_VERSION) ($QMAKE)"

# linuxdeploy and its Qt plugin (continuous builds)
mkdir -p "$TOOLS_DIR"
for tool in linuxdeploy/linuxdeploy/linuxdeploy-$ARCH.AppImage \
            linuxdeploy/linuxdeploy-plugin-qt/linuxdeploy-plugin-qt-$ARCH.AppImage; do
    repo="${tool%/*}"
    file="${tool##*/}"
    if [[ ! -x "$TOOLS_DIR/$file" ]]; then
        echo "==> Downloading $file"
        curl -fsSL -o "$TOOLS_DIR/$file" "https://github.com/$repo/releases/download/continuous/$file"
        chmod +x "$TOOLS_DIR/$file"
    fi
done
export PATH="$TOOLS_DIR:$PATH"
# run the tools without FUSE (containers, CI runners)
export APPIMAGE_EXTRACT_AND_RUN=1

generator=()
command -v ninja >/dev/null 2>&1 && generator=(-G Ninja)

echo "==> Building"
cmake -S "$SRC_DIR" -B "$BUILD_DIR" "${generator[@]}" "${cmake_prefix[@]}" \
      -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_SKIP_INSTALL_RPATH=ON
cmake --build "$BUILD_DIR" --parallel
rm -rf "$APPDIR"
DESTDIR="$APPDIR" cmake --install "$BUILD_DIR"

# QML modules: found by scanning the QML sources of the application
export QML_SOURCES_PATHS="$SRC_DIR/qml"
# Wayland support when the Qt kit has it (X11/XWayland otherwise)
if [[ -f "$QT_PLUGINS/platforms/libqwayland-egl.so" ]]; then
    export EXTRA_PLATFORM_PLUGINS="libqwayland-egl.so;libqwayland-generic.so"
fi
# the strip of linuxdeploy fails on binaries made by recent toolchains
export NO_STRIP=1

mkdir -p "$DIST_DIR"
OUT="$DIST_DIR/CoursRadio-$VERSION-$ARCH.AppImage"
rm -f "$OUT"
echo "==> Creating the AppImage"
(
    cd "$BUILD_DIR"
    LDAI_OUTPUT="$OUT" OUTPUT="$OUT" linuxdeploy-$ARCH.AppImage \
        --appdir "$APPDIR" \
        --executable "$APPDIR/usr/bin/coursradio" \
        --desktop-file "$APPDIR/usr/share/applications/coursradio.desktop" \
        --plugin qt \
        --output appimage
)
[[ -f "$OUT" ]] || die "No AppImage produced"
echo "==> AppImage: $OUT"
