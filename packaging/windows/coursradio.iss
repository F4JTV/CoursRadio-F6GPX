; Inno Setup script for Cours Radioamateur (Windows 10/11, 64-bit).
; Called by build_windows.bat with:
;   /DAppVersion=<x.y.z> /DSourceDir=<deployed folder> /DProjectDir=<source tree>

#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif
#ifndef SourceDir
  #error SourceDir (folder produced by windeployqt) must be defined
#endif
#ifndef ProjectDir
  #define ProjectDir "..\.."
#endif

#define AppName "Cours Radioamateur"
#define AppExe "CoursRadio.exe"
#define AppPublisher "CoursRadio Community"

[Setup]
AppId={{6C2E8B1D-4A7F-4E39-9B52-3D0F1A7C5E84}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL=https://f6kgl-f5kff.fr
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
LicenseFile={#ProjectDir}\LICENSE.md
OutputBaseFilename=CoursRadio-{#AppVersion}-win64-setup
SetupIconFile={#ProjectDir}\packaging\windows\coursradio.ico
UninstallDisplayIcon={app}\{#AppExe}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExe}"
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExe}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
