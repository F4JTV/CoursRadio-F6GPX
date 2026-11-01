#!/usr/bin/env bash
# Builds the Android APK of Cours Radioamateur (Linux host).
#
# Requirements:
#   - Qt 6.4 or later from the Qt online installer, with both the "Android"
#     component (e.g. ~/Qt/6.11.2/android_arm64_v8a) and the "Desktop" one of
#     the same version (host tools, e.g. ~/Qt/6.11.2/gcc_64)
#   - Android SDK (platform-tools, build-tools, a platform) and the NDK version
#     recommended for your Qt version, JDK 17
#
# Environment (all optional):
#   QT_ROOT           Qt installation      (default: ~/Qt; the newest 6.x.y
#                                           version with an Android kit is used)
#   ANDROID_ABI       arm64_v8a (default), armv7, x86_64 or x86
#   QT_ANDROID        Qt for Android kit   (default: found under QT_ROOT)
#   QT_HOST           desktop Qt kit       (default: same version as QT_ANDROID)
#   ANDROID_SDK_ROOT  Android SDK          (default: $ANDROID_HOME or ~/Android/Sdk)
#   ANDROID_NDK_ROOT  Android NDK          (default: newest folder in $ANDROID_SDK_ROOT/ndk)
#   JAVA_HOME         JDK 17
#   BUILD_DIR         build folder         (default: build-android)
# Optional release signing (otherwise the APK is signed with a debug key):
#   QT_ANDROID_KEYSTORE_PATH, QT_ANDROID_KEYSTORE_ALIAS,
#   QT_ANDROID_KEYSTORE_STORE_PASS, QT_ANDROID_KEYSTORE_KEY_PASS
#
# Output: dist/CoursRadio-<version>-<abi>.apk
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QT_ROOT="${QT_ROOT:-$HOME/Qt}"
ANDROID_ABI="${ANDROID_ABI:-arm64_v8a}"
ANDROID_SDK_ROOT="${ANDROID_SDK_ROOT:-${ANDROID_HOME:-$HOME/Android/Sdk}}"
BUILD_DIR="${BUILD_DIR:-$SRC_DIR/build-android}"
DIST_DIR="$SRC_DIR/dist"

die() { echo "[ERROR] $*" >&2; exit 1; }

# Newest Qt 6.x.y under QT_ROOT that has the Android kit for ANDROID_ABI
# (versions compared numerically: 6.11 is newer than 6.9).
find_qt_android() {
    local v
    for v in $(ls -1 "$QT_ROOT" 2>/dev/null | grep -E '^6\.[0-9]+\.[0-9]+$' | sort -rV); do
        if [[ -x "$QT_ROOT/$v/android_$ANDROID_ABI/bin/qt-cmake" ]]; then
            echo "$QT_ROOT/$v/android_$ANDROID_ABI"
            return 0
        fi
    done
    return 0
}

where="under $QT_ROOT"
if [[ -n "${QT_ANDROID:-}" ]]; then
    where="in $QT_ANDROID"
else
    QT_ANDROID="$(find_qt_android)"
fi
if [[ -z "$QT_ANDROID" || ! -x "$QT_ANDROID/bin/qt-cmake" ]]; then
    echo "[ERROR] No Qt for Android kit (android_$ANDROID_ABI) found $where." >&2
    for d in "$QT_ROOT"/6.*/; do
        [[ -d "$d" ]] || continue
        echo "        Installed in $(basename "$d"): $(ls -1 "$d" | grep -vxE 'Src|doc|examples|sha1s.txt' | tr '\n' ' ')" >&2
    done
    echo "        Add the \"Android\" component of your Qt version with the Qt Maintenance Tool" >&2
    echo "        (~/Qt/MaintenanceTool), or set QT_ANDROID to the kit folder." >&2
    exit 1
fi

# The host tools must come from the desktop kit of the same Qt version.
QT_VERSION_DIR="$(dirname "$QT_ANDROID")"
if [[ -z "${QT_HOST:-}" ]]; then
    for kit in gcc_64 linux_gcc_64 gcc_arm64 linux_gcc_arm64; do
        if [[ -d "$QT_VERSION_DIR/$kit/bin" ]]; then
            QT_HOST="$QT_VERSION_DIR/$kit"
            break
        fi
    done
fi
[[ -n "${QT_HOST:-}" && -d "$QT_HOST/bin" ]] \
    || die "Desktop Qt $(basename "$QT_VERSION_DIR") not found next to $QT_ANDROID: add the \"Desktop\" component of the same version, or set QT_HOST"
echo "==> Qt for Android: $QT_ANDROID"
echo "==> Qt host tools:  $QT_HOST"
[[ -d "$ANDROID_SDK_ROOT" ]] || die "Android SDK not found in $ANDROID_SDK_ROOT (set ANDROID_SDK_ROOT)"
if [[ -z "${ANDROID_NDK_ROOT:-}" ]]; then
    ANDROID_NDK_ROOT="$(ls -d "$ANDROID_SDK_ROOT"/ndk/*/ 2>/dev/null | sort -V | tail -1 || true)"
    ANDROID_NDK_ROOT="${ANDROID_NDK_ROOT%/}"
fi
[[ -d "${ANDROID_NDK_ROOT:-}" ]] || die "Android NDK not found (set ANDROID_NDK_ROOT)"
command -v java >/dev/null 2>&1 || [[ -n "${JAVA_HOME:-}" ]] || die "JDK not found (set JAVA_HOME to a JDK 17)"
export ANDROID_SDK_ROOT ANDROID_NDK_ROOT

VERSION="$(sed -n 's/^project(CoursRadio VERSION \([0-9.]*\).*/\1/p' "$SRC_DIR/CMakeLists.txt")"
ABI="$(basename "$QT_ANDROID" | sed 's/^android_//')"

generator=()
command -v ninja >/dev/null 2>&1 && generator=(-G Ninja)

signing=()
if [[ -n "${QT_ANDROID_KEYSTORE_PATH:-}" ]]; then
    signing=(-DQT_ANDROID_SIGN_APK=ON)
    echo "==> Release signing with $QT_ANDROID_KEYSTORE_PATH"
fi

echo "==> Configuring for Android ($ABI), NDK $ANDROID_NDK_ROOT"
"$QT_ANDROID/bin/qt-cmake" -S "$SRC_DIR" -B "$BUILD_DIR" "${generator[@]}" \
    -DCMAKE_BUILD_TYPE=Release \
    -DQT_HOST_PATH="$QT_HOST" \
    -DANDROID_SDK_ROOT="$ANDROID_SDK_ROOT" \
    -DANDROID_NDK_ROOT="$ANDROID_NDK_ROOT" \
    "${signing[@]}"

echo "==> Building the APK"
cmake --build "$BUILD_DIR" --parallel
cmake --build "$BUILD_DIR" --target apk

# Gradle output: android-build/ (or android-build-CoursRadio/ when
# QT_USE_TARGET_ANDROID_BUILD_DIR is set, Qt 6.8 and later)
find_apk() { find "$BUILD_DIR" -path "*/android-build*/build/outputs/apk/release/$1" -type f 2>/dev/null | head -1; }
APK="$(find_apk '*-signed.apk')"
if [[ -z "$APK" ]]; then
    UNSIGNED="$(find_apk '*.apk')"
    [[ -n "$UNSIGNED" ]] || die "No APK produced under $BUILD_DIR/android-build*/build/outputs/apk/release"
    # No release keystore: sign with the Android debug key so the APK installs.
    BUILD_TOOLS="$(ls -d "$ANDROID_SDK_ROOT"/build-tools/*/ | sort -V | tail -1)"
    KEYSTORE="$HOME/.android/debug.keystore"
    if [[ ! -f "$KEYSTORE" ]]; then
        mkdir -p "$HOME/.android"
        keytool -genkeypair -v -keystore "$KEYSTORE" -storepass android -keypass android \
            -alias androiddebugkey -keyalg RSA -keysize 2048 -validity 10000 \
            -dname "CN=Android Debug,O=Android,C=US"
    fi
    ALIGNED="$BUILD_DIR/CoursRadio-aligned.apk"
    "${BUILD_TOOLS}zipalign" -f -p 4 "$UNSIGNED" "$ALIGNED"
    APK="$BUILD_DIR/CoursRadio-debugsigned.apk"
    "${BUILD_TOOLS}apksigner" sign --ks "$KEYSTORE" --ks-pass pass:android --key-pass pass:android \
        --out "$APK" "$ALIGNED"
    echo "==> Signed with the debug key (set QT_ANDROID_KEYSTORE_* for a release key)"
fi

mkdir -p "$DIST_DIR"
OUT="$DIST_DIR/CoursRadio-$VERSION-$ABI.apk"
cp "$APK" "$OUT"
echo "==> APK: $OUT"
echo "    Install with: adb install -r \"$OUT\""
