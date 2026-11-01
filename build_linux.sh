#!/usr/bin/env bash
# Builds Cours Radioamateur on Debian 12+ or Ubuntu 24.04+ with the Qt 6
# packages of the distribution (Qt 6.4 or later).
#
#   ./build_linux.sh                 # Release build in ./build-linux
#   ./build_linux.sh --install-deps  # install the build dependencies first (sudo)
#   ./build_linux.sh --run           # build, then start the application
#
# Environment: BUILD_DIR (default build-linux), BUILD_TYPE (default Release),
#              JOBS (default: number of CPUs).
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${BUILD_DIR:-$SRC_DIR/build-linux}"
BUILD_TYPE="${BUILD_TYPE:-Release}"
JOBS="${JOBS:-$(nproc)}"

BUILD_DEPS=(
    build-essential cmake ninja-build dpkg-dev
    qt6-base-dev qt6-base-dev-tools
    qt6-declarative-dev qt6-declarative-dev-tools
)
RUNTIME_DEPS=(
    qml6-module-qtquick qml6-module-qtquick-controls qml6-module-qtquick-layouts
    qml6-module-qtquick-templates qml6-module-qtquick-window qml6-module-qtqml-workerscript
    qt6-qpa-plugins
)

install_deps=0
run_after=0
for arg in "$@"; do
    case "$arg" in
        --install-deps) install_deps=1 ;;
        --run) run_after=1 ;;
        -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
        *) echo "Unknown option: $arg" >&2; exit 2 ;;
    esac
done

if [[ $install_deps -eq 1 ]]; then
    sudo=()
    [[ $EUID -ne 0 ]] && sudo=(sudo)   # root in a container: no sudo
    "${sudo[@]}" apt-get update
    "${sudo[@]}" env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        "${BUILD_DEPS[@]}" "${RUNTIME_DEPS[@]}"
fi

missing=()
for pkg in "${BUILD_DEPS[@]}" "${RUNTIME_DEPS[@]}"; do
    dpkg-query -W -f='${Status}' "$pkg" 2>/dev/null | grep -q "install ok installed" || missing+=("$pkg")
done
if [[ ${#missing[@]} -gt 0 ]]; then
    echo "Missing packages: ${missing[*]}" >&2
    echo "Run: $0 --install-deps   (or: sudo apt install ${missing[*]})" >&2
    exit 1
fi

generator=()
command -v ninja >/dev/null 2>&1 && generator=(-G Ninja)

echo "==> Configuring ($BUILD_TYPE) in $BUILD_DIR"
cmake -S "$SRC_DIR" -B "$BUILD_DIR" "${generator[@]}" \
      -DCMAKE_BUILD_TYPE="$BUILD_TYPE" -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_SKIP_INSTALL_RPATH=ON

echo "==> Building"
cmake --build "$BUILD_DIR" --parallel "$JOBS"

echo "==> Done: $BUILD_DIR/coursradio"
if [[ $run_after -eq 1 ]]; then
    exec "$BUILD_DIR/coursradio"
fi
