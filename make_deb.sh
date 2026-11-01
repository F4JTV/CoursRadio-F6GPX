#!/usr/bin/env bash
# Builds a .deb package of Cours Radioamateur for the Debian or Ubuntu release
# it runs on (Debian 12+, Ubuntu 24.04+). The package uses the Qt 6 libraries
# of that release (no Qt library is bundled): the library dependencies are
# computed by dpkg-shlibdeps, the QML modules loaded at run time are listed
# below.
#
#   ./make_deb.sh            # builds (via build_linux.sh) then packages
#   ./make_deb.sh --no-build # packages an existing build (BUILD_DIR)
#
# Environment: DEB_DISTRO (default from /etc/os-release, e.g. ubuntu24.04,
#              debian12), DEB_MAINTAINER.
# Output: dist/coursradio_<version>_<distro>_<arch>.deb
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${BUILD_DIR:-$SRC_DIR/build-linux}"
DIST_DIR="$SRC_DIR/dist"
PKG_NAME="coursradio"
MAINTAINER="${DEB_MAINTAINER:-CoursRadio Community <coursradio@users.noreply.github.com>}"

# QML modules and Qt plugins loaded at run time (not seen by dpkg-shlibdeps);
# same names on Debian 12/13 and Ubuntu 24.04/26.04
QML_DEPENDS="qml6-module-qtquick, qml6-module-qtquick-controls, qml6-module-qtquick-layouts,
 qml6-module-qtquick-templates, qml6-module-qtquick-window, qml6-module-qtqml-workerscript,
 qt6-qpa-plugins"

VERSION="$(sed -n 's/^project(CoursRadio VERSION \([0-9.]*\).*/\1/p' "$SRC_DIR/CMakeLists.txt")"
ARCH="$(dpkg --print-architecture)"
[[ -n "$VERSION" ]] || { echo "Cannot read the version from CMakeLists.txt" >&2; exit 1; }
# read in a subshell: /etc/os-release defines its own VERSION variable
DISTRO="${DEB_DISTRO:-$(. /etc/os-release && echo "${ID}${VERSION_ID}")}"
CODENAME="$(. /etc/os-release && echo "${VERSION_CODENAME:-stable}")"
command -v dpkg-shlibdeps >/dev/null 2>&1 || { echo "dpkg-shlibdeps not found: install dpkg-dev" >&2; exit 1; }

if [[ "${1:-}" != "--no-build" ]]; then
    BUILD_DIR="$BUILD_DIR" BUILD_TYPE=Release "$SRC_DIR/build_linux.sh"
fi
[[ -x "$BUILD_DIR/coursradio" ]] || { echo "No build found in $BUILD_DIR" >&2; exit 1; }

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
ROOT="$STAGE/${PKG_NAME}_${VERSION}_${ARCH}"

echo "==> Installing into the staging tree"
DESTDIR="$ROOT" cmake --install "$BUILD_DIR" --prefix /usr
strip --strip-unneeded "$ROOT/usr/bin/coursradio"

DOC="$ROOT/usr/share/doc/$PKG_NAME"
install -d "$DOC"
install -m 644 "$SRC_DIR/README.md" "$DOC/README.md"
cat > "$DOC/copyright" <<COPYRIGHT
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: Cours Radioamateur
Source: course by F6GPX, Radio-Club de la Haute Ile (F6KGL / F5KFF) - https://f6kgl-f5kff.fr

Files: *
Copyright: F6GPX and the Radio-Club de la Haute Ile (course content);
           CoursRadio Community (application)
License: CC-BY-NC-SA-4.0
 Attribution-NonCommercial-ShareAlike 4.0 International.
 https://creativecommons.org/licenses/by-nc-sa/4.0/

Files: fonts/Liberation*
Copyright: Red Hat, Inc. (Liberation fonts, embedded in the executable)
License: OFL-1.1

Files: fonts/CoursRadioSymbols.ttf
Copyright: 2003 Bitstream, Inc.; DejaVu changes are in the public domain
 (subset of DejaVu Sans renamed "CoursRadio Symbols", embedded in the executable)
License: Bitstream-Vera
COPYRIGHT
cat > "$STAGE/changelog" <<CHANGELOG
$PKG_NAME ($VERSION) $CODENAME; urgency=medium

  * Release $VERSION.

 -- $MAINTAINER  $(date -R)
CHANGELOG
gzip -9n -c "$STAGE/changelog" > "$DOC/changelog.gz"
chmod 644 "$DOC/changelog.gz"

# Shared libraries -> packages of this release, e.g. libqt6core6t64 (>= 6.4.0)
# on Ubuntu 24.04 but libqt6core6 on Debian 12
SHLIBS_DIR="$STAGE/shlibs"
mkdir -p "$SHLIBS_DIR/debian"
touch "$SHLIBS_DIR/debian/control"
SHLIBS="$(cd "$SHLIBS_DIR" && dpkg-shlibdeps -O "$ROOT/usr/bin/coursradio" 2>/dev/null | sed -n 's/^shlibs:Depends=//p')"
[[ -n "$SHLIBS" ]] || { echo "dpkg-shlibdeps found no dependency" >&2; exit 1; }

INSTALLED_SIZE="$(du -sk --exclude=DEBIAN "$ROOT" | cut -f1)"
install -d "$ROOT/DEBIAN"
cat > "$ROOT/DEBIAN/control" <<CONTROL
Package: $PKG_NAME
Version: $VERSION
Section: education
Priority: optional
Architecture: $ARCH
Installed-Size: $INSTALLED_SIZE
Maintainer: $MAINTAINER
Depends: $SHLIBS,
 $QML_DEPENDS
Recommends: qt6-wayland
Homepage: https://f6kgl-f5kff.fr
Description: Course for the French amateur radio operator certificate
 Offline reader for "Preparation au certificat d'operateur du service
 amateur" (F6GPX, Radio-Club de la Haute Ile F6KGL / F5KFF): regulation and
 technique chapters with every schematic redrawn as a native vector figure,
 light and dark themes and adjustable text size.
CONTROL

# Post-install: refresh the desktop and icon caches when available
cat > "$ROOT/DEBIAN/postinst" <<'POSTINST'
#!/bin/sh
set -e
if [ "$1" = "configure" ]; then
    command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database -q /usr/share/applications || true
    command -v gtk-update-icon-cache >/dev/null 2>&1 && gtk-update-icon-cache -q -t /usr/share/icons/hicolor || true
fi
exit 0
POSTINST
chmod 755 "$ROOT/DEBIAN/postinst"
cp "$ROOT/DEBIAN/postinst" "$ROOT/DEBIAN/postrm"
sed -i 's/"configure"/"remove"/' "$ROOT/DEBIAN/postrm"

find "$ROOT/usr" -type d -exec chmod 755 {} +
find "$ROOT/usr" -type f ! -path "*/bin/*" -exec chmod 644 {} +

mkdir -p "$DIST_DIR"
DEB="$DIST_DIR/${PKG_NAME}_${VERSION}_${DISTRO}_${ARCH}.deb"
dpkg-deb --root-owner-group --build "$ROOT" "$DEB"
echo "==> Package: $DEB"
echo "    Install with: sudo apt install $DEB"
