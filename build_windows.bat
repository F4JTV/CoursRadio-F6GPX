@echo off
rem ===========================================================================
rem  Cours Radioamateur - Windows 10/11 build and installer
rem
rem  Run from the "x64 Native Tools Command Prompt for VS 2022".
rem
rem  Requirements:
rem    - Visual Studio 2022 (workload "Desktop development with C++",
rem      which also provides CMake and Ninja)
rem    - Qt 6.4 or later for MSVC 64-bit (Qt online installer)
rem    - Inno Setup 6.3 or later (https://jrsoftware.org/isinfo.php)
rem
rem  Configuration (environment variables, optional):
rem    QT_DIR     Qt kit folder        default: newest C:\Qt\6.x.y\msvc*_64 kit
rem    QT_ROOT    Qt installation      default: C:\Qt (used to find QT_DIR)
rem    ISCC       Inno Setup compiler  default: C:\Program Files (x86)\Inno Setup 6\ISCC.exe
rem    BUILD_DIR  build folder         default: build-windows
rem
rem  Usage:  build_windows.bat            build + deploy + installer
rem          build_windows.bat noinstaller build + deploy only
rem
rem  Output: dist\CoursRadio-<version>-win64-setup.exe
rem          dist\CoursRadio-<version>-win64\  (portable folder)
rem ===========================================================================
setlocal EnableExtensions EnableDelayedExpansion

set "SRC_DIR=%~dp0"
if "%SRC_DIR:~-1%"=="\" set "SRC_DIR=%SRC_DIR:~0,-1%"
if not defined QT_ROOT set "QT_ROOT=C:\Qt"
if not defined QT_DIR call :find_qt
if not defined ISCC set "ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not defined BUILD_DIR set "BUILD_DIR=%SRC_DIR%\build-windows"

rem --- version from CMakeLists.txt ("project(CoursRadio VERSION x.y.z ...)")
set "APP_VERSION="
for /f "tokens=3" %%v in ('findstr /r /c:"^project(CoursRadio VERSION" "%SRC_DIR%\CMakeLists.txt"') do set "APP_VERSION=%%v"
if not defined APP_VERSION (
    echo [ERROR] Cannot read the version from CMakeLists.txt
    exit /b 1
)
set "DEPLOY_DIR=%SRC_DIR%\dist\CoursRadio-%APP_VERSION%-win64"

echo === Cours Radioamateur %APP_VERSION% ===

rem --- checks
where cl >nul 2>&1
if errorlevel 1 (
    echo [ERROR] cl.exe not found: open the "x64 Native Tools Command Prompt for VS 2022".
    exit /b 1
)
if not defined QT_DIR (
    echo [ERROR] No Qt MSVC 64-bit kit found under "%QT_ROOT%".
    echo         Install one with the Qt online installer, or set QT_DIR to the kit folder.
    exit /b 1
)
if not exist "%QT_DIR%\bin\windeployqt.exe" (
    echo [ERROR] Qt not found in "%QT_DIR%". Set QT_DIR to your Qt MSVC 64-bit kit.
    exit /b 1
)
echo Qt kit: %QT_DIR%
where cmake >nul 2>&1
if errorlevel 1 (
    echo [ERROR] cmake not found in PATH.
    exit /b 1
)
set "GENERATOR=NMake Makefiles"
where ninja >nul 2>&1
if not errorlevel 1 set "GENERATOR=Ninja"

rem --- configure and build
echo.
echo === Configuring (%GENERATOR%) ===
cmake -S "%SRC_DIR%" -B "%BUILD_DIR%" -G "%GENERATOR%" ^
      -DCMAKE_BUILD_TYPE=Release ^
      -DCMAKE_PREFIX_PATH="%QT_DIR%"
if errorlevel 1 goto :failed

echo.
echo === Building ===
cmake --build "%BUILD_DIR%" --config Release
if errorlevel 1 goto :failed

rem --- deploy (Qt libraries, QML modules, plugins, MSVC runtime)
echo.
echo === Deploying to %DEPLOY_DIR% ===
if exist "%DEPLOY_DIR%" rmdir /s /q "%DEPLOY_DIR%"
mkdir "%DEPLOY_DIR%"
copy /y "%BUILD_DIR%\CoursRadio.exe" "%DEPLOY_DIR%\" >nul
if errorlevel 1 goto :failed
"%QT_DIR%\bin\windeployqt.exe" --release --qmldir "%SRC_DIR%\qml" --no-translations ^
      --no-compiler-runtime "%DEPLOY_DIR%\CoursRadio.exe"
if errorlevel 1 goto :failed
rem MSVC runtime DLLs next to the executable (app-local deployment), so that
rem the portable folder and the installed application run without the
rem Visual C++ Redistributable. VCToolsRedistDir is set by the VS prompt.
if not defined VCToolsRedistDir (
    echo [ERROR] VCToolsRedistDir is not set: use the x64 Native Tools Command Prompt for VS 2022.
    goto :failed
)
set "CRT_FOUND="
for /d %%D in ("%VCToolsRedistDir%\x64\Microsoft.VC*.CRT") do (
    copy /y "%%~D\*.dll" "%DEPLOY_DIR%\" >nul
    set "CRT_FOUND=1"
)
if not defined CRT_FOUND (
    echo [ERROR] MSVC runtime not found in "%VCToolsRedistDir%\x64".
    goto :failed
)
copy /y "%SRC_DIR%\README.md" "%DEPLOY_DIR%\" >nul
copy /y "%SRC_DIR%\LICENSE.md" "%DEPLOY_DIR%\" >nul

if /i "%~1"=="noinstaller" goto :done

rem --- installer
echo.
echo === Building the installer (Inno Setup) ===
if not exist "%ISCC%" (
    echo [WARNING] Inno Setup not found at "%ISCC%": installer skipped.
    echo           The portable folder is ready in %DEPLOY_DIR%
    goto :done
)
"%ISCC%" /Q "/DAppVersion=%APP_VERSION%" "/DSourceDir=%DEPLOY_DIR%" ^
      "/DProjectDir=%SRC_DIR%" "/O%SRC_DIR%\dist" "%SRC_DIR%\packaging\windows\coursradio.iss"
if errorlevel 1 goto :failed
echo Installer: %SRC_DIR%\dist\CoursRadio-%APP_VERSION%-win64-setup.exe

:done
echo.
echo === Done ===
endlocal
exit /b 0

:failed
echo.
echo [ERROR] Build failed.
endlocal
exit /b 1

:find_qt
rem Newest QT_ROOT\6.x.y\msvc*_64 kit with windeployqt; versions are compared
rem numerically (6.11 is newer than 6.9), which a plain "dir" sort does not do.
set "QT_DIR="
for /f "usebackq delims=" %%Q in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-ChildItem -LiteralPath $env:QT_ROOT -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '\A6\.\d+\.\d+\z' } | Sort-Object { [version]$_.Name } -Descending | ForEach-Object { Get-ChildItem -LiteralPath $_.FullName -Directory -Filter 'msvc*_64' } | Where-Object { Test-Path (Join-Path $_.FullName 'bin\windeployqt.exe') } | Select-Object -First 1 -ExpandProperty FullName"`) do set "QT_DIR=%%Q"
exit /b 0
