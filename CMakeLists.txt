cmake_minimum_required(VERSION 3.16)

project(CoursRadio VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

# Qt 6.4 is the version shipped by Ubuntu 24.04; newer versions work too.
find_package(Qt6 6.4 REQUIRED COMPONENTS Core Gui Qml Quick QuickControls2)

qt_standard_project_setup()

# Newer Qt versions: no Android path in this project uses generator
# expressions, so the new behaviour of QTP0002 is fine (Qt 6.4 has no policies).
if(QT_KNOWN_POLICY_QTP0002)
    qt_policy(SET QTP0002 NEW)
endif()

qt_add_executable(CoursRadio
    src/main.cpp
)

target_compile_definitions(CoursRadio PRIVATE COURSRADIO_VERSION="${PROJECT_VERSION}")
target_include_directories(CoursRadio PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)

# --- QML module -------------------------------------------------------------
file(GLOB QML_SOURCES RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} CONFIGURE_DEPENDS qml/*.qml)
foreach(qml_file IN LISTS QML_SOURCES)
    get_filename_component(qml_name ${qml_file} NAME)
    set_source_files_properties(${qml_file} PROPERTIES QT_RESOURCE_ALIAS ${qml_name})
endforeach()
set_source_files_properties(qml/Style.qml PROPERTIES QT_QML_SINGLETON_TYPE TRUE)

qt_add_qml_module(CoursRadio
    URI CoursRadio
    VERSION 1.0
    RESOURCE_PREFIX /
    OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/qml/CoursRadio
    # lets androiddeployqt and qmllint find this module in the build tree
    IMPORT_PATH ${CMAKE_CURRENT_BINARY_DIR}/qml
    QML_FILES ${QML_SOURCES}
    SOURCES
        src/appsettings.h src/appsettings.cpp
        src/contentstore.h src/contentstore.cpp
        src/diagram.h src/diagram.cpp
        src/diagramitem.h src/diagramitem.cpp
        src/themecolors.h src/themecolors.cpp
)

# --- Resources ----------------------------------------------------------------
file(GLOB_RECURSE CONTENT_FILES RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} CONFIGURE_DEPENDS
    content/*.json content/*.jpg content/*.png)
qt_add_resources(CoursRadio "content"
    PREFIX "/"
    FILES ${CONTENT_FILES}
)

file(GLOB FONT_FILES RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} CONFIGURE_DEPENDS fonts/*.ttf)
qt_add_resources(CoursRadio "fonts"
    PREFIX "/fonts"
    BASE fonts
    FILES ${FONT_FILES}
)

file(GLOB ICON_FILES RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} CONFIGURE_DEPENDS icons/*.png)
qt_add_resources(CoursRadio "icons"
    PREFIX "/icons"
    BASE icons
    FILES ${ICON_FILES}
)

target_link_libraries(CoursRadio PRIVATE
    Qt6::Core Qt6::Gui Qt6::Qml Qt6::Quick Qt6::QuickControls2
)

# --- Platform specifics ---------------------------------------------------------
if(WIN32)
    set_target_properties(CoursRadio PROPERTIES WIN32_EXECUTABLE ON)
    # Icon and version resource (absolute icon path written by configure_file)
    set(COURSRADIO_ICO "${CMAKE_CURRENT_SOURCE_DIR}/packaging/windows/coursradio.ico")
    string(REPLACE "." "," COURSRADIO_VERSION_COMMAS "${PROJECT_VERSION}.0")
    configure_file(packaging/windows/coursradio.rc.in ${CMAKE_CURRENT_BINARY_DIR}/coursradio.rc @ONLY)
    target_sources(CoursRadio PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/coursradio.rc)
endif()

if(APPLE)
    # Application bundle CoursRadio.app with its icon
    set(COURSRADIO_ICNS "${CMAKE_CURRENT_SOURCE_DIR}/packaging/macos/coursradio.icns")
    set_source_files_properties(${COURSRADIO_ICNS} PROPERTIES MACOSX_PACKAGE_LOCATION "Resources")
    target_sources(CoursRadio PRIVATE ${COURSRADIO_ICNS})
    set_target_properties(CoursRadio PROPERTIES
        MACOSX_BUNDLE TRUE
        MACOSX_BUNDLE_BUNDLE_NAME "Cours Radioamateur"
        MACOSX_BUNDLE_GUI_IDENTIFIER org.coursradio.CoursRadio
        MACOSX_BUNDLE_ICON_FILE coursradio.icns
        MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
        MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION}
        MACOSX_BUNDLE_COPYRIGHT "CC BY-NC-SA 4.0 - F6GPX, CoursRadio Community"
    )
endif()

if(UNIX AND NOT APPLE AND NOT ANDROID)
    # Lower-case command name on Linux (/usr/bin/coursradio)
    set_target_properties(CoursRadio PROPERTIES OUTPUT_NAME coursradio)
endif()

if(ANDROID)
    set_target_properties(CoursRadio PROPERTIES
        QT_ANDROID_PACKAGE_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/packaging/android
        QT_ANDROID_VERSION_NAME ${PROJECT_VERSION}
        QT_ANDROID_VERSION_CODE 10000
    )
endif()

include(GNUInstallDirs)
# LIBRARY: on Android the application is a shared library loaded by the APK
install(TARGETS CoursRadio
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

if(UNIX AND NOT APPLE AND NOT ANDROID)
    install(FILES packaging/linux/coursradio.desktop
        DESTINATION ${CMAKE_INSTALL_DATADIR}/applications)
    install(FILES packaging/linux/coursradio.metainfo.xml
        DESTINATION ${CMAKE_INSTALL_DATADIR}/metainfo)
    install(FILES icons/coursradio.png
        DESTINATION ${CMAKE_INSTALL_DATADIR}/icons/hicolor/512x512/apps)
    install(FILES icons/coursradio-256.png
        DESTINATION ${CMAKE_INSTALL_DATADIR}/icons/hicolor/256x256/apps
        RENAME coursradio.png)
endif()

# --- Developer tool: diagram preview (not installed) ----------------------------
option(COURSRADIO_BUILD_TOOLS "Build the figrender preview tool" OFF)
if(COURSRADIO_BUILD_TOOLS)
    add_executable(figrender tools/figrender/main.cpp src/diagram.cpp src/themecolors.cpp)
    target_link_libraries(figrender PRIVATE Qt6::Core Qt6::Gui)
endif()
